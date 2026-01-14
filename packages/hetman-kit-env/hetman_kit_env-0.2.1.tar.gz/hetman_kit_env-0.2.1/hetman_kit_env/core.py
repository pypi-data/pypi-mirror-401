from __future__ import annotations

import json
from os import environ
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Unpack

from dotenv import load_dotenv
from pipeline import Pipe

from .exceptions import InvalidEnvironmentVariable, MissingEnvironmentVariable

if TYPE_CHECKING:
    from pipeline.core.pipe.resources.constants import PipeResult
    from pipeline.core.pipeline.resources.types import PipelinePipeConfig

T = TypeVar("T")


class EnvironmentVariable(Generic[T]):
    """
    Handles fetching, parsing, and validating environment variables.

    This class integrates with the `hetman-pipeline` system to automatically validate and 
    transform values retrieved from the system environment (`os.environ`). 
    It supports optional `.env` file loading and automatic JSON parsing.

    Attributes:
        dotenv_path (str | None): Path to the .env file. If None, the 
            python-dotenv library automatically searches for a .env file.
            The file is loaded during the first initialization of any class instance.

    Note:
        The class uses a `_dotenv_loaded` flag to ensure that the `.env` file 
        is loaded only once during the application lifecycle.
    """
    dotenv_path: str | None = None

    _dotenv_loaded: bool = False

    def __init__(
        self,
        name: str,
        parse_as_json: bool = True,
        **pipe_config: Unpack[PipelinePipeConfig]
    ) -> None:
        """
        Initializes the EnvironmentVariable instance and loads the value.

        Args:
            name: The name of the environment variable.
            parse_as_json: If True (default), attempts to parse the retrieved 
                string using `json.loads()`.
            **pipe_config: Arguments unpacked into the Pipe configuration, 
                such as `optional`, `check`, `match`, or `transform`.
        """
        self.name: str = name
        self.parse_as_json: bool = parse_as_json

        self.pipe_config: PipelinePipeConfig = pipe_config

        self._load_dotenv()

        self.variable: T = self.load_variable()

    def load_variable(self) -> T:
        """
        Executes the full loading and processing lifecycle.

        Fetches the raw value, optionally parses it as JSON, and then 
        passes it through the defined Pipe for final processing.

        Returns:
            T: The processed value, typed according to the generic parameter.
        """
        value: Any = self._load_raw_variable()

        if value is None:
            return value

        if self.parse_as_json:
            value = self._try_parse_as_json(value=value)

        value = self._send_variable_to_pipe(value=value)

        return value

    def _load_raw_variable(self) -> Any:
        """
        Retrieves the raw value from `os.environ`.

        Returns:
            Any: The environment variable value or None.

        Raises:
            MissingEnvironmentVariable: If the variable does not exist and 
                is not marked as `optional` in `pipe_config`.
        """
        value: Any = environ.get(self.name)

        if value is None and not self.pipe_config.get('optional'):
            raise MissingEnvironmentVariable(cls=self)

        return value

    def _try_parse_as_json(self, value: Any) -> Any:
        """
        Attempts to decode a string value as a JSON object.

        Args:
            value: The raw string value to parse.

        Returns:
            Any: The decoded object (dict, list, int, etc.) or the original 
                value if decoding fails.
        """
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def _send_variable_to_pipe(self, value: Any) -> T:
        """
        Passes the value to the Pipe class for validation and transformation.

        Args:
            value: The value to be processed.

        Returns:
            T: The final value after passing through the pipe.

        Raises:
            InvalidEnvironmentVariable: If the Pipe results contain 
                condition errors or match errors.
        """
        pipe: Pipe = Pipe(value=value, **self.pipe_config)

        result: PipeResult = pipe.run()

        if result.condition_errors or result.match_errors:
            raise InvalidEnvironmentVariable(cls=self, result=result)

        return result.value

    def _load_dotenv(self) -> None:
        """
        Loads the .env file using python-dotenv.

        Execution logic ensures the file is loaded only once per class lifecycle 
        if `dotenv_path` is defined.
        """
        if not self.__class__._dotenv_loaded:
            load_dotenv(dotenv_path=self.__class__.dotenv_path)

            self.__class__._dotenv_loaded = True

    @property
    def get(self) -> T:
        """
        Returns the loaded and processed environment variable.

        Returns:
            T: The stored variable value.
        """
        return self.variable

    def __str__(self) -> str:
        """Returns the string representation of the processed variable."""
        return str(self.get)

    def __repr__(self) -> str:
        """Returns a technical representation of the EnvironmentVariable instance."""
        return f"EnvironmentVariable(name={self.name})"

    def __bool__(self) -> bool:
        """Allows using the instance in boolean checks (e.g., if env_var:)."""
        return bool(self.get)

    def __eq__(self, other: Any) -> bool:
        """Enables equality comparison between the variable value and other objects."""
        if isinstance(other, EnvironmentVariable):
            return self.get == other.get

        return self.get == other

    def __call__(self) -> T:
        """Allows the instance to be called as a function to retrieve its value."""
        return self.get
