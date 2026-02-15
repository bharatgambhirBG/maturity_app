import streamlit as st
from data.db import SessionLocal
from data.question_loader import load_question_model
from services.assessment_service import AssessmentService
from services.scoring_service import ScoringService

st.set_page_config(layout="wide", page_title="Maturity Assessment")

QUESTION_MODEL = load_question_model("config/questions.json")


# -----------------------------
# Session State Initialization
# -----------------------------
if "selected_domain_id" not in st.session_state:
    st.session_state.selected_domain_id = QUESTION_MODEL["domains"][0]["id"]

if "selected_subdomain_id" not in st.session_state:
    st.session_state.selected_subdomain_id = QUESTION_MODEL["domains"][0]["subdomains"][0]["id"]

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "assessment_id" not in st.session_state:
    st.session_state.assessment_id = None

if "question_map" not in st.session_state:
    st.session_state.question_map = {}


def get_db():
    return SessionLocal()


def get_domain(domain_id):
    return next(d for d in QUESTION_MODEL["domains"] if d["id"] == domain_id)


def get_subdomain(domain, subdomain_id):
    return next(sd for sd in domain["subdomains"] if sd["id"] == subdomain_id)


# -----------------------------
# Header
# -----------------------------
st.title("Enterprise Maturity Assessment")

with st.expander("Start / Identify Assessment", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        product_name = st.text_input("Product Name")
    with c2:
        version = st.text_input("Version / Release")
    with c3:
        assessor = st.text_input("Assessed By")

    if st.button("Initialize Assessment", key="btn_init_assessment", type="primary"):
        if not product_name or not assessor:
            st.error("Product name and assessor are required.")
        else:
            session = get_db()
            assessment, question_map = AssessmentService.initialize_assessment(
                session=session,
                product_name=product_name,
                version=version,
                assessed_by=assessor,
                question_model=QUESTION_MODEL,
            )
            st.session_state.assessment_id = assessment.id
            st.session_state.question_map = question_map
            st.success(f"Assessment initialized (ID: {assessment.id})")


# -----------------------------
# Layout
# -----------------------------
col_left, col_right = st.columns([1, 3])

# -----------------------------
# LEFT PANEL — Domain & Subdomain Navigation
# -----------------------------
with col_left:
    st.markdown("### Domains")

    for d in QUESTION_MODEL["domains"]:
        is_selected = (d["id"] == st.session_state.selected_domain_id)

        if st.button(
            d["name"],
            key=f"domain_btn_{d['id']}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_domain_id = d["id"]
            st.session_state.selected_subdomain_id = d["subdomains"][0]["id"]
            st.rerun()

    domain = get_domain(st.session_state.selected_domain_id)

    st.markdown("---")
    st.markdown("### Sub-domains")

    for sd in domain["subdomains"]:
        is_selected = (sd["id"] == st.session_state.selected_subdomain_id)

        if st.button(
            f"• {sd['name']}",
            key=f"subdomain_btn_{sd['id']}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_subdomain_id = sd["id"]
            st.rerun()


# -----------------------------
# RIGHT PANEL — Questions
# -----------------------------
with col_right:
    domain = get_domain(st.session_state.selected_domain_id)
    subdomain = get_subdomain(domain, st.session_state.selected_subdomain_id)

    st.markdown(f"## {domain['name']}")
    st.caption(domain.get("description", ""))

    st.markdown(f"### {subdomain['name']}")

    for q in subdomain["questions"]:
        qid = q["id"]
        base_key = f"{domain['id']}_{subdomain['id']}_{qid}"

        st.markdown(f"#### {q['text']}")
        with st.expander("Why this is important"):
            st.write(q.get("help", ""))
        
        # NEW: Show KPI impact
        if "kpi" in q:
            st.markdown(f"**Impacts KPIs:** {', '.join(q['kpi'])}")


        maturity = st.slider(
            "Maturity (1–10)",
            1, 10, 5,
            key=f"{base_key}_maturity",
        )

        criticality = st.slider(
            "Criticality (1–5)",
            1, 5, 3,
            key=f"{base_key}_criticality",
        )

        risk_exposure = st.selectbox(
            "Risk exposure",
            ["Low", "Medium", "High"],
            key=f"{base_key}_risk",
        )

        remediation_effort = st.selectbox(
            "Remediation effort",
            ["Low", "Medium", "High"],
            key=f"{base_key}_effort",
        )

        confidence = st.selectbox(
            "Confidence level",
            ["Low", "Medium", "High"],
            key=f"{base_key}_confidence",
        )

        notes = st.text_area(
            "Notes / observations",
            key=f"{base_key}_notes",
        )

        uploaded_files = st.file_uploader(
            "Upload evidence (optional)",
            type=["pdf", "docx", "xlsx", "pptx", "png", "jpg"],
            accept_multiple_files=True,
            key=f"{base_key}_files",
        )

        st.session_state.responses[qid] = {
            "question_db_id": st.session_state.question_map.get(qid),
            "maturity": maturity,
            "criticality": criticality,
            "risk_exposure": risk_exposure,
            "remediation_effort": remediation_effort,
            "confidence": confidence,
            "notes": notes,
            "files": uploaded_files,
        }

        st.markdown("---")

    if st.button("Save & Compute KPIs", key="btn_save_responses", type="primary"):
        if not st.session_state.assessment_id:
            st.error("Please initialize the assessment first.")
        else:
            session = get_db()
            AssessmentService.save_responses(
                session=session,
                assessment_id=st.session_state.assessment_id,
                responses=st.session_state.responses,
            )
            ScoringService.compute_and_store_metrics(
                session=session,
                assessment_id=st.session_state.assessment_id,
            )
            st.success("Responses saved and KPIs computed.")

    with st.expander("Debug: Current Captured Data"):
        st.json(st.session_state.responses)