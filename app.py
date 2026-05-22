import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala AI CAD", layout="wide")

st.title("🤖 SolidShala AI CAD Trainer - Level 6 (Ultimate AI System)")
st.write("Think → Ask AI → Build → Learn → Master Engineering")

# =========================
# STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = False

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# ENGINEERING DATABASE
# =========================
QUESTIONS = [
    {
        "q": "Crankshaft banane ke liye best initial shape?",
        "options": ["Circle", "Square", "Triangle"],
        "answer": "Circle",
        "stage": "sketch",
        "why": "Rotational parts always axis-based circular geometry use karte hain."
    },
    {
        "q": "Circle ko 3D shaft banane ka tool?",
        "options": ["Extrude", "Cut", "Pattern"],
        "answer": "Extrude",
        "stage": "extrude",
        "why": "Extrude 2D profile ko 3D solid banata hai."
    },
    {
        "q": "Material remove karne ka tool?",
        "options": ["Cut", "Fillet", "Scale"],
        "answer": "Cut",
        "stage": "cut",
        "why": "Cut subtractive manufacturing operation hai."
    },
    {
        "q": "Sharp edges smooth karne ke liye?",
        "options": ["Fillet", "Mirror", "Pattern"],
        "answer": "Fillet",
        "stage": "finish",
        "why": "Fillet stress concentration reduce karta hai."
    }
]

q = QUESTIONS[st.session_state.step % len(QUESTIONS)]

# =========================
# AI HINT ENGINE
# =========================
def ai_hint():
    st.info("🤖 AI Hint: Think about engineering function, not just shape.")

    if q["stage"] == "sketch":
        st.write("👉 Rotational objects = circle base")
    elif q["stage"] == "extrude":
        st.write("👉 2D to 3D conversion = height add")
    elif q["stage"] == "cut":
        st.write("👉 Removing material = subtractive process")
    elif q["stage"] == "finish":
        st.write("👉 Stress points = sharp edges → fillet")

# =========================
# MODEL ENGINE
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    # SKETCH
    if stage == "sketch":
        t = np.linspace(0, 2*np.pi, 80)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

    # EXTRUDE
    elif stage == "extrude":
        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 30)
        t, z = np.meshgrid(t, z)

        fig.add_trace(go.Surface(
            x=np.cos(t),
            y=np.sin(t),
            z=z,
            opacity=0.85
        ))

    # CUT
    elif stage == "cut":
        h2 = max(0.4, h - 0.5)

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h2,h2,h2,h2]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

    # FINISH
    elif stage == "finish":
        t = np.linspace(0, 2*np.pi, 60)
        z = np.linspace(0, h, 25)
        t, z = np.meshgrid(t, z)

        fig.add_trace(go.Surface(
            x=np.cos(t)*0.9,
            y=np.sin(t)*0.9,
            z=z,
            opacity=0.85
        ))

    fig.update_layout(height=520, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI
# =========================
st.subheader("🎯 Engineering Challenge")

st.info(q["q"])

choice = st.radio("Select Best CAD Decision", q["options"])

st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

# =========================
# BUTTONS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit Answer"):

        if choice == q["answer"]:
            st.success("✔ Correct Engineering Thinking")
            st.session_state.score += 1
            st.session_state.stage = q["stage"]
        else:
            st.error("❌ Wrong Thinking - Learn Concept")

        st.write("🧠 WHY:")
        st.write(q["why"])

        st.session_state.step += 1

with col2:
    if st.button("🤖 AI Hint"):
        ai_hint()

with col3:
    if st.button("🧠 AI Mode ON/OFF"):
        st.session_state.ai_mode = not st.session_state.ai_mode

# =========================
# MODEL VIEW
# =========================
st.subheader("📐 Live CAD Simulation")

st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# AI CHAT (SIMPLE SIMULATION)
# =========================
if st.session_state.ai_mode:

    st.subheader("🤖 AI CAD Tutor")

    user_q = st.text_input("Ask CAD question:")

    if user_q:

        if "extrude" in user_q.lower():
            st.write("Extrude = 2D → 3D conversion (height add)")
        elif "cut" in user_q.lower():
            st.write("Cut = material removal process")
        elif "fillet" in user_q.lower():
            st.write("Fillet = edge smoothing for stress reduction")
        else:
            st.write("Think in terms of geometry + function + manufacturing")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 AI Learning Dashboard")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)
st.sidebar.write("Stage:", st.session_state.stage)

if st.sidebar.button("Reset AI System"):
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
    st.session_state.ai_mode = False
