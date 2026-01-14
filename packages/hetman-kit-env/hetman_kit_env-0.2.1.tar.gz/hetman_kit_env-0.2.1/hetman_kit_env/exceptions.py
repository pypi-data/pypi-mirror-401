from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pipeline.core.pipe.resources.constants import PipeResult

    from .core import EnvironmentVariable


class MissingEnvironmentVariable(Exception):
    def __init__(self, cls: EnvironmentVariable) -> None:
        super().__init__(
            f"Required environment variable named \"{cls.name}\" is missing. Type: {cls.pipe_config['type'].__name__}."
        )


class InvalidEnvironmentVariable(Exception):
    def __init__(self, cls: EnvironmentVariable, result: PipeResult) -> None:

        super().__init__(
            f"The environment variable named \"{cls.name}\" is invaild. "
            f"Errors: {[*result.condition_errors, *result.match_errors]}"
        )
