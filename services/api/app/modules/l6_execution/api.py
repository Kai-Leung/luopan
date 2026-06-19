"""L6 execution response API."""

from fastapi import APIRouter

from app.modules.l6_execution.schemas import (
    L6ExecutionResponseRequest,
    L6ExecutionResponseResponse,
)
from app.modules.l6_execution.service import create_l6_execution_response

router = APIRouter(prefix="/l6", tags=["l6-execution"])


@router.post("/execution-responses", response_model=L6ExecutionResponseResponse)
def create_execution_response(
    payload: L6ExecutionResponseRequest,
) -> L6ExecutionResponseResponse:
    return create_l6_execution_response(payload)
