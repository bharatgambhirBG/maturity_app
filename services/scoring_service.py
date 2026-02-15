from sqlalchemy.orm import Session
from data.repository import Repository


class ScoringService:

    @staticmethod
    def _risk_weight(value: str) -> float:
        return {"Low": 0.8, "Medium": 1.0, "High": 1.2}.get(value, 1.0)

    @staticmethod
    def _effort_weight(value: str) -> float:
        return {"Low": 0.8, "Medium": 1.0, "High": 1.2}.get(value, 1.0)

    @staticmethod
    def _confidence_weight(value: str) -> float:
        return {"Low": 0.8, "Medium": 1.0, "High": 1.1}.get(value, 1.0)

    @staticmethod
    def compute_and_store_metrics(session: Session, assessment_id: int):
        responses = Repository.get_responses_for_assessment(session, assessment_id)
        if not responses:
            return None

        scores = []

        for r in responses:
            base = r.maturity * r.criticality
            risk_factor = ScoringService._risk_weight(r.risk_exposure)
            effort_factor = ScoringService._effort_weight(r.remediation_effort)
            conf_factor = ScoringService._confidence_weight(r.confidence)

            adjusted = base * risk_factor / effort_factor * conf_factor
            scores.append(adjusted)

        if not scores:
            return None

        avg = sum(scores) / len(scores)

        # Simple mapping of one composite score into 10 KPIs
        metrics = {
            "ASS": avg * 1.0,
            "TDI": max(0.0, 100 - avg),   # higher score → lower debt
            "SCS": avg * 0.9,
            "SCRS": avg * 0.85,
            "ORS": avg * 0.8,
            "DQGS": avg * 0.9,
            "AIRS": avg * 0.88,
            "TCKRS": avg * 0.75,
            "MCE": max(0.0, 100 - avg),  # inverse proxy
            "SPS": avg * 0.95,
        }

        return Repository.upsert_metrics(session, assessment_id, metrics)