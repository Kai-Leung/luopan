"""语音转写网关 Schema。

只表达音频转写结果，不承接 L0-L7 业务链路。
"""

from typing import Literal

from pydantic import BaseModel


class VoiceTranscriptionResponse(BaseModel):
    status: Literal["transcribed"]
    text: str
