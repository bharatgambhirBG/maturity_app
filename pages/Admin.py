import streamlit as st
import pandas as pd
from data.db import SessionLocal
from data.repository import Repository


def get_db():
    return SessionLocal()


def main():
    st.title("Admin Dashboard")

    # ---------------------------------------------------------
    # KPI DEFINITIONS PANEL (PLAIN TEXT, COLLAPSIBLE PER KPI)
    # ---------------------------------------------------------
    with st.expander(" KPI Definitions, Formulas & Meaning", expanded=False):

        # -----------------------------
        # AvgScore Explanation
        # -----------------------------
        with st.expander(" How AvgScore Is Calculated", expanded=False):
            st.markdown("""
AvgScore is the core composite score used to derive all KPIs.  
It represents the overall technical strength of the product after adjusting for risk, effort, and confidence.

**Step 1 — Base Score**  
BaseScore = Maturity * Criticality

**Step 2 — Apply Risk Factor**  
RiskFactor values: Low = 0.8, Medium = 1.0, High = 1.2  
RiskAdjusted = BaseScore * RiskFactor

**Step 3 — Apply Effort Penalty**  
EffortFactor values: Low = 0.8, Medium = 1.0, High = 1.2  
EffortAdjusted = RiskAdjusted / EffortFactor

**Step 4 — Apply Confidence Weight**  
ConfidenceFactor values: Low = 0.8, Medium = 1.0, High = 1.1  
FinalQuestionScore = EffortAdjusted * ConfidenceFactor

**Step 5 — Compute the Average**  
AvgScore = Average(FinalQuestionScore across all questions)

**Meaning:**  
AvgScore reflects the overall technical maturity, weighted by importance, risk, effort, and certainty.
            """)

        # -----------------------------
        # KPI 1 — ASS
        # -----------------------------
        with st.expander(" 1. ASS — Architecture Sustainability Score", expanded=False):
            st.markdown("""
**Meaning:**  
Measures how maintainable, modular, and future-proof the architecture is.

**Formula:**  
ASS = AvgScore * 1.0

**High Score Means:**  
Architecture is clean, modular, and easier to evolve.
            """)

        # -----------------------------
        # KPI 2 — TDI
        # -----------------------------
        with st.expander(" 2. TDI — Technical Debt Index", expanded=False):
            st.markdown("""
**Meaning:**  
Quantifies accumulated technical debt.

**Formula:**  
TDI = 100 - AvgScore

**High Score Means:**  
High technical debt and higher modernization pressure.
            """)

        # -----------------------------
        # KPI 3 — SCS
        # -----------------------------
        with st.expander(" 3. SCS — Scalability Ceiling Score", expanded=False):
            st.markdown("""
**Meaning:**  
Measures how well the system can scale horizontally/vertically.

**Formula:**  
SCS = AvgScore * 0.9

**High Score Means:**  
System can scale with fewer architectural changes.
            """)

        # -----------------------------
        # KPI 4 — SCRS
        # -----------------------------
        with st.expander(" 4. SCRS — Security & Compliance Risk Score", expanded=False):
            st.markdown("""
**Meaning:**  
Evaluates vulnerabilities, security posture, and compliance gaps.

**Formula:**  
SCRS = AvgScore * 0.85

**High Score Means:**  
Lower security/compliance risk and better controls.
            """)

        # -----------------------------
        # KPI 5 — ORS
        # -----------------------------
        with st.expander("5. ORS — Operational Resilience Score", expanded=False):
            st.markdown("""
**Meaning:**  
Measures reliability, failover readiness, monitoring, and incident resilience.

**Formula:**  
ORS = AvgScore * 0.8

**High Score Means:**  
System is resilient, observable, and recoverable.
            """)

        # -----------------------------
        # KPI 6 — DQGS
        # -----------------------------
        with st.expander(" 6. DQGS — Data Quality & Governance Score", expanded=False):
            st.markdown("""
**Meaning:**  
Evaluates data accuracy, lineage, governance, and stewardship.

**Formula:**  
DQGS = AvgScore * 0.9

**High Score Means:**  
Data is reliable, well-governed, and trusted.
            """)

        # -----------------------------
        # KPI 7 — AIRS
        # -----------------------------
        with st.expander(" 7. AIRS — API & Integration Readiness Score", expanded=False):
            st.markdown("""
**Meaning:**  
Measures API maturity, integration readiness, and interoperability.

**Formula:**  
AIRS = AvgScore * 0.88

**High Score Means:**  
Product integrates cleanly with other systems.
            """)

        # -----------------------------
        # KPI 8 — TCKRS
        # -----------------------------
        with st.expander(" 8. TCKRS — Team Capability & Knowledge Risk Score", expanded=False):
            st.markdown("""
**Meaning:**  
Evaluates team skill, documentation quality, and knowledge concentration risk.

**Formula:**  
TCKRS = AvgScore * 0.75

**High Score Means:**  
Strong team capability and lower key-person risk.
            """)

        # -----------------------------
        # KPI 9 — MCE
        # -----------------------------
        with st.expander(" 9. MCE — Modernization Cost Estimate", expanded=False):
            st.markdown("""
**Meaning:**  
Predicts modernization cost based on technical debt and complexity.

**Formula:**  
MCE = 100 - AvgScore

**High Score Means:**  
Higher expected modernization cost.
            """)

        # -----------------------------
        # KPI 10 — SPS
        # -----------------------------
        with st.expander(" 10. SPS — Synergy Potential Score", expanded=False):
            st.markdown("""
**Meaning:**  
Measures how well the product aligns with enterprise ecosystem, roadmap, and strategy.

**Formula:**  
SPS = AvgScore * 0.95

**High Score Means:**  
High strategic fit and strong synergy with existing landscape.
            """)

    st.markdown("---")

    # ---------------------------------------------------------
    # ASSESSMENT TABLE
    # ---------------------------------------------------------
    db = get_db()
    assessments = Repository.get_all_assessments(db)

    if not assessments:
        st.info("No assessments found.")
        return

    rows = []
    for a in assessments:
        metrics = Repository.get_metrics(db, a.id)
        responses = Repository.get_responses_for_assessment(db, a.id)

        rows.append({
            "ID": a.id,
            "Product": a.product_name,
            "Version": a.version,
            "Assessed By": a.assessed_by,
            "Created": a.created_at,
            "Responses": len(responses),
            "ASS": metrics.ASS if metrics else None,
            "TDI": metrics.TDI if metrics else None,
            "SCS": metrics.SCS if metrics else None,
            "SCRS": metrics.SCRS if metrics else None,
            "ORS": metrics.ORS if metrics else None,
            "DQGS": metrics.DQGS if metrics else None,
            "AIRS": metrics.AIRS if metrics else None,
            "TCKRS": metrics.TCKRS if metrics else None,
            "MCE": metrics.MCE if metrics else None,
            "SPS": metrics.SPS if metrics else None,
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "assessments.csv",
        "text/csv",
    )


if __name__ == "__main__":
    main()