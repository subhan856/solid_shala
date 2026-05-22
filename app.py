import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala Level 5", layout="wide")

st.title("🧠 SolidShala CAD Master Trainer - Level 5 (Final Pro)")
st.write("Build → Think → Assemble → Learn (Engineering Game Mode)")

# =========================
# STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "hints" not in st.session_state:
    st.session_state.hints = 0

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# FULL ENGINE PROJECT (ENGINE BUILD)
# =========================
STEPS = [
    {
        "title": "Step 1: Crankshaft Design Start",
        "question": "Crankshaft ka base design kis shape se start hota hai?",
        "options": ["Circle Sketch", "Square Sketch", "Line"],
        "answer": "Circle Sketch",
        "stage": "sketch",
        "hint": "Rotational parts always axis-based hote hain.",
        "explain": "Engine shaft circular symmetry use karta hai."
    },
    {
        "title": "Step 2: Shaft Formation",
        "question": "Circle ko shaft banane ke liye?",
        "options": ["Extrude", "Cut", "Mirror"],
        "answer": "Extrude",
        "stage": "shaft",
        "hint": "2D sketch ko 3D banana hota hai.",
        "explain": "Extrude cylinder banata hai."
    },
    {
        "title": "Step 3: Crank Offset",
        "question": "Offset/arm create karne ke liye best tool?",
        "options": ["Cut", "Extrude", "Chamfer"],
        "answer": "Cut",
        "stage": "offset",
        "hint": "Material remove karke shape change hoti hai.",
        "explain": "Cut se crank offset create hota hai."
    },
    {
        "title": "Step 4: Stress Reduction",
        "question": "Edges smooth karne ke liye?",
        "options": ["Fillet", "Pattern", "Scale"],
        "answer": "Fillet",
        "stage": "finish",
        "hint": "Sharp edges = stress concentration.",
        "explain": "Fillet stress reduce karta hai."
    },
    {
        "title": "Step 5: Final Assembly Thinking",
        "question": "Multiple parts ko repeat karne ke liye?",
        "options": ["Pattern", "Extrude", "Cut"],
        "answer": "Pattern",
        "stage": "assembly",
        "hint": "Repeating structures = pattern.",
        "explain": "Pattern assembly replication ke liye use hota hai."
    }
]

q = STEPS[st.session_state.step % len(STEPS)]

# =========================
# AI HINT SYSTEM
# =========================
def show_hint():
    st.warning("💡 Hint: " + q["hint"])
    st.session_state.hints += 1

# =========================
# CAD RENDER ENGINE
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    # ---------------- SKETCH ----------------
    if stage == "sketch":
        t = np.linspace(0, 2*np.pi, 60)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

    # ---------------- SHAFT ----------------
    elif stage == "shaft":

        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 25)

        t, z = np.meshgrid(t, z)

        fig.add_trace(go.Surface(
            x=np.cos(t),
            y=np.sin(t),
            z=z,
            opacity=0.85
        ))

    # ---------------- OFFSET ----------------
    elif stage == "offset":

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h,h,h,h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

        # crank arm visualization
        fig.add_trace(go.Scatter3d(
            x=[0,1],
            y=[0,0.5],
            z=[h,h+0.5],
            mode="lines"
        ))

    # ---------------- FINISH ----------------
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

    # ---------------- ASSEMBLY ----------------
    elif stage == "assembly":

        for i in range(3):
            t = np.linspace(0, 2*np.pi, 40)
            z = np.linspace(0, h, 20)

            t, z = np.meshgrid(t, z)

            fig.add_trace(go.Surface(
                x=np.cos(t) + i*2,
                y=np.sin(t),
                z=z,
                opacity=0.5
            ))

    fig.update_layout(height=520, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI
# =========================
st.subheader(q["title"])
st.info(q["question"])

choice = st.radio("Select Engineering Decision", q["options"])

st.slider("Scale Control (Engineering Size)", 1.0, 5.0, 1.0, key="height")

# =========================
# ACTIONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Step"):

        if choice == q["answer"]:
            st.success("✔ Correct Engineering Decision")
            st.session_state.score += 1
            st.session_state.stage = q["stage"]
        else:
            st.error("❌ Wrong Thinking - Learn Concept")

        st.write("🧠 Why?")
        st.write(q["explain"])

        st.session_state.step += 1

with col2:
    if st.button("💡 Hint"):
        show_hint()

# =========================
# LIVE MODEL
# =========================
st.subheader("📐 Live Engine Build Simulation")

st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Learning Dashboard")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)
st.sidebar.write("Hints Used:", st.session_state.hints)
st.sidebar.write("Current Stage:", st.session_state.stage)

if st.sidebar.button("Reset System"):
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.stage = "start"
    st.session_state.hints = 0
    st.session_state.height = 1.0
