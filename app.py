import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala Level 3", layout="wide")

st.title("🧠 SolidShala CAD Thinking Trainer - Level 3")
st.write("Learn → Decide → Build (Step-by-step Engineering)")

# =========================
# STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "height" not in st.session_state:
    st.session_state.height = 1.0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

# =========================
# PROJECT (CRANKSHAFT MINI MODEL)
# =========================
STEPS = [
    {
        "title": "Step 1: Base Sketch",
        "question": "Crankshaft jaisi part ke liye base shape kya hogi?",
        "options": ["Circle Sketch", "Square Sketch", "Triangle"],
        "answer": "Circle Sketch",
        "tool": "sketch_circle",
        "explain": "Rotational parts always circle sketch se start hote hain."
    },
    {
        "title": "Step 2: 3D Formation",
        "question": "Circle ko 3D cylinder banane ke liye?",
        "options": ["Extrude", "Cut", "Mirror"],
        "answer": "Extrude",
        "tool": "extrude",
        "explain": "Extrude 2D circle ko cylinder banata hai."
    },
    {
        "title": "Step 3: Shape Modification",
        "question": "Shaft me material remove karna ho?",
        "options": ["Cut", "Scale", "Pattern"],
        "answer": "Cut",
        "tool": "cut",
        "explain": "Cut machining operation hai jo material remove karta hai."
    },
    {
        "title": "Step 4: Engineering Finish",
        "question": "Sharp edges ko smooth karne ke liye?",
        "options": ["Chamfer", "Fillet", "Extrude"],
        "answer": "Fillet",
        "tool": "fillet",
        "explain": "Fillet stress reduce karta hai aur smooth edge deta hai."
    }
]

step_data = STEPS[st.session_state.step % len(STEPS)]

# =========================
# SIMPLE MODEL STATE
# =========================
def build_model():

    fig = go.Figure()

    stage = st.session_state.stage
    h = st.session_state.height

    # ------------------
    # SKETCH
    # ------------------
    if stage == "sketch_circle":
        t = np.linspace(0, 2*np.pi, 50)
        x = np.cos(t)
        y = np.sin(t)
        z = np.zeros_like(t)

        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines"))

    # ------------------
    # EXTRUDE
    # ------------------
    elif stage == "extrude":

        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 20)

        t, z = np.meshgrid(t, z)

        x = np.cos(t)
        y = np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.85))

    # ------------------
    # CUT (visual safe)
    # ------------------
    elif stage == "cut":

        h2 = max(0.4, h - 0.4)

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h2,h2,h2,h2]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

    # ------------------
    # FILLET (visual smooth hint)
    # ------------------
    elif stage == "fillet":

        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 20)

        t, z = np.meshgrid(t, z)

        x = np.cos(t) * 0.9
        y = np.sin(t) * 0.9

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.8))

    fig.update_layout(height=500, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI
# =========================
st.subheader(step_data["title"])

st.info(step_data["question"])

choice = st.radio("Select Correct CAD Tool / Thinking", step_data["options"])

# =========================
# HEIGHT CONTROL
# =========================
st.slider("Model Size Control", 1.0, 5.0, 1.0, key="height")

# =========================
# SUBMIT STEP
# =========================
if st.button("Submit Step"):

    if choice == step_data["answer"]:
        st.success("✔ Correct Engineering Thinking!")
        st.session_state.score += 1
        st.session_state.stage = step_data["tool"]
    else:
        st.error("❌ Wrong CAD Thinking")

    st.write("🧠 Explanation:")
    st.write(step_data["explain"])

    st.session_state.step += 1

# =========================
# MODEL VIEW
# =========================
st.subheader("📐 Live CAD Build View")

st.plotly_chart(build_model(), use_container_width=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Progress")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)

if st.sidebar.button("Reset"):
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
