import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from orchestration.engine import run_agents

st.set_page_config(page_title="Autonomous Deal AI", layout="wide")

st.title("🤖 Autonomous Deal Risk & Recovery AI")

# 🔥 MODE
mode = st.selectbox("Mode", ["manual", "autonomous"])

# 🔥 DEAL (manual only)
if mode == "manual":
    deal_id = st.selectbox("Select Deal", ["D001","D002", "D003", "D004", "D005"])
else:
    deal_id = None

# 🔥 NATURAL LANGUAGE INPUT
user_prompt = st.text_input(
    "What do you want the system to do?",
    placeholder="e.g., assess risk, recover this deal, run full autonomous recovery"
)

# 🔥 RUN
if st.button("Run AI"):

    st.info("Running AI system...")

    initial_state = {
        "deal_id": deal_id,
        "user_goal": user_prompt,
        "raw_data": {},
        "signals": {},
        "risk": {},
        "strategy": {},
        "actions": {},
        "feedback": {},
        "logs": []
    }

    result = run_agents(initial_state)

    st.success("Execution Started ✅")

    logs = result.get("logs", [])

    # 🔥 STREAMING PLACEHOLDERS
    selection_box = st.empty()
    risk_box = st.empty()
    strategy_box = st.empty()
    action_box = st.empty()
    feedback_box = st.empty()

    # ---------------------------------------
    # 📌 MANUAL DEAL DISPLAY
    # ---------------------------------------
    if deal_id:
        selection_box.markdown(
            f"""
### 📌 Deal Selected

**Deal ID:** {deal_id} (Manual)
"""
        )

    # ---------------------------------------
    # 🔄 STREAM EXECUTION
    # ---------------------------------------
    for log in logs:
        time.sleep(0.25)

        # 📌 DEAL SELECTION
        if "Portfolio selected" in log:
            selected_deal = result.get("deal_id")

            selection_box.markdown(
                f"""
### 📌 Deal Selected

**Deal ID:** {selected_deal}
"""
            )

        if "Reason:" in log:
            selection_box.markdown(f"🧠 {log}")

        # 📊 RISK
        if "Risk Score" in log:
            risk = result.get("risk", {})

            factors_text = "\n".join(
                [f"- {f}" for f in risk.get("factors", [])]
            )

            risk_box.markdown(
                f"""
### 📊 Risk Assessment

**Score:** {risk.get("risk_score")}  
**Confidence:** {risk.get("confidence")}

**Factors:**
{factors_text}

**Reasoning:**
{risk.get("reasoning")}
"""
            )

        # 🧠 STRATEGY
        if "Strategy agent executed" in log:
            strategy = result.get("strategy", {})

            rc_text = "\n".join(
                [f"- {rc}" for rc in strategy.get("root_causes", [])]
            )

            strategy_box.markdown(
                f"""
### 🧠 Strategy Generated

**Summary:**  
{strategy.get("summary")}

**Root Causes:**
{rc_text}
"""
            )

        # ⚡ ACTIONS
        if "Execution agent executed" in log:
            actions = result.get("actions", {})
            content = actions.get("generated_content", {})

            email = content.get("email_primary", {})

            if email:
                action_box.markdown(
                    f"""
### ⚡ Action Executed

📧 **Email Sent**

**Subject:** {email.get("subject")}

{email.get("body")}
"""
                )

        # 🔁 FEEDBACK
        if "Feedback agent simulated outcome" in log:
            feedback = result.get("feedback", {})

            feedback_box.markdown(
                f"""
### 🔁 Feedback Loop

**Outcome:** {feedback.get("outcome")}
"""
            )

    # =======================================
    # 🔥 FINAL STRUCTURED OUTPUT
    # =======================================
    st.divider()
    st.header("📦 Final AI Output Summary")

    # 📌 DEAL
    st.subheader("📌 Deal")
    st.write("Selected Deal:", result.get("deal_id"))

    # 📊 RISK
    st.subheader("📊 Risk")
    risk = result.get("risk", {})

    st.write("Score:", risk.get("risk_score"))
    st.write("Confidence:", risk.get("confidence"))

    st.write("Factors:")
    for f in risk.get("factors", []):
        st.write("-", f)

    st.write("Reasoning:")
    st.write(risk.get("reasoning"))

    # 🧠 STRATEGY
    if result.get("strategy"):
        st.subheader("🧠 Strategy")

        strategy = result.get("strategy", {})

        st.write("Root Causes:")
        for rc in strategy.get("root_causes", []):
            st.write("-", rc)

        st.write("Summary:")
        st.write(strategy.get("summary"))

    # ⚡ ACTIONS
    if result.get("actions"):
        st.subheader("⚡ Actions")

        actions = result.get("actions", {})
        content = actions.get("generated_content", {})

        email = content.get("email_primary", {})
        if email:
            st.write("📧 Email Subject:", email.get("subject"))
            st.code(email.get("body"), language="markdown")

        if content.get("call_script"):
            st.write("📞 Call Script:")
            st.write(content.get("call_script"))

    # 🔁 FEEDBACK
    if result.get("feedback"):
        st.subheader("🔁 Feedback")

        feedback = result.get("feedback", {})
        st.write("Outcome:", feedback.get("outcome"))
        st.write("Learning:", feedback.get("learning"))

    # 📜 LOGS
    with st.expander("📜 Full Execution Logs"):
        for log in logs:
            st.write("•", log)