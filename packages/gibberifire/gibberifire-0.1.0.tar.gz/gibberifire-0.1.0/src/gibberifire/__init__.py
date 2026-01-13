"""
Gibberifire - Protect text by confusing either AIs or humans with reversible obfuscation.

Example::

    from gibberifire import Gibberifire
    from gibberifire.core.models import DEFAULT_PROFILES

    # Use a default profile
    profile = DEFAULT_PROFILES['medium']
    gf = Gibberifire(profile=profile)

    protected = gf.protect('Hello, World!')
    original = gf.clean(protected)

    # Check if text is protected
    if gf.is_protected(protected):
        print('Text has protection!')

Async usage::

    from gibberifire import AsyncGibberifire
    from gibberifire.core.models import DEFAULT_PROFILES

    async with AsyncGibberifire(profile=DEFAULT_PROFILES['medium']) as gf:
        protected = await gf.protect('Hello!')
"""

from gibberifire.asynchronous.gibberifire import AsyncGibberifire
from gibberifire.core.exceptions import GibberifireError
from gibberifire.core.gibberifire import Gibberifire
from gibberifire.core.models import DEFAULT_PROFILES, PipelineStep, Profile

__version__ = '0.1.0'
__all__ = [
    'DEFAULT_PROFILES',
    'AsyncGibberifire',
    'Gibberifire',
    'GibberifireError',
    'PipelineStep',
    'Profile',
    '__version__',
]
