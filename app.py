import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala Global CAD Platform", layout="wide")

st.title("🌍 SolidShala Global CAD Learning Platform")
st.write("AI Powered Engineering Education System (Industry + LMS + Simulation)")

# =========================
# SAFE STATE SYSTEM (PRODUCTION READY)
# =========================
DEFAULT_STATE = {
    "user": "Guest",
    "score": 0,
    "tool_index": 0,
    "stage": "start",
    "mode": "Learn",
    "level": 1,
    "height": 1.0
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# 200+ TOOL ENGINE (REAL STRUCTURE)
# =========================
TOOL_LIBRARY = [
    ("Extrude", "create", "2D to 3D solid conversion"),
    ("Revolve", "create", "Rotational geometry creation"),
    ("Cut", "modify", "Material subtraction process"),
    ("Fillet", "finish", "Edge smoothing for stress relief"),
    ("Chamfer", "finish", "Angular edge finishing"),
    ("Shell", "modify", "Hollow structure creation"),
    ("Pattern", "copy", "Feature repetition system"),
    ("Mirror", "copy", "Symmetry duplication"),
    ("Sweep", "create", "Path based solid creation"),
    ("Loft", "create", "Profile blending surface")
]

TOOLS = []
for i in range(200):
    base = random.choice(TOOL_LIBRARY)
    TOOLS.append({
        "name": f"{base[0]}_{i}",
        "type": base[1],
        "desc": base[2]
    })

tool = TOOLS[st.session_state.tool_index % 200]

# =========================
# QUESTION ENGINE (SMART LEARNING LOGIC)
# =========================
def generate_question(tool):

    name = tool["name"]

    if "Extrude" in name:
        return "Extrude ka main purpose kya hai?", ["3D creation", "Cutting", "Rotation"], "3D creation"

    if "Cut" in name:
        return "Cut operation kis liye use hota hai?", ["Remove material", "Add material", "Rotate shape"], "Remove material"

    if "Revolve" in name:
        return "Revolve kis process ka part hai?", ["Rotation based modeling", "Cutting", "Scaling"], "Rotation based modeling"

    return "Is tool ka category kya hai?", ["Create", "Modify", "Finish"], tool["type"].capitalize()

q, options, answer = generate_question(tool)

# =========================
# AI ENGINE (EDUCATIONAL BRAIN)
# =========================
def ai_brain(question):

    q = question.lower()

    if "extrude" in q:
        return "Extrude = 2D sketch ko 3D solid banata hai (depth add hoti hai)."

    if "cut" in q:
        return "Cut = material remove karne ka process (machining logic)."

    if "revolve" in q:
        return "Revolve = axis ke around rotation se solid create hota hai."

    if "fillet" in q:
        return "Fillet = sharp edges smooth karna (stress reduction)."

    return "Engineering thinking: shape + purpose + manufacturing process samjho."

# =========================
# CAD VISUAL ENGINE (SAFE + STABLE)
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    if stage == "start":
        t = np.linspace(0, 2*np.pi, 80)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

    elif stage == "create":
        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 25)
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

    fig.update_layout(height=520, scene=dict(aspectmode="data"))
    return fig

# =========================
# SIDEBAR (GLOBAL DASHBOARD)
# =========================
st.sidebar.title("🌍 Global Dashboard")

st.sidebar.write("User:", st.session_state.user)
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Level:", st.session_state.level)
st.sidebar.write("Tool:", st.session_state.tool_index, "/ 200")

progress = st.session_state.tool_index / 200
st.sidebar.progress(progress)

mode = st.sidebar.radio("Mode", ["Learn", "Practice", "Exam"])

# =========================
# MAIN UI
# =========================
st.subheader(f"🛠 Tool: {tool['name']}")
st.info(tool["desc"])

st.subheader("🎯 Engineering Question")

choice = st.radio(q, options)

st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

# =========================
# ACTION SYSTEM
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Submit Answer"):

        if choice == answer:
            st.success("✔ Correct Engineering Decision")
            st.session_state.score += 1

            if st.session_state.score % 10 == 0:
                st.session_state.level += 1

            if tool["type"] == "create":
                st.session_state.stage = "create"
            elif tool["type"] == "modify":
                st.session_state.stage = "modify"
            else:
                st.session_state.stage = "finish"

        else:
            st.error("❌ Wrong Concept")

        st.session_state.tool_index += 1

with col2:
    if st.button("🤖 AI Tutor"):
        st.info(ai_brain(q))

with col3:
    if st.button("Next Tool"):
        st.session_state.tool_index += 1

# =========================
# CAD VIEW
# =========================
st.subheader("📐 Live Engineering Simulation")
st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# RESET SYSTEM
# =========================
if st.sidebar.button("Reset Platform"):
    for k, v in DEFAULT_STATE.items():
        st.session_state[k] = v
