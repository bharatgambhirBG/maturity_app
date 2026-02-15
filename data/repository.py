from sqlalchemy.orm import Session
from data.models import (
    Assessment,
    Domain,
    Subdomain,
    Question,
    Response,
    AssessmentMetrics,
)


class Repository:

    # ---------------------------------------------------------
    # ASSESSMENT
    # ---------------------------------------------------------
    @staticmethod
    def create_assessment(session: Session, product_name: str, version: str, assessed_by: str):
        a = Assessment(
            product_name=product_name,
            version=version,
            assessed_by=assessed_by,
        )
        session.add(a)
        session.commit()
        session.refresh(a)
        return a

    @staticmethod
    def get_all_assessments(session: Session):
        return session.query(Assessment).order_by(Assessment.created_at.desc()).all()

    @staticmethod
    def get_assessment_by_id(session: Session, assessment_id: int):
        return session.query(Assessment).filter(Assessment.id == assessment_id).first()

    # ---------------------------------------------------------
    # STRUCTURE: DOMAIN / SUBDOMAIN / QUESTION
    # ---------------------------------------------------------
    @staticmethod
    def create_domain(session: Session, assessment_id: int, domain_id: str, name: str):
        d = Domain(
            assessment_id=assessment_id,
            domain_id=domain_id,
            name=name,
        )
        session.add(d)
        session.commit()
        session.refresh(d)
        return d

    @staticmethod
    def create_subdomain(session: Session, domain_id: int, subdomain_id: str, name: str):
        sd = Subdomain(
            domain_id=domain_id,
            subdomain_id=subdomain_id,
            name=name,
        )
        session.add(sd)
        session.commit()
        session.refresh(sd)
        return sd

    @staticmethod
    def create_question(session: Session, subdomain_id: int, question_id: str, text: str, help_text: str):
        q = Question(
            subdomain_id=subdomain_id,
            question_id=question_id,
            text=text,
            help_text=help_text,
        )
        session.add(q)
        session.commit()
        session.refresh(q)
        return q

    # ---------------------------------------------------------
    # RESPONSES
    # ---------------------------------------------------------
    @staticmethod
    def save_response(
        session: Session,
        assessment_id: int,
        question_id: int,
        data: dict,
        evidence_paths: list[str],
    ):
        r = Response(
            assessment_id=assessment_id,
            question_id=question_id,
            maturity=data["maturity"],
            criticality=data["criticality"],
            risk_exposure=data["risk_exposure"],
            remediation_effort=data["remediation_effort"],
            confidence=data["confidence"],
            notes=data["notes"],
            evidence_path=";".join(evidence_paths) if evidence_paths else None,
        )
        session.add(r)
        session.commit()
        session.refresh(r)
        return r

    @staticmethod
    def get_responses_for_assessment(session: Session, assessment_id: int):
        return (
            session.query(Response)
            .filter(Response.assessment_id == assessment_id)
            .all()
        )

    # ---------------------------------------------------------
    # METRICS (KPIs)
    # ---------------------------------------------------------
    @staticmethod
    def upsert_metrics(session: Session, assessment_id: int, metrics: dict):
        m = session.query(AssessmentMetrics).filter(
            AssessmentMetrics.assessment_id == assessment_id
        ).first()

        if not m:
            m = AssessmentMetrics(assessment_id=assessment_id)

        for key, value in metrics.items():
            setattr(m, key, value)

        session.add(m)
        session.commit()
        session.refresh(m)
        return m

    @staticmethod
    def get_metrics(session: Session, assessment_id: int):
        return session.query(AssessmentMetrics).filter(
            AssessmentMetrics.assessment_id == assessment_id
        ).first()