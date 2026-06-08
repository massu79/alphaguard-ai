from fastapi import APIRouter

from app.models.analysis import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.risk_analyzer import RiskAnalyzer

router = APIRouter()
analyzer = RiskAnalyzer()


@router.post("/assess", response_model=RiskAssessmentResponse)
def assess_risk(payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
    return analyzer.assess(payload)
