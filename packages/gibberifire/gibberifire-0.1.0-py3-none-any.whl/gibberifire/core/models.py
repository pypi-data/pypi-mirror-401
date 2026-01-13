"""Configuration models using Pydantic."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, SerializeAsAny, model_validator


class BaseMethodParams(BaseModel):
    """
    Base class for method parameters.

    :param seed: Optional seed for deterministic behavior specific to this method.
                 If None, a random seed is used.
    """

    seed: int | None = None


class ZWSPParams(BaseMethodParams):
    """
    Parameters for ZWSP method.

    :param min_burst: Minimum number of invisible characters to inject per insertion.
    :param max_burst: Maximum number of invisible characters to inject per insertion.
    :param use_initial_burst: Whether to inject characters at the very beginning.
    :param initial_burst_min: Minimum characters for initial burst.
    :param initial_burst_max: Maximum characters for initial burst.
    :param preserve_emoji: Whether to preserve emoji sequences (don't inject inside them).
    """

    min_burst: int = Field(default=1, ge=0)
    max_burst: int = Field(default=3, ge=1)
    use_initial_burst: bool = False
    initial_burst_min: int = Field(default=1, ge=0)
    initial_burst_max: int = Field(default=3, ge=1)
    preserve_emoji: bool = True


class HomoglyphParams(BaseMethodParams):
    """Parameters for Homoglyph method."""

    probability: float = Field(default=0.2, ge=0.0, le=1.0)


class CombiningParams(BaseMethodParams):
    """Parameters for Combining method."""

    probability: float = Field(default=0.3, ge=0.0, le=1.0)


class BidiParams(BaseMethodParams):
    """Parameters for Bidi method."""

    # Currently no params


class EncodingParams(BaseMethodParams):
    """Parameters for Encoding method."""

    scheme: Literal['hex', 'emoji'] = 'hex'


class PipelineStep(BaseModel):
    """A single step in the protection pipeline."""

    method: str
    params: SerializeAsAny[BaseMethodParams] = Field(default_factory=BaseMethodParams)

    @model_validator(mode='before')
    @classmethod
    def instantiate_params(cls, data: object) -> object:
        """
        Automatically instantiate the correct Params class based on the 'method' field.

        This allows Pydantic to handle polymorphism without an explicit discriminator in 'params'.
        """
        if not isinstance(data, dict):
            return data

        method = data.get('method')
        params = data.get('params', {})

        # If params is already a model instance, don't convert
        if isinstance(params, BaseMethodParams):
            return data

        if isinstance(params, dict):
            if method == 'zwsp':
                data['params'] = ZWSPParams(**params)
            elif method == 'homoglyph':
                data['params'] = HomoglyphParams(**params)
            elif method == 'combining':
                data['params'] = CombiningParams(**params)
            elif method == 'bidi':
                data['params'] = BidiParams(**params)
            elif method == 'encoding':
                data['params'] = EncodingParams(**params)
            else:
                # Fallback for unknown methods or generic params
                data['params'] = BaseMethodParams(**params)
        return data


class Profile(BaseModel):
    """Configuration profile defining a protection strategy."""

    description: str = ''
    # seed is removed from here, it lives only in methods
    pipeline: list[PipelineStep]


class ConfigFile(BaseModel):
    """Structure of the configuration file."""

    profiles: dict[str, Profile]


# Default configuration to be written if file doesn't exist
DEFAULT_PROFILES = {
    'low': Profile(
        description='Minimal protection using only Zero-Width Spaces (1-3 chars). Invisible but easily detected.',
        pipeline=[PipelineStep(method='zwsp', params=ZWSPParams(min_burst=1, max_burst=3, use_initial_burst=False))],
    ),
    'medium': Profile(
        description='Standard protection using ZWSP (5-15 chars) and Homoglyphs (20%). Good balance.',
        pipeline=[
            PipelineStep(
                method='zwsp',
                params=ZWSPParams(
                    min_burst=5,
                    max_burst=15,
                    use_initial_burst=True,
                    initial_burst_min=5,
                    initial_burst_max=15,
                ),
            ),
            PipelineStep(method='homoglyph', params=HomoglyphParams(probability=0.2)),
        ],
    ),
    'high': Profile(
        description=(
            'Strong protection using all available methods and aggressive ZWSP (20-50 chars). May affect accessibility.'
        ),
        pipeline=[
            PipelineStep(method='bidi', params=BidiParams()),
            PipelineStep(
                method='zwsp',
                params=ZWSPParams(
                    min_burst=20,
                    max_burst=50,
                    use_initial_burst=True,
                    initial_burst_min=20,
                    initial_burst_max=50,
                ),
            ),
            PipelineStep(method='combining', params=CombiningParams(probability=0.3)),
            PipelineStep(method='homoglyph', params=HomoglyphParams(probability=0.4)),
        ],
    ),
    'encoded': Profile(
        description='Make text harder for humans to read while keeping it LLM-decodable (hex encoding).',
        pipeline=[
            PipelineStep(
                method='encoding',
                params=EncodingParams(scheme='hex'),
            ),
        ],
    ),
}
