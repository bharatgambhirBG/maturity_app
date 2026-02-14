import streamlit as st
from data.repository import init_db

def main():
    st.set_page_config(page_title="Maturity Assessment", layout="wide")
    st.sidebar.title("Maturity Assessment App")
    st.sidebar.info("Use the pages on the left to navigate.")
    st.title("Welcome to the Maturity Assessment Portal")
    st.write("Use the pages to fill assessments and view admin reports.")

if __name__ == "__main__":
    init_db()
    main()