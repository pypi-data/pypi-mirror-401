from pydantic import BaseModel


class Icon(BaseModel):
    """Model for an icon."""

    value: str
    original_file_extension: str
    encoding: str
    mime_type: str
