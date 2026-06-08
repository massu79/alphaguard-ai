from enum import StrEnum

from pydantic import BaseModel, Field


class RiskLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class RiskSignal(BaseModel):
    name: str = Field(..., min_length=1, examples=["failed_login_rate"])
    value: float = Field(..., ge=0, examples=[0.35])
    weight: float = Field(default=1.0, gt=0, le=10, examples=[2.0])


class RiskAssessmentRequest(BaseModel):
    subject_id: str = Field(..., min_length=1, examples=["account-123"])
    signals: list[RiskSignal] = Field(..., min_length=1)


class RiskAssessmentResponse(BaseModel):
    subject_id: str
    score: float = Field(..., ge=0, le=1)
    level: RiskLevel
    recommendation: str
