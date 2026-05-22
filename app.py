import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala LMS Pro", layout="wide")

st.title("🏭 SolidShala LMS + CAD Thinking Platform (Final System)")
st.write("Learn Engineering → Practice CAD → Pass Exams → Build Thinking")

# =========================
# SESSION STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "lesson" not in st.session_state:
    st.session_state.lesson = 0

if "tool_index" not in st.session_state:
    st.session_state.tool_index = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "mode" not in st.session_state:
    st.session_state.mode = "Learn"

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# TOOL DATABASE (200 SYSTEM)
# =========================
BASE_TOOLS = [
    ("Extrude", "create", "2D → 3D conversion"),
    ("Revolve", "create", "Rotational geometry"),
    ("Cut", "modify", "Material removal"),
    ("Fillet", "finish", "Edge smoothing"),
    ("Chamfer", "finish", "Angular edge cut"),
    ("Shell", "modify", "Hollow structure"),
    ("Pattern", "copy", "Repeat feature"),
    ("Mirror", "copy", "Symmetry creation")
]

TOOLS = []
for i in range(200):
    t = random.choice(BASE_TOOLS)
    TOOLS.append({
        "name": f"{t[0]}_{i}",
        "type": t[1],
        "why": t[2]
    })

tool = TOOLS[st.session_state.tool_index % len(TOOLS)]

# =========================
# QUESTION ENGINE
# =========================
def make_question(tool):

    if "Extrude" in tool["name"]:
        return "2D sketch ko 3D banane ke liye best tool?", ["Extrude", "Cut", "Mirror"], "Extrude"

    if "Revolve" in tool["name"]:
        return "Rotational part ke liye best tool?", ["Revolve", "Extrude", "Scale"], "Revolve"

    if "Cut" in tool["name"]:
        return "Material remove karne ke liye?", ["Cut", "Fillet", "Pattern"], "Cut"

    return f"{tool['name']} kis category ka tool hai?", ["Create", "Modify", "Finish"], tool["type"].capitalize()

q, options, answer = make_question(tool)

# =========================
# CAD VISUAL ENGINE
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

        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 30)
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
# AI TUTOR (RULE BASED)
# =========================
def ai_tutor(question):

    if "Extrude" in question:
        return "Extrude 2D shape ko 3D solid banata hai (height add hoti hai)."
    if "Cut" in question:
        return "Cut material remove karta hai (subtractive process)."
    if "Revolve" in question:
        return "Revolve rotational parts banata hai (axis symmetry)."

    return "Think in geometry + function + manufacturing logic."

# =========================
# MODE SELECT
# =========================
st.sidebar.title("🎮 Mode")
st.session_state.mode = st.sidebar.radio("Select", ["Learn Mode", "Practice Mode", "Exam Mode"])

# =========================
# MAIN UI
# =========================
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

    if st.button("Submit Answer"):

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
            st.error("❌ Wrong Thinking")

        st.session_state.tool_index += 1

with col2:

    if st.button("🤖 AI Help"):
        st.write(ai_tutor(q))

with col3:

    if st.button("Next Tool"):
        st.session_state.tool_index += 1

# =========================
# PRACTICE / LEARN / EXAM SWITCH
# =========================
st.subheader("📐 CAD View")
st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# DASHBOARD
# =========================
st.sidebar.title("📊 Dashboard")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Tool Index:", st.session_state.tool_index)

progress = (st.session_state.tool_index % 200) / 2
st.sidebar.progress(progress / 100)

if st.sidebar.button("Reset System"):
    st.session_state.score = 0
    st.session_state.tool_index = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
