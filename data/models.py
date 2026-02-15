from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float,
    ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from data.db import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    assessed_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    domains = relationship("Domain", back_populates="assessment")
    metrics = relationship("AssessmentMetrics", back_populates="assessment", uselist=False)
    responses = relationship("Response", back_populates="assessment")


class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    domain_id = Column(String, nullable=False)  # JSON ID
    name = Column(String, nullable=False)

    assessment = relationship("Assessment", back_populates="domains")
    subdomains = relationship("Subdomain", back_populates="domain")


class Subdomain(Base):
    __tablename__ = "subdomains"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=False)
    subdomain_id = Column(String, nullable=False)  # JSON ID
    name = Column(String, nullable=False)

    domain = relationship("Domain", back_populates="subdomains")
    questions = relationship("Question", back_populates="subdomain")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subdomain_id = Column(Integer, ForeignKey("subdomains.id"), nullable=False)
    question_id = Column(String, nullable=False)  # JSON ID
    text = Column(Text, nullable=False)
    help_text = Column(Text, nullable=True)

    subdomain = relationship("Subdomain", back_populates="questions")
    responses = relationship("Response", back_populates="question")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    maturity = Column(Integer, nullable=False)
    criticality = Column(Integer, nullable=False)
    risk_exposure = Column(String, nullable=False)
    remediation_effort = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    evidence_path = Column(Text, nullable=True)

    assessment = relationship("Assessment", back_populates="responses")
    question = relationship("Question", back_populates="responses")


class AssessmentMetrics(Base):
    __tablename__ = "assessment_metrics"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), unique=True, nullable=False)

    ASS = Column(Float, default=0.0)
    TDI = Column(Float, default=0.0)
    SCS = Column(Float, default=0.0)
    SCRS = Column(Float, default=0.0)
    ORS = Column(Float, default=0.0)
    DQGS = Column(Float, default=0.0)
    AIRS = Column(Float, default=0.0)
    TCKRS = Column(Float, default=0.0)
    MCE = Column(Float, default=0.0)
    SPS = Column(Float, default=0.0)

    assessment = relationship("Assessment", back_populates="metrics")