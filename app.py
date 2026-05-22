import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala Level 4", layout="wide")

st.title("🧠 SolidShala CAD Thinking Trainer - Level 4 (Ultimate)")
st.write("Think → Build → Correct → Learn (AI Guided CAD Training)")

# =========================
# STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "hint_used" not in st.session_state:
    st.session_state.hint_used = False

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# FULL ENGINE (CRANKSHAFT PROJECT)
# =========================
STEPS = [
    {
        "title": "Step 1: Design Start",
        "question": "Crankshaft banane ke liye best starting point?",
        "options": ["Circle Sketch", "Square Sketch", "Line"],
        "answer": "Circle Sketch",
        "stage": "sketch",
        "hint": "Rotational parts always circle se start hote hain (axis symmetry).",
        "explain": "Engine shaft rotational part hota hai, is liye circle base hota hai."
    },
    {
        "title": "Step 2: 3D Conversion",
        "question": "Circle ko cylinder banane ke liye kaunsa tool?",
        "options": ["Extrude", "Cut", "Mirror"],
        "answer": "Extrude",
        "stage": "extrude",
        "hint": "2D → 3D conversion ke liye height add hoti hai.",
        "explain": "Extrude 2D sketch ko 3D solid banata hai."
    },
    {
        "title": "Step 3: Material Removal",
        "question": "Shaft me groove banani ho to?",
        "options": ["Cut", "Scale", "Pattern"],
        "answer": "Cut",
        "stage": "cut",
        "hint": "Material remove karna = subtractive operation.",
        "explain": "Cut machining operation hai jo material remove karta hai."
    },
    {
        "title": "Step 4: Engineering Finish",
        "question": "Stress reduce aur smooth edges ke liye?",
        "options": ["Chamfer", "Fillet", "Extrude"],
        "answer": "Fillet",
        "stage": "fillet",
        "hint": "Sharp edges = stress concentration, smooth = fillet.",
        "explain": "Fillet edges ko smooth karta hai aur failure reduce karta hai."
    }
]

q = STEPS[st.session_state.step % len(STEPS)]

# =========================
# AI HINT SYSTEM
# =========================
def show_hint():
    st.warning("💡 Hint: " + q["hint"])
    st.session_state.hint_used = True

# =========================
# MODEL RENDER ENGINE
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    # ---------------- SKETCH ----------------
    if stage == "sketch":

        t = np.linspace(0, 2*np.pi, 60)
        x = np.cos(t)
        y = np.sin(t)
        z = np.zeros_like(t)

        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines"))

    # ---------------- EXTRUDE ----------------
    elif stage == "extrude":

        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 25)

        t, z = np.meshgrid(t, z)

        x = np.cos(t)
        y = np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.85))

    # ---------------- CUT ----------------
    elif stage == "cut":

        h2 = max(0.4, h - 0.4)

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h2,h2,h2,h2]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

    # ---------------- FILLET ----------------
    elif stage == "fillet":

        t = np.linspace(0, 2*np.pi, 60)
        z = np.linspace(0, h, 25)

        t, z = np.meshgrid(t, z)

        x = np.cos(t) * 0.9
        y = np.sin(t) * 0.9

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.85))

    fig.update_layout(height=520, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI
# =========================
st.subheader(q["title"])
st.info(q["question"])

choice = st.radio("Select Best CAD Thinking", q["options"])

# =========================
# HEIGHT CONTROL
# =========================
st.slider("Model Size (Engineering Scale)", 1.0, 5.0, 1.0, key="height")

# =========================
# ACTIONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Answer"):

        if choice == q["answer"]:
            st.success("✔ Correct Engineering Thinking!")
            st.session_state.score += 1
            st.session_state.stage = q["stage"]
        else:
            st.error("❌ Wrong CAD Thinking — Try Understanding Concept")

        st.write("🧠 Explanation:")
        st.write(q["explain"])

        st.session_state.step += 1
        st.session_state.hint_used = False

with col2:
    if st.button("💡 Get Hint"):
        show_hint()

# =========================
# LIVE MODEL
# =========================
st.subheader("📐 Live CAD Simulation")

st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Progress Tracker")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)
st.sidebar.write("Current Stage:", st.session_state.stage)

if st.sidebar.button("Reset Full System"):
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
    st.session_state.hint_used = False
