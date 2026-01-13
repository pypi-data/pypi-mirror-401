# Gibberifire 🔥

[![PyPI version](https://img.shields.io/pypi/v/gibberifire)](https://pypi.org/project/gibberifire/)
[![Python versions](https://img.shields.io/pypi/pyversions/gibberifire)](https://pypi.org/project/gibberifire/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/vlad-gavrilov/gibberifire/ci.yml?branch=master&label=CI)](https://github.com/vlad-gavrilov/gibberifire/actions/workflows/ci.yml)

**Gibberifire** is a Python library and CLI tool designed to "protect" text by corrupting what either
humans **or** LLMs see. It can inject invisible/visually identical Unicode noise to keep text
human-readable but model-hostile, or, conversely, encode text so it is **LLM-readable but
human-gibberish**.

> **Warning**: This tool is for education and research. Obfuscation can be removed by models or
> cleaning scripts. API stability is **not guaranteed** until `1.0.0` (SemVer `0.x` rules).

## Features

* **Invisible Protection**: Uses Zero-Width Spaces (ZWSP), Homoglyphs, Combining Characters, and Bidirectional (Bidi)
  markers to fool LLMs while keeping humans comfortable.
* **Human-Obscuring Encoding**: New encoding method (hex/emoji) makes text hard to read for humans but straightforward
  for LLMs to decode.
* **Reversibility**: Provides a `clean` method to restore the original text for both directions.
* **Detection**: Can detect if text has been "protected"/encoded.
* **Configurable Profiles**: Use built-in profiles (`low`, `medium`, `high`, `encoded`) or create your own flexible
  configuration.
* **Async Support**: Fully supports asynchronous operations.
* **CLI**: Unix-style command line interface (works with pipes).

## Installation

```bash
pip install gibberifire
```

## Usage

### CLI

The CLI is designed to work with standard input (STDIN) and standard output (STDOUT).

**Basic Usage:**

```bash
# Protect text from a pipe
echo "Hello World" | gibberifire protect > protected.txt

# Clean text
cat protected.txt | gibberifire clean

# Detect protection (returns exit code 0 if protected, 1 if clean)
cat file.txt | gibberifire detect
```

**With Profiles:**

```bash
# Use 'high' profile
cat data.txt | gibberifire protect -p high > protected.txt

# Clean using specific profile pipeline (recommended)
cat protected.txt | gibberifire clean -p high > restored.txt

# Make text LLM-readable but human-gibberish
echo "Secret plan" | gibberifire protect -p encoded > encoded.txt

# Clean using the same profile
cat encoded.txt | gibberifire clean -p encoded > restored.txt
```

**With Custom Config:**

```bash
cat data.txt | gibberifire -c ./my_config.yaml protect -p custom_profile
```

### Python API

```python
from gibberifire import Gibberifire, Profile, PipelineStep
from gibberifire.core.models import ZWSPParams, HomoglyphParams, DEFAULT_PROFILES

profile = DEFAULT_PROFILES["medium"]
gf = Gibberifire(profile=profile)

protected = gf.protect("Hello, World!")
print(protected)

cleaned = gf.clean(protected)
assert cleaned == "Hello, World!"
```

### Async API

```python
import asyncio

from gibberifire import AsyncGibberifire, PipelineStep, Profile
from gibberifire.core.models import ZWSPParams


async def main() -> None:
    custom_profile = Profile(
        description="Async demo using a lighter ZWSP mix",
        pipeline=[
            PipelineStep(
                method="zwsp",
                params=ZWSPParams(min_burst=2, max_burst=6, seed=42),
            ),
        ],
    )

    async with AsyncGibberifire(profile=custom_profile) as gf:
        protected = await gf.protect("Async hello from Gibberifire!")
        print(protected)

        if await gf.is_protected(protected):
            restored = await gf.clean(protected)
            print(restored)


asyncio.run(main())
```

### Configuration File Example

```yaml
profiles:
  my_custom_profile:
    description: "Custom protection mix"
    pipeline:
      - method: zwsp
        params:
          min_burst: 2
          max_burst: 5
          preserve_emoji: true
          seed: 123
      - method: homoglyph
        params:
          probability: 0.3
```

## Further Reading

- See the [Deep Dive](docs/DEEP_DIVE.md) section for a detailed walkthrough of methods, defaults, and limitations.

## Versioning & Releases

- SemVer `0.x`: breaking changes are possible until `1.0.0`.
- Release notes live in [CHANGELOG.md](CHANGELOG.md).

## Contributing & Security

- Contributions are welcome—see [CONTRIBUTING.md](CONTRIBUTING.md).
- Responsible use, limitations, and reporting guidance are in [SECURITY.md](SECURITY.md). There is no
  warranty; use at your own risk.

## License

MIT. See [LICENSE](LICENSE).
