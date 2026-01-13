"""CLI implementation for Gibberifire."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gibberifire.cli.config import ConfigManager
from gibberifire.core.exceptions import ConfigurationError
from gibberifire.core.gibberifire import Gibberifire


def create_parser() -> argparse.ArgumentParser:
    """Create an argument parser for CLI."""
    parser = argparse.ArgumentParser(
        prog='gibberifire',
        description=(
            'Protect text from AI or humans: invisible Unicode noise or reversible encodings. '
            'Reads from STDIN, writes to STDOUT.'
        ),
    )

    # Global arguments
    parser.add_argument('-c', '--config', help='Path to configuration file', type=Path, default=None)

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Common profile argument
    profile_arg = {
        'flags': ['-p', '--profile'],
        'kwargs': {'default': 'medium', 'help': 'Protection profile name (default: medium)'},
    }

    # Protect command
    protect_parser = subparsers.add_parser('protect', help='Protect text (STDIN -> STDOUT)')
    protect_parser.add_argument(*profile_arg['flags'], **profile_arg['kwargs'])

    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Remove protection (STDIN -> STDOUT)')
    clean_parser.add_argument(*profile_arg['flags'], **profile_arg['kwargs'])

    # Detect command
    detect_parser = subparsers.add_parser('detect', help="Check protection (STDIN -> 'True'/'False' + Exit Code)")
    detect_parser.add_argument(*profile_arg['flags'], **profile_arg['kwargs'])

    return parser


def handle_input(parser: argparse.ArgumentParser) -> str:
    """
    Read input from STDIN.

    If run in interactive terminal without pipe, print error and help.
    Ensures UTF-8 encoding is used.
    """
    if sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.stderr.write('\nError: No input provided. Pipe text to STDIN.\n')
        raise SystemExit(1)

    try:
        # Explicitly reconfigure stdin to utf-8 if needed, mostly relevant if system locale is ASCII
        # In Python 3.7+, sys.stdin usually honors PYTHONIOENCODING or locale.
        # Reading buffer and decoding is safest for forced UTF-8.
        # But standard sys.stdin.read() is preferred unless we want to force UTF-8 over system locale.
        # Given our domain is Unicode, forcing UTF-8 is safer.
        return sys.stdin.buffer.read().decode('utf-8')
    except (UnicodeDecodeError, OSError) as exc:
        sys.stderr.write(f'Error reading input: {exc}\n')
        raise SystemExit(1) from exc


def load_configuration(args: argparse.Namespace) -> Gibberifire:
    """Load configuration and initialize Gibberifire instance."""
    config_manager = ConfigManager(args.config)
    config_file = config_manager.load()

    profile_name = getattr(args, 'profile', 'medium')

    if profile_name not in config_file.profiles:
        message = f"Profile '{profile_name}' not found in configuration."
        raise ConfigurationError(message)

    profile = config_file.profiles[profile_name]
    return Gibberifire(profile=profile)


def process_command(gf: Gibberifire, command: str, text: str) -> int:
    """
    Process the text with the given command using the initialized Gibberifire instance.

    :return: Exit code
    """
    # Ensure stdout writes UTF-8
    # sys.stdout might be ascii in some docker containers
    if hasattr(sys.stdout, 'buffer'):
        stdout_writer = lambda s: sys.stdout.buffer.write(s.encode('utf-8'))  # noqa: E731
    else:
        stdout_writer = sys.stdout.write

    if command == 'protect':
        result = gf.protect(text)
        stdout_writer(result)
        return 0

    if command == 'clean':
        result = gf.clean(text)
        stdout_writer(result)
        return 0

    if command == 'detect':
        is_protected = gf.is_protected(text)
        # Detect output is simple ascii usually (True/False), but for consistency
        stdout_writer(str(is_protected))
        # Return exit code for shell scripting (0 = Protected, 1 = Clean/False)
        return 0 if is_protected else 1

    return 1


def main(argv: list[str] | None = None) -> int:
    """
    Run the CLI entry point.

    :param argv: Command line arguments (default: sys.argv[1:])
    :return: Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        input_text = handle_input(parser)
        gf = load_configuration(args)
        return process_command(gf, args.command, input_text)

    except ConfigurationError as exc:
        sys.stderr.write(f'Error: {exc}\n')
        return 1
    except OSError as exc:
        sys.stderr.write(f'I/O error: {exc}\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
