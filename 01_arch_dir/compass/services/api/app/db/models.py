from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class RawInput(Base):
    __tablename__ = "raw_inputs"

    id = Column(Integer, primary_key=True, index=True)
    raw_input_id = Column(String, unique=True, nullable=False, index=True)
    source_type = Column(String, nullable=False)
    raw_payload = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    received_at = Column(DateTime(timezone=True), nullable=False)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String, unique=True, nullable=False, index=True)
    raw_input_id = Column(String, nullable=False, index=True)
    candidate_status = Column(String, nullable=False)
    candidate_payload = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class GovernanceResult(Base):
    __tablename__ = "governance_results"

    id = Column(Integer, primary_key=True, index=True)
    governance_id = Column(String, unique=True, nullable=False, index=True)
    candidate_id = Column(String, nullable=False, index=True)
    governance_status = Column(String, nullable=False)
    missing_fields = Column(Text, nullable=False)
    risk_hints = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class ManualReview(Base):
    __tablename__ = "manual_reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, nullable=False, index=True)
    governance_id = Column(String, nullable=False, index=True)
    review_action = Column(String, nullable=False)
    review_status = Column(String, nullable=False)
    policy_decision = Column(String, nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=False)


class FactRecord(Base):
    __tablename__ = "fact_records"

    id = Column(Integer, primary_key=True, index=True)
    fact_id = Column(String, unique=True, nullable=False, index=True)
    raw_input_id = Column(String, nullable=False, index=True)
    candidate_id = Column(String, nullable=False, index=True)
    governance_id = Column(String, nullable=False, index=True)
    review_id = Column(String, nullable=False, index=True)
    fact_type = Column(String, nullable=False)
    fact_payload = Column(Text, nullable=False)
    fact_status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class ProjectAsset(Base):
    __tablename__ = "project_assets"

    id = Column(Integer, primary_key=True, index=True)
    project_asset_id = Column(String, unique=True, nullable=False, index=True)
    project_name = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    project_address = Column(String, nullable=True)
    source_candidate_id = Column(String, nullable=False, index=True)
    source_raw_input_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    confirmed_by = Column(String, nullable=True)
    confirmation_id = Column(String, nullable=False, index=True)
