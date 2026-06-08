from app.models.analysis import RiskAssessmentRequest, RiskAssessmentResponse, RiskLevel


class RiskAnalyzer:
    def assess(self, payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
        weighted_total = sum(signal.value * signal.weight for signal in payload.signals)
        weight_total = sum(signal.weight for signal in payload.signals)
        score = min(weighted_total / weight_total, 1.0)
        level = self._level_for_score(score)

        return RiskAssessmentResponse(
            subject_id=payload.subject_id,
            score=round(score, 4),
            level=level,
            recommendation=self._recommendation_for_level(level),
        )

    @staticmethod
    def _level_for_score(score: float) -> RiskLevel:
        if score >= 0.7:
            return RiskLevel.high
        if score >= 0.4:
            return RiskLevel.medium
        return RiskLevel.low

    @staticmethod
    def _recommendation_for_level(level: RiskLevel) -> str:
        recommendations = {
            RiskLevel.low: "Continue standard monitoring.",
            RiskLevel.medium: "Review the subject and increase monitoring cadence.",
            RiskLevel.high: "Escalate for immediate investigation.",
        }
        return recommendations[level]
