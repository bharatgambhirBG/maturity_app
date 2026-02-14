import streamlit as st
from sqlalchemy.orm import Session
from data.db import SessionLocal
from services.assessment_service import process_and_save_assessment

QUESTIONS = [
    {"dimension": "People", "question": "Do you have defined roles & responsibilities?"},
    {"dimension": "Process", "question": "Are core processes documented?"},
    {"dimension": "Technology", "question": "Are tools standardized across teams?"},
    {"dimension": "Governance", "question": "Is there a regular review mechanism?"},
]

def get_db_session() -> Session:
    return SessionLocal()

def main():
    st.title("Maturity Assessment")

    user_name = st.text_input("Your Name")
    org = st.text_input("Organization / Team")

    st.subheader("Answer the following (1 = Low, 5 = High):")
    answers = []
    for q in QUESTIONS:
        val = st.slider(q["question"], 1, 5, 3)
        answers.append(
            {
                "dimension": q["dimension"],
                "question": q["question"],
                "answer": val,
            }
        )

    if st.button("Submit Assessment"):
        if not user_name or not org:
            st.error("Please fill your name and organization.")
            return

        db = get_db_session()
        assessment, scoring = process_and_save_assessment(
            db=db,
            user_name=user_name,
            org=org,
            answers=answers,
        )
        st.success("Assessment submitted successfully!")
        st.write(f"Overall Score: **{scoring['overall_score']}**")
        st.write(f"Maturity Level: **{scoring['maturity_level']}**")

if __name__ == "__main__":
    main()