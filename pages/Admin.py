import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from data.db import SessionLocal
from data.repository import get_all_assessments

def get_db_session() -> Session:
    return SessionLocal()

def main():
    st.title("Admin Dashboard")

    db = get_db_session()
    assessments = get_all_assessments(db)

    if not assessments:
        st.info("No assessments submitted yet.")
        return

    data = [
        {
            "ID": a.id,
            "User": a.user_name,
            "Org": a.org,
            "Score": a.overall_score,
            "Level": a.maturity_level,
            "Created": a.created_at,
        }
        for a in assessments
    ]
    df = pd.DataFrame(data)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "assessments.csv", "text/csv")

if __name__ == "__main__":
    main()