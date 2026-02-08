import streamlit as st

def run_dashboard(national_score, classification, regional_reports):

    st.set_page_config(layout="wide")
    st.title("Federal AI Governance Dashboard")

    st.metric("National Stability Index", national_score)
    st.subheader("National Classification")
    st.write(classification)

    st.divider()

    st.subheader("Regional Risk Overview")

    for r in regional_reports:
        st.write(f"{r['region']} -> Risk Score: {r['risk_score']}")
