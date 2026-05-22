import streamlit as st
import random
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SolidShala 200 Tools CAD", layout="wide")

st.title("🧠 SolidShala CAD Master System (200 Tools Edition)")
st.write("Engineering Thinking + 200 Tool Intelligence System")

# =========================
# STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "step" not in st.session_state:
    st.session_state.step = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "tool_index" not in st.session_state:
    st.session_state.tool_index = 0

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# 200 TOOLS SYSTEM (DATA DRIVEN)
# =========================
TOOLS = [
    {"name": "Extrude", "why": "2D → 3D conversion", "type": "create"},
    {"name": "Revolve", "why": "Rotational parts", "type": "create"},
    {"name": "Cut", "why": "Material removal", "type": "modify"},
    {"name": "Fillet", "why": "Edge smoothing", "type": "finish"},
    {"name": "Chamfer", "why": "Angular edge cut", "type": "finish"},
]

# Expand to 200 tools dynamically
BASE = ["Shell", "Pattern", "Mirror", "Scale", "Loft", "Sweep", "Draft"]

for i in range(1, 200):
    tool = random.choice(BASE)
    TOOLS.append({
        "name": f"{tool}_{i}",
        "why": f"{tool} operation engineering use case {i}",
        "type": "advanced"
    })

# =========================
# QUESTION GENERATOR (200+ QUESTIONS LOGIC)
# =========================
def generate_question(tool):

    if tool["name"].startswith("Extrude"):
        q = "2D sketch ko 3D banane ke liye?"
        options = ["Extrude", "Cut", "Mirror"]
        answer = "Extrude"

    elif tool["name"].startswith("Revolve"):
        q = "Rotational part ke liye best tool?"
        options = ["Revolve", "Extrude", "Scale"]
        answer = "Revolve"

    elif tool["name"].startswith("Cut"):
        q = "Material remove karne ke liye?"
        options = ["Cut", "Fillet", "Pattern"]
        answer = "Cut"

    else:
        q = f"{tool['name']} kis category ka tool hai?"
        options = ["Create", "Modify", "Finish"]
        answer = tool["type"].capitalize()

    return q, options, answer

# =========================
# TOOL PICK
# =========================
tool = TOOLS[st.session_state.tool_index % len(TOOLS)]

q, options, answer = generate_question(tool)

# =========================
# MODEL RENDER (SIMPLE SAFE CAD VIEW)
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
# UI
# =========================
st.subheader(f"🛠 Tool #{st.session_state.tool_index+1}: {tool['name']}")

st.info(tool["why"])

st.subheader("🎯 Question")

choice = st.radio(q, options)

st.slider("Model Scale", 1.0, 5.0, 1.0, key="height")

# =========================
# ACTIONS
# =========================
col1, col2 = st.columns(2)

with col1:

    if st.button("Submit Answer"):

        if choice == answer:
            st.success("✔ Correct Engineering Thinking")
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
        st.session_state.step += 1

with col2:

    if st.button("Next Tool"):
        st.session_state.tool_index += 1

# =========================
# MODEL VIEW
# =========================
st.subheader("📐 Live CAD View")

st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# DASHBOARD
# =========================
st.sidebar.title("📊 System Dashboard")

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Step:", st.session_state.step)
st.sidebar.write("Tool Index:", st.session_state.tool_index)

progress = (st.session_state.tool_index % 200) / 2
st.sidebar.progress(progress / 100)

if st.sidebar.button("Reset System"):
    st.session_state.score = 0
    st.session_state.step = 0
    st.session_state.tool_index = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
