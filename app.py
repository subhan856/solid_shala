import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala Stable CAD LMS", layout="wide")

st.title("🏭 SolidShala CAD LMS (Stable Production Version)")
st.write("Clean + Stable + Learning Focused System")

# =========================
# SAFE SESSION STATE
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "tool_index" not in st.session_state:
    st.session_state.tool_index = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# SAFE TOOL SYSTEM (200 LOGIC)
# =========================
BASE_TOOLS = [
    ("Extrude", "create"),
    ("Revolve", "create"),
    ("Cut", "modify"),
    ("Fillet", "finish"),
    ("Chamfer", "finish"),
    ("Shell", "modify"),
    ("Pattern", "copy"),
    ("Mirror", "copy")
]

TOOLS = []
for i in range(200):
    t = random.choice(BASE_TOOLS)
    TOOLS.append({
        "name": f"{t[0]}_{i}",
        "type": t[1],
        "why": f"{t[0]} engineering concept"
    })

tool = TOOLS[st.session_state.tool_index % len(TOOLS)]

# =========================
# QUESTION ENGINE (SAFE)
# =========================
def question(tool):
    if "Extrude" in tool["name"]:
        return "2D → 3D ke liye best tool?", ["Extrude", "Cut", "Mirror"], "Extrude"

    if "Cut" in tool["name"]:
        return "Material remove karne ke liye?", ["Cut", "Fillet", "Pattern"], "Cut"

    if "Revolve" in tool["name"]:
        return "Rotational shape ke liye?", ["Revolve", "Extrude", "Scale"], "Revolve"

    return "Tool category?", ["Create", "Modify", "Finish"], tool["type"].capitalize()

q, options, answer = question(tool)

# =========================
# SAFE CAD RENDER
# =========================
def render(stage):

    fig = go.Figure()
    h = st.session_state.height

    if stage == "start":
        t = np.linspace(0, 2*np.pi, 50)
        fig.add_trace(go.Scatter3d(
            x=np.cos(t),
            y=np.sin(t),
            z=np.zeros_like(t),
            mode="lines"
        ))

    elif stage == "create":
        t = np.linspace(0, 2*np.pi, 30)
        z = np.linspace(0, h, 15)
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
        z = np.linspace(0, h, 15)
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
st.subheader(f"🛠 Tool: {tool['name']}")
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
    if st.button("Next Tool"):
        st.session_state.tool_index += 1

# =========================
# CAD VIEW
# =========================
st.subheader("📐 CAD View")
st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# FIXED PROGRESS BAR (IMPORTANT FIX)
# =========================
st.sidebar.title("📊 Dashboard")

progress = st.session_state.tool_index % 200
st.sidebar.progress(progress / 200)   # ✅ FIXED RANGE (0–1 safe)

st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Tool:", st.session_state.tool_index, "/ 200")

# RESET
if st.sidebar.button("Reset"):
    st.session_state.score = 0
    st.session_state.tool_index = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
