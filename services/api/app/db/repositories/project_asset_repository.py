from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import ProjectAsset


def create_project_asset(
    db: Session,
    *,
    project_asset_id: str,
    project_name: str,
    customer_name: Optional[str],
    project_address: Optional[str],
    source_candidate_id: str,
    source_raw_input_id: str,
    status: str,
    created_at,
    confirmed_by: Optional[str],
    confirmation_id: str,
) -> ProjectAsset:
    row = ProjectAsset(
        project_asset_id=project_asset_id,
        project_name=project_name,
        customer_name=customer_name,
        project_address=project_address,
        source_candidate_id=source_candidate_id,
        source_raw_input_id=source_raw_input_id,
        status=status,
        created_at=created_at,
        confirmed_by=confirmed_by,
        confirmation_id=confirmation_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_project_asset(db: Session, project_asset_id: str) -> Optional[ProjectAsset]:
    return (
        db.query(ProjectAsset)
        .filter(ProjectAsset.project_asset_id == project_asset_id)
        .first()
    )


def list_project_assets(db: Session) -> list[ProjectAsset]:
    return db.query(ProjectAsset).order_by(ProjectAsset.created_at.asc()).all()
