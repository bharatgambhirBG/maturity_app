from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from .db import Base, engine
from typing import List, Dict

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255))
    org = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    overall_score = Column(Float)
    maturity_level = Column(String(50))

    responses = relationship("Response", back_populates="assessment")

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    dimension = Column(String(100))
    question = Column(Text)
    answer = Column(Integer)
    score = Column(Float)

    assessment = relationship("Assessment", back_populates="responses")

def init_db():
    Base.metadata.create_all(bind=engine)

def save_assessment(db: Session, user_name: str, org: str,
                    overall_score: float, maturity_level: str,
                    answers: List[Dict]):
    assessment = Assessment(
        user_name=user_name,
        org=org,
        overall_score=overall_score,
        maturity_level=maturity_level,
    )
    db.add(assessment)
    db.flush()

    for ans in answers:
        resp = Response(
            assessment_id=assessment.id,
            dimension=ans["dimension"],
            question=ans["question"],
            answer=ans["answer"],
            score=ans["score"],
        )
        db.add(resp)

    db.commit()
    db.refresh(assessment)
    return assessment

def get_all_assessments(db: Session):
    return db.query(Assessment).all()

def get_assessment_details(db: Session, assessment_id: int):
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()