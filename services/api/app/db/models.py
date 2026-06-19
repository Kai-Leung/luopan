from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

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


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    trace_ref = Column(String, nullable=False, index=True)
    source_fact_id = Column(String, nullable=True, index=True)
    raw_input_id = Column(String, nullable=True, index=True)
    candidate_id = Column(String, nullable=True, index=True)
    governance_id = Column(String, nullable=True, index=True)
    review_id = Column(String, nullable=True, index=True)
    analysis_id = Column(String, nullable=True, index=True)
    recommendation_id = Column(String, nullable=True, index=True)
    execution_response_id = Column(String, nullable=True, index=True)
    feedback_id = Column(String, nullable=True, index=True)
    source_stage = Column(String, nullable=False)
    target_stage = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    actor_id = Column(String, nullable=False)
    organization_id = Column(String, nullable=False, index=True)
    readonly = Column(Boolean, nullable=False, default=True)
    no_write_l2 = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False)


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, nullable=False, index=True)
    source_fact_id = Column(String, nullable=False, index=True)
    trace_ref = Column(String, nullable=False, index=True)
    analysis_status = Column(String, nullable=False)
    analysis_summary = Column(Text, nullable=False)
    organization_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)


class RecommendationRecord(Base):
    __tablename__ = "recommendation_records"

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(String, unique=True, nullable=False, index=True)
    analysis_id = Column(String, nullable=True, index=True)
    source_fact_id = Column(String, nullable=True, index=True)
    trace_ref = Column(String, nullable=False, index=True)
    recommendation_status = Column(String, nullable=False)
    recommendation_summary = Column(Text, nullable=False)
    organization_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)


class ExecutionResponseRecord(Base):
    __tablename__ = "execution_response_records"

    id = Column(Integer, primary_key=True, index=True)
    execution_response_id = Column(String, unique=True, nullable=False, index=True)
    recommendation_id = Column(String, nullable=True, index=True)
    source_fact_id = Column(String, nullable=True, index=True)
    trace_ref = Column(String, nullable=False, index=True)
    execution_status = Column(String, nullable=False)
    execution_note = Column(Text, nullable=False)
    organization_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)


class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(String, unique=True, nullable=False, index=True)
    execution_response_id = Column(String, nullable=True, index=True)
    source_fact_id = Column(String, nullable=True, index=True)
    trace_ref = Column(String, nullable=False, index=True)
    feedback_status = Column(String, nullable=False)
    feedback_type = Column(String, nullable=True)
    feedback_note = Column(Text, nullable=False)
    return_raw_input_id = Column(String, nullable=False, index=True)
    return_candidate_id = Column(String, nullable=False, index=True)
    organization_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
