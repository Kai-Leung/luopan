"""Schemas for original file upload.

Upload only stores the original file and returns a reference. It does not create
candidates, facts, or governance records.
"""

from pydantic import BaseModel, ConfigDict


class UploadFileStoredResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    upload_id: str
    filename: str
    content_type: str
    file_size: int
    storage_path: str
    saved: bool
