"""L0 原始输入接收路由。"""

from fastapi import APIRouter

from app.modules.l0_input.schemas import RawInputCreate, RawInputReceived
from app.modules.l0_input.service import receive_raw_input

router = APIRouter(prefix="/l0", tags=["l0-raw-input"])


@router.post("/raw-input", response_model=RawInputReceived)
def create_raw_input(payload: RawInputCreate) -> RawInputReceived:
    return receive_raw_input(payload)
