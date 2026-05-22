import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="SolidShala Learning System", layout="wide")

st.title("🧠 SolidShala CAD Thinking Trainer")
st.write("Learn WHY tools are used, not just HOW")

# =========================
# SESSION STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "step" not in st.session_state:
    st.session_state.step = 0

# =========================
# LESSON DATABASE
# =========================
LESSONS = [
    {
        "question": "Crankshaft jaisa rotating part banana hai, best tool?",
        "options": ["Extrude", "Revolve", "Cut"],
        "answer": "Revolve",
        "explain": "Rotational parts revolve se bante hain, extrude flat shape banata hai."
    },
    {
        "question": "Hole banana ho solid block me, kaunsa tool?",
        "options": ["Cut", "Shell", "Scale"],
        "answer": "Cut",
        "explain": "Cut material remove karta hai."
    },
    {
        "question": "2D circle ko 3D cylinder banana ho?",
        "options": ["Extrude", "Chamfer", "Mirror"],
        "answer": "Extrude",
        "explain": "Extrude 2D ko 3D banata hai."
    },
    {
        "question": "Edge ko smooth banana ho?",
        "options": ["Chamfer", "Fillet", "Pattern"],
        "answer": "Fillet",
        "explain": "Fillet edges ko round smooth karta hai."
    }
]

# =========================
# CURRENT QUESTION
# =========================
q = LESSONS[st.session_state.step % len(LESSONS)]

st.subheader("🎯 Challenge Question")

st.info(q["question"])

choice = st.radio("Select Tool", q["options"])

# =========================
# CHECK ANSWER
# =========================
if st.button("Submit Answer"):

    if choice == q["answer"]:
        st.success("✔ Correct Thinking!")
        st.session_state.score += 1
    else:
        st.error("❌ Wrong Thinking")

    st.write("🧠 Explanation:")
    st.write(q["explain"])

    st.session_state.step += 1

# =========================
# SCORE PANEL
# =========================
st.sidebar.title("📊 Progress")
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Level Step:", st.session_state.step)

# =========================
# RESET
# =========================
if st.sidebar.button("Reset"):
    st.session_state.score = 0
    st.session_state.step = 0
