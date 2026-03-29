import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
from orchestration.graph import graph

st.title(" Autonomous Deal Risk & Recovery AI")

deal_id = st.selectbox("Select Deal", ["D001", "D002"])

if st.button("Run AI Pipeline"):
    initial_state = {
        "deal_id": deal_id,
        "raw_data": {},
        "signals": {},
        "risk": {},
        "strategy": {},
        "actions": {},
        "feedback": {},
        "logs": []
    }

    result = graph.invoke(initial_state)

    st.success("Pipeline executed successfully!")

    # SHOW OUTPUTS

    st.subheader(" Risk Analysis")
    st.json(result.get("risk"))

    st.subheader(" Strategy")
    st.json(result.get("strategy"))

    st.subheader(" Actions")
    st.json(result.get("actions"))

    st.subheader(" Feedback")
    st.json(result.get("feedback"))

    st.subheader(" Logs")
    st.write(result.get("logs"))