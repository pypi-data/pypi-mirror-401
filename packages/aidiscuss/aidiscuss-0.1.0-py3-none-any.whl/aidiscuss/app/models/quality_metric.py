"""
Quality Metric Model

Stores quality assessment results for agent responses including:
- RAG grounding scores
- LLM-as-Judge evaluations
- Novelty scores
- Persona consistency scores
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from aidiscuss.app.db.base import Base


class QualityCheckResult(BaseModel):
    """Pydantic schema for quality check result"""

    conversation_id: str
    message_id: str
    turn_number: int
    agent_id: Optional[str] = None

    # Quality scores (0.0 - 1.0 scale)
    rag_grounding_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="How well response is grounded in RAG context"
    )
    llm_judge_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="LLM-as-Judge quality score"
    )
    novelty_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Novelty score (1.0 - max_similarity with recent responses)"
    )
    consistency_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Persona consistency score"
    )

    # Overall assessment
    passed_quality_check: bool = Field(
        default=True,
        description="Whether response passed quality threshold"
    )
    aggregate_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Weighted average of all quality scores"
    )

    # Feedback
    feedback: List[str] = Field(
        default_factory=list,
        description="List of quality issues or warnings"
    )
    citations: List[str] = Field(
        default_factory=list,
        description="Citations extracted from response (if RAG enabled)"
    )

    # Regeneration tracking
    regeneration_attempt: int = Field(
        default=0,
        ge=0,
        description="Which regeneration attempt this is (0 = first attempt)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "message_id": "msg_456",
                "turn_number": 5,
                "agent_id": "agent_1",
                "rag_grounding_score": 0.85,
                "llm_judge_score": 0.92,
                "novelty_score": 0.78,
                "passed_quality_check": True,
                "aggregate_score": 0.85,
                "feedback": [],
                "citations": ["Source: Economics Report 2025, p.42"]
            }
        }


class QualityMetric(Base):
    """Database model for quality metrics"""
    __tablename__ = "quality_metrics"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False, index=True)
    message_id = Column(String, nullable=False, index=True)
    turn_number = Column(Integer, nullable=False)
    agent_id = Column(String, nullable=True)

    # Quality scores
    rag_grounding_score = Column(Float, nullable=True)
    llm_judge_score = Column(Float, nullable=True)
    novelty_score = Column(Float, nullable=True)
    consistency_score = Column(Float, nullable=True)
    aggregate_score = Column(Float, nullable=True)

    # Assessment result
    passed_quality_check = Column(Boolean, nullable=False, default=True)
    feedback = Column(JSON, nullable=True)  # List of feedback strings
    citations = Column(JSON, nullable=True)  # List of citation strings
    regeneration_attempt = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_schema(self) -> QualityCheckResult:
        """Convert database model to Pydantic schema"""
        return QualityCheckResult(
            conversation_id=self.conversation_id,
            message_id=self.message_id,
            turn_number=self.turn_number,
            agent_id=self.agent_id,
            rag_grounding_score=self.rag_grounding_score,
            llm_judge_score=self.llm_judge_score,
            novelty_score=self.novelty_score,
            consistency_score=self.consistency_score,
            aggregate_score=self.aggregate_score,
            passed_quality_check=self.passed_quality_check,
            feedback=self.feedback or [],
            citations=self.citations or [],
            regeneration_attempt=self.regeneration_attempt
        )

    @staticmethod
    def from_schema(schema: QualityCheckResult, metric_id: str) -> "QualityMetric":
        """Create database model from Pydantic schema"""
        return QualityMetric(
            id=metric_id,
            conversation_id=schema.conversation_id,
            message_id=schema.message_id,
            turn_number=schema.turn_number,
            agent_id=schema.agent_id,
            rag_grounding_score=schema.rag_grounding_score,
            llm_judge_score=schema.llm_judge_score,
            novelty_score=schema.novelty_score,
            consistency_score=schema.consistency_score,
            aggregate_score=schema.aggregate_score,
            passed_quality_check=schema.passed_quality_check,
            feedback=schema.feedback,
            citations=schema.citations,
            regeneration_attempt=schema.regeneration_attempt
        )

    def __repr__(self) -> str:
        return (
            f"<QualityMetric(id={self.id}, message_id={self.message_id}, "
            f"passed={self.passed_quality_check}, score={self.aggregate_score})>"
        )
