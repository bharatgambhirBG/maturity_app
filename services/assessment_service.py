from typing import List, Dict
from sqlalchemy.orm import Session
from .scoring_service import calculate_scores
from data.repository import save_assessment

def process_and_save_assessment(
    db: Session,
    user_name: str,
    org: str,
    answers: List[Dict],
):
    scoring = calculate_scores(answers)
    assessment = save_assessment(
        db=db,
        user_name=user_name,
        org=org,
        overall_score=scoring["overall_score"],
        maturity_level=scoring["maturity_level"],
        answers=answers,
    )
    return assessment, scoring