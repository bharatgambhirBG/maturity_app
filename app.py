import streamlit as st
#from data.repository import init_db
from data.db import Base, engine
Base.metadata.create_all(bind=engine)

def main():
    # st.set_page_config(page_title="Maturity Assessment", layout="wide")
    st.set_page_config(layout="wide")
    st.sidebar.title("Maturity Assessment App")
    st.sidebar.info("Use the pages on the left to navigate.")
    st.title("Welcome to the Product Maturity Assessment Portal")
    st.write("Use the pages to fill assessments and view admin reports.")
    st.write("For defination of KPI, see admin page.")
    st.write("Regards,Bharat")

if __name__ == "__main__":
    #init_db()
    main()