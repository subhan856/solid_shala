import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala Industry CAD LMS", layout="wide")

st.title("🏭 SolidShala Industry CAD Learning System")
st.write("Professional Engineering Training Platform (Stable + Scalable)")

# =========================
# SAFE STATE MANAGEMENT
# =========================
for key, val in {
    "score": 0,
    "tool_index": 0,
    "stage": "start",
    "height": 1.0,
    "mode": "Learn"
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# =========================
# TOOL ENGINE (200 SAFE TOOLS)
# =========================
BASE_TOOLS = [
    ("Extrude", "create", "2D to 3D conversion"),
    ("Revolve", "create", "Rotational geometry"),
    ("Cut", "modify", "Material removal"),
    ("Fillet", "finish", "Edge smoothing"),
    ("Chamfer", "finish", "Angular edge"),
    ("Shell", "modify", "Hollow body"),
    ("Pattern", "copy", "Repeat feature"),
    ("Mirror", "copy", "Symmetry"),
]

TOOLS = [
    {
        "name": f"{random.choice(BASE_TOOLS)[0]}_{i}",
        "type": random.choice(BASE_TOOLS)[1],
        "why": random.choice(BASE_TOOLS)[2]
    }
    for i in range(200)
]

tool = TOOLS[st.session_state.tool_index % 200]

# =========================
# QUESTION ENGINE
# =========================
def generate_question(tool):

    name = tool["name"]

    if "Extrude" in name:
        return "2D sketch ko 3D banane ke liye?", ["Extrude", "Cut", "Mirror"], "Extrude"

    if "Cut" in name:
        return "Material remove karne ke liye tool?", ["Cut", "Fillet", "Pattern"], "Cut"

    if "Revolve" in name:
        return "Rotational part ke liye?", ["Revolve", "Extrude", "Scale"], "Revolve"

    return "Tool category kya hai?", ["Create", "Modify", "Finish"], tool["type"].capitalize()

q, options, answer = generate_question(tool)

# =========================
# AI TUTOR (RULE BASED)
# =========================
def ai_tutor(q):

    q = q.lower()

    if "extrude" in q:
        return "Extrude = 2D sketch ko 3D solid banata hai (height add hoti hai)."

    if "cut" in q:
        return "Cut = material remove karne ka process (subtractive)."

    if "revolve" in q:
        return "Revolve = axis ke around rotation se shape banti hai."

    return "Engineering thinking: shape + function + manufacturing logic samjho."

# =========================
# CAD RENDER ENGINE (SAFE)
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    if stage == "start":
        t = np.linspace(0, 2*np.pi, 60)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

    elif stage == "create":
        t = np.linspace(0, 2*np.pi, 30)
        z = np.linspace(0, h, 20)
        t, z = np.meshgrid(t, z)

        fig.add_trace(go.Surface(
            x=np.cos(t),
            y=np.sin(t),
            z=z,
            opacity=0.85
        ))

    elif stage == "modify":
        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,h,h,h,h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.8))

    elif stage == "finish":
        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 20)
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
# UI
# =========================
st.sidebar.title("📊 Dashboard")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Tool:", st.session_state.tool_index, "/ 200")

progress = st.session_state.tool_index / 200
st.sidebar.progress(progress)

mode = st.sidebar.radio("Mode", ["Learn", "Practice", "Exam"])

st.subheader(f"🛠 Tool: {tool['name']}")
st.info(tool["why"])

st.subheader("🎯 Question")
choice = st.radio(q, options)

st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

# =========================
# ACTIONS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit"):
        if choice == answer:
            st.success("✔ Correct Thinking")
            st.session_state.score += 1

            if tool["type"] == "create":
                st.session_state.stage = "create"
            elif tool["type"] == "modify":
                st.session_state.stage = "modify"
            else:
                st.session_state.stage = "finish"
        else:
            st.error("❌ Wrong Answer")

        st.session_state.tool_index += 1

with col2:
    if st.button("🤖 AI Help"):
        st.info(ai_tutor(q))

with col3:
    if st.button("Next Tool"):
        st.session_state.tool_index += 1

# =========================
# CAD VIEW
# =========================
st.subheader("📐 Live CAD Simulation")
st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# RESET SYSTEM
# =========================
if st.sidebar.button("Reset All"):
    st.session_state.score = 0
    st.session_state.tool_index = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
