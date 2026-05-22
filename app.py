import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala PRO CAD", layout="wide")

st.title("🏭 SolidShala PRO CAD Learning Platform")
st.write("Real Engineering Thinking + Sketch + Build + Exam System")

# =========================
# STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "step" not in st.session_state:
    st.session_state.step = 0

if "stage" not in st.session_state:
    st.session_state.stage = "canvas"

if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = False

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# ENGINEERING TASKS
# =========================
TASKS = [
    {
        "q": "Rotational shaft design ke liye best sketch?",
        "options": ["Circle", "Square", "Line"],
        "answer": "Circle",
        "stage": "sketch",
        "why": "Rotation = axis symmetry → circle base"
    },
    {
        "q": "Circle ko 3D shaft banane ke liye?",
        "options": ["Extrude", "Cut", "Pattern"],
        "answer": "Extrude",
        "stage": "extrude",
        "why": "Extrude 2D profile ko 3D solid banata hai"
    },
    {
        "q": "Material remove karne ka process?",
        "options": ["Cut", "Fillet", "Scale"],
        "answer": "Cut",
        "stage": "cut",
        "why": "Cut subtractive manufacturing hai"
    },
    {
        "q": "Sharp edge ko safe banane ke liye?",
        "options": ["Fillet", "Mirror", "Extrude"],
        "answer": "Fillet",
        "stage": "finish",
        "why": "Fillet stress concentration reduce karta hai"
    }
]

q = TASKS[st.session_state.step % len(TASKS)]

# =========================
# SIMPLE CANVAS SIMULATION
# =========================
def sketch_canvas():

    st.subheader("✏️ Sketch Canvas (Simulated)")

    x = st.slider("X Shape Control", 0.0, 10.0, 5.0)
    y = st.slider("Y Shape Control", 0.0, 10.0, 5.0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, x, x, 0, 0],
        y=[0, 0, y, y, 0],
        mode="lines+markers"
    ))

    fig.update_layout(height=400)

    return fig

# =========================
# CAD MODEL ENGINE
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    if stage == "sketch":

        t = np.linspace(0, 2*np.pi, 80)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

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

    elif stage == "cut":

        h2 = max(0.4, h - 0.5)

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h2,h2,h2,h2]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

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

    fig.update_layout(height=500, scene=dict(aspectmode="data"))
    return fig

# =========================
# UI MODE
# =========================
st.sidebar.title("🎮 Mode")

mode = st.sidebar.radio("Select Mode", ["Learning Mode", "Exam Mode"])

# =========================
# EXAM MODE
# =========================
if mode == "Exam Mode":

    st.header("📝 CAD Exam Mode")

    st.info(q["q"])

    choice = st.radio("Answer", q["options"])

    if st.button("Submit Exam Answer"):

        if choice == q["answer"]:
            st.success("✔ Correct")
            st.session_state.score += 1
            st.session_state.stage = q["stage"]
        else:
            st.error("❌ Wrong")

        st.write("🧠 Reason:")
        st.write(q["why"])

        st.session_state.step += 1

    st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

    st.subheader("📐 Model View")
    st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# LEARNING MODE
# =========================
else:

    st.header("📘 Learning Mode")

    st.info(q["q"])

    st.write("Select Tool Thinking:")

    choice = st.radio("Tool", q["options"])

    if st.button("Learn"):

        if choice == q["answer"]:
            st.success("✔ Correct Thinking")
            st.session_state.stage = q["stage"]
        else:
            st.error("❌ Wrong Thinking")

        st.write("🧠 Explanation:")
        st.write(q["why"])

        st.session_state.step += 1

    st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✏️ Sketch Canvas")
        st.plotly_chart(sketch_canvas(), use_container_width=True)

    with col2:
        st.subheader("📐 CAD Model View")
        st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# DASHBOARD
# =========================
st.sidebar.write("📊 Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)
st.sidebar.write("Stage:", st.session_state.stage)

if st.sidebar.button("Reset All"):
    st.session_state.score = 0
    st.session_state.step = 0
    st.session_state.stage = "canvas"
    st.session_state.height = 1.0
