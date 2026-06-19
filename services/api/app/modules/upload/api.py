"""Upload API.

This endpoint stores original files only. It does not enter L0/L1/S2/L2.
"""

from fastapi import APIRouter, Request

from app.modules.upload.schemas import UploadFileStoredResponse
from app.modules.upload.service import save_original_file_from_multipart

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/files", response_model=UploadFileStoredResponse)
async def upload_file(request: Request) -> UploadFileStoredResponse:
    return save_original_file_from_multipart(
        request.headers.get("content-type", ""),
        await request.body(),
    )
