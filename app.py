import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala Level 2", layout="wide")

st.title("🧠 SolidShala CAD Thinking Trainer - Level 2")
st.write("Learn WHY + SEE + DO (Thinking + Visualization)")

# =========================
# STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "step" not in st.session_state:
    st.session_state.step = 0

if "shape" not in st.session_state:
    st.session_state.shape = None

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# LESSONS (LEVEL 2)
# =========================
LESSONS = [
    {
        "question": "Crankshaft (rotating part) banana hai — best tool?",
        "options": ["Extrude", "Revolve", "Cut"],
        "answer": "Revolve",
        "explain": "Rotational parts revolve se bante hain, kyun ke shape axis ke around rotate hota hai.",
        "model": "revolve"
    },
    {
        "question": "Solid block me hole banana hai?",
        "options": ["Cut", "Extrude", "Scale"],
        "answer": "Cut",
        "explain": "Cut material remove karta hai (subtractive manufacturing).",
        "model": "cut"
    },
    {
        "question": "Cylinder banana ho 2D circle se?",
        "options": ["Extrude", "Chamfer", "Mirror"],
        "answer": "Extrude",
        "explain": "Extrude 2D sketch ko 3D solid banata hai.",
        "model": "extrude"
    }
]

q = LESSONS[st.session_state.step % len(LESSONS)]

# =========================
# SIMPLE 3D MODEL ENGINE
# =========================
def render_model(model_type):

    fig = go.Figure()

    if model_type == "revolve":
        # cylinder (revolve feel)
        r = 1
        h = st.session_state.height

        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 20)

        t, z = np.meshgrid(t, z)

        x = r * np.cos(t)
        y = r * np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.85))

    elif model_type == "extrude":
        # box extrude
        s = 1
        h = st.session_state.height

        x = [0, s, s, 0, 0, s, s, 0]
        y = [0, 0, s, s, 0, 0, s, s]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

    elif model_type == "cut":
        # block with reduced height (cut effect)
        s = 1
        h = max(0.4, st.session_state.height - 0.4)

        x = [0, s, s, 0, 0, s, s, 0]
        y = [0, 0, s, s, 0, 0, s, s]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.7))

    fig.update_layout(height=500, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI
# =========================
st.subheader("🎯 Challenge")

st.info(q["question"])

choice = st.radio("Select Tool", q["options"])

# =========================
# HEIGHT CONTROL (VISUAL UNDERSTANDING)
# =========================
st.slider("Model Size (Height Control)", 1.0, 5.0, 1.0, key="height")

# =========================
# SUBMIT
# =========================
if st.button("Submit Answer"):

    if choice == q["answer"]:
        st.success("✔ Correct Thinking!")
        st.session_state.score += 1
    else:
        st.error("❌ Wrong Thinking")

    st.write("🧠 Why?")
    st.write(q["explain"])

    st.session_state.step += 1

# =========================
# MODEL PREVIEW (IMPORTANT LEVEL 2 FEATURE)
# =========================
st.subheader("📐 Live Model Preview")

st.plotly_chart(render_model(q["model"]), use_container_width=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Progress")
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)

if st.sidebar.button("Reset"):
    st.session_state.score = 0
    st.session_state.step = 0
    st.session_state.height = 1.0
