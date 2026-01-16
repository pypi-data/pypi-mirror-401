"""Pre-release feature management and gating for the Arize SDK."""

import functools
import logging
from collections.abc import Callable
from enum import StrEnum

from arize.version import __version__

logger = logging.getLogger(__name__)


class ReleaseStage(StrEnum):
    """Enum representing the release stage of API features."""

    ALPHA = "alpha"
    BETA = "beta"


_WARNED: set[str] = set()


def _format_prerelease_message(*, key: str, stage: ReleaseStage) -> str:
    return (
        f"[{stage.upper()}] {key} is an {stage} API "
        f"in Arize SDK v{__version__} and may change without notice."
    )


def prerelease_endpoint(*, stage: ReleaseStage, key: str) -> object:
    """Decorate a method to emit a prerelease warning via logging once per process."""

    def deco(fn: Callable[..., object]) -> object:
        @functools.wraps(fn)
        def wrapper(*args: object, **kwargs: object) -> object:
            if key not in _WARNED:
                _WARNED.add(key)
                logger.warning(_format_prerelease_message(key=key, stage=stage))
            return fn(*args, **kwargs)

        return wrapper

    return deco
