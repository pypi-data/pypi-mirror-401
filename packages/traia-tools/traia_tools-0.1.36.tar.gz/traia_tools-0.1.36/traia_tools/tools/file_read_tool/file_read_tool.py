from typing import Any, Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field


class FileReadToolSchema(BaseModel):
    """Input for FileReadTool."""

    # IMPORTANT:
    # Some runtimes (e.g., agent frameworks) may inject extra keys like
    # `security_context` when calling tools. We must not fail validation for that.
    #
    # We still enforce the public contract ("file_path only") inside `_run()`.
    model_config = ConfigDict(extra="ignore")

    # NOTE: Optional on purpose.
    # - If the tool was constructed with a default file path, callers can do `tool.run()`.
    # - Otherwise, callers must pass `file_path` at runtime.
    file_path: Optional[str] = Field(
        None, description="Full path to the file to read (optional if provided at construction time)."
    )


class FileReadTool(BaseTool):
    """A tool for reading file contents.

    This tool inherits its schema handling from BaseTool to avoid recursive schema
    definition issues. The args_schema is set to FileReadToolSchema which defines
    the file_path parameter. The schema should not be overridden in the
    constructor as it would break the inheritance chain and cause infinite loops.

    The tool supports two ways of specifying the file path:
    1. At construction time via the file_path parameter
    2. At runtime via the file_path parameter in the tool's input

    Args:
        file_path (Optional[str]): Path to the file to be read. If provided,
            this becomes the default file path for the tool.
        **kwargs: Additional keyword arguments passed to BaseTool.

    Example:
        >>> tool = FileReadTool(file_path="/path/to/file.txt")
        >>> content = tool.run()  # Reads /path/to/file.txt
        >>> content = tool.run(file_path="/path/to/other.txt")  # Reads other.txt
    """

    name: str = "Read a file's content"
    description: str = (
        "Reads the full contents of a file. Input: 'file_path'."
    )
    args_schema: Type[BaseModel] = FileReadToolSchema
    file_path: Optional[str] = None

    def __init__(self, file_path: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize the FileReadTool.

        Args:
            file_path (Optional[str]): Path to the file to be read. If provided,
                this becomes the default file path for the tool.
            **kwargs: Additional keyword arguments passed to BaseTool.
        """
        if file_path is not None:
            kwargs["description"] = (
                f"Reads the full contents of a file. Default file: {file_path}. Override with 'file_path'."
            )

        super().__init__(**kwargs)
        self.file_path = file_path

    def _run(
        self,
        **kwargs: Any,
    ) -> str:
        # Be tolerant to framework-injected parameters.
        # Some runtimes add keys like `security_context` (and sometimes other metadata).
        # As long as we have a file path (constructor default or runtime override),
        # we proceed and simply ignore everything else.
        file_path = kwargs.get("file_path", self.file_path)

        if file_path is None:
            return (
                "Error: No file path provided. Please provide a file path either in the constructor or as an argument."
            )

        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"Error: File not found at path: {file_path}"
        except PermissionError:
            return f"Error: Permission denied when trying to read file: {file_path}"
        except Exception as e:
            return f"Error: Failed to read file {file_path}. {str(e)}"