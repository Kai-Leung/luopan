"""L0 原始输入接口 Schema。

只接收原始输入字段，不承接候选、治理、确认或真源入链字段。
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.modules.standard_governance.enums.source_types import SourceType


class RawInputCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    text: Optional[str] = None
    image_ref: Optional[str] = None
    file_ref: Optional[str] = None
    input_session_id: Optional[str] = None
    source_type: SourceType

    @model_validator(mode="after")
    def require_raw_payload(self) -> "RawInputCreate":
        if not any((self.text, self.image_ref, self.file_ref)):
            raise ValueError("text、image_ref、file_ref 至少提供一项")
        return self


class RawInputReceived(BaseModel):
    raw_input_id: str
    input_session_id: str
    status: str
    message: str
