"""Original file upload service.

The upload module only stores original files and returns storage metadata. It
must not create L0/L1 candidates or L2 facts.
"""

from dataclasses import dataclass
from pathlib import Path
from re import search
from uuid import uuid4

from fastapi import HTTPException, status

from app.modules.upload.schemas import UploadFileStoredResponse

CODE_ROOT = Path(__file__).resolve().parents[5]
UPLOAD_ROOT = CODE_ROOT / "storage" / "dev" / "uploads"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_MULTIPART_BYTES = MAX_UPLOAD_BYTES + 64 * 1024
ALLOWED_EXTENSIONS = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".pdf": "application/pdf",
}


@dataclass(frozen=True)
class ParsedMultipartFile:
    filename: str
    content_type: str
    content: bytes


def save_original_file_from_multipart(content_type: str, body: bytes) -> UploadFileStoredResponse:
    if len(body) > MAX_MULTIPART_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="文件大小不能超过 10MB。",
        )

    parsed_file = parse_single_file_part(content_type, body)
    safe_filename = sanitize_filename(parsed_file.filename)
    extension = Path(safe_filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="仅支持 jpg、jpeg、png、pdf 文件。",
        )
    if len(parsed_file.content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="文件大小不能超过 10MB。",
        )
    if len(parsed_file.content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="上传文件不能为空。")

    upload_id = f"upload_{uuid4().hex}"
    saved_filename = f"{upload_id}{extension}"
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    saved_path = UPLOAD_ROOT / saved_filename
    saved_path.write_bytes(parsed_file.content)

    return UploadFileStoredResponse(
        upload_id=upload_id,
        filename=safe_filename,
        content_type=parsed_file.content_type or ALLOWED_EXTENSIONS[extension],
        file_size=len(parsed_file.content),
        storage_path=f"storage/dev/uploads/{saved_filename}",
        saved=True,
    )


def parse_single_file_part(content_type: str, body: bytes) -> ParsedMultipartFile:
    boundary = extract_multipart_boundary(content_type)
    delimiter = f"--{boundary}".encode("utf-8")
    for raw_part in body.split(delimiter):
        part = raw_part.strip(b"\r\n")
        if not part or part == b"--":
            continue
        if part.endswith(b"--"):
            part = part[:-2].rstrip(b"\r\n")
        header_bytes, separator, content = part.partition(b"\r\n\r\n")
        if not separator:
            continue
        headers = parse_part_headers(header_bytes)
        disposition = headers.get("content-disposition", "")
        if 'name="file"' not in disposition:
            continue
        filename = extract_disposition_filename(disposition)
        if content.endswith(b"\r\n"):
            content = content[:-2]
        return ParsedMultipartFile(
            filename=filename,
            content_type=headers.get("content-type", ""),
            content=content,
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="缺少上传文件。")


def extract_multipart_boundary(content_type: str) -> str:
    if "multipart/form-data" not in content_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请求必须使用 multipart/form-data。")
    match = search(r'boundary="?([^";]+)"?', content_type)
    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="缺少 multipart boundary。")
    return match.group(1)


def parse_part_headers(header_bytes: bytes) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in header_bytes.decode("latin-1").split("\r\n"):
        name, separator, value = line.partition(":")
        if separator:
            headers[name.strip().lower()] = value.strip()
    return headers


def extract_disposition_filename(disposition: str) -> str:
    match = search(r'filename="([^"]+)"', disposition)
    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="缺少文件名。")
    return match.group(1)


def sanitize_filename(filename: str) -> str:
    safe_name = Path(filename).name.strip()
    if not safe_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="缺少文件名。")
    return safe_name
