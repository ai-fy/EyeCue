import streamlit as st

def show():
    st.markdown("### Research Agend for EyeCue")

    company_name = st.text_input("Company Name", "LabLab.ai")

    if st.button("Start research"):
        st.write("Starting research for "+ company_name)