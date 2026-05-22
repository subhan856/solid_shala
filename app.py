import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala Startup CAD LMS", layout="wide")

st.title("🚀 SolidShala Startup CAD Learning Platform")
st.write("From Beginner → Engineer → CAD Expert")

# =========================
# USERS (simple simulation login)
# =========================
if "user" not in st.session_state:
    st.session_state.user = "Guest"

if "score" not in st.session_state:
    st.session_state.score = 0

if "tool_index" not in st.session_state:
    st.session_state.tool_index = 0

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "height" not in st.session_state:
    st.session_state.height = 1.0

# =========================
# LOGIN SYSTEM (simple)
# =========================
st.sidebar.title("🔐 Login System")

name = st.sidebar.text_input("Enter Name")

if st.sidebar.button("Login"):
    if name:
        st.session_state.user = name
        st.sidebar.success(f"Welcome {name}")
    else:
        st.sidebar.error("Enter name first")

st.sidebar.write("👤 User:", st.session_state.user)

# =========================
# 200 TOOLS SYSTEM
# =========================
BASE = [
    ("Extrude", "create"),
    ("Revolve", "create"),
    ("Cut", "modify"),
    ("Fillet", "finish"),
    ("Chamfer", "finish"),
    ("Shell", "modify"),
    ("Pattern", "copy"),
    ("Mirror", "copy"),
    ("Sweep", "create"),
    ("Loft", "create")
]

TOOLS = []
for i in range(200):
    t = random.choice(BASE)
    TOOLS.append({
        "name": f"{t[0]}_{i}",
        "type": t[1],
        "why": f"{t[0]} engineering use case {i}"
    })

tool = TOOLS[st.session_state.tool_index % len(TOOLS)]

# =========================
# QUESTION ENGINE
# =========================
def make_question(tool):

    if "Extrude" in tool["name"]:
        return "2D sketch ko 3D banane ke liye?", ["Extrude", "Cut", "Mirror"], "Extrude"

    if "Cut" in tool["name"]:
        return "Material remove karne ke liye?", ["Cut", "Fillet", "Pattern"], "Cut"

    if "Revolve" in tool["name"]:
        return "Rotational part ke liye?", ["Revolve", "Extrude", "Scale"], "Revolve"

    return f"{tool['name']} kis category ka tool hai?", ["Create", "Modify", "Finish"], tool["type"].capitalize()

q, options, answer = make_question(tool)

# =========================
# AI TUTOR
# =========================
def ai_tutor(q):

    if "Extrude" in q:
        return "Extrude = 2D sketch → 3D solid"
    if "Cut" in q:
        return "Cut = material removal process"
    if "Revolve" in q:
        return "Revolve = axis rotation geometry"

    return "Think: geometry + function + engineering logic"

# =========================
# CAD MODEL ENGINE
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
st.subheader(f"👤 Student: {st.session_state.user}")

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
# MODEL VIEW
# =========================
st.subheader("📐 CAD Simulation")
st.plotly_chart(render(st.session_state.stage), use_container_width=True)

# =========================
# LEADERBOARD (simple local)
# =========================
st.sidebar.title("🏆 Dashboard")

st.sidebar.write("User:", st.session_state.user)
st.sidebar.write("Score:", st.session_state.score)
st.sidebar.write("Progress Tool:", st.session_state.tool_index)

st.sidebar.progress((st.session_state.tool_index % 200) / 2)

# =========================
# RESET
# =========================
if st.sidebar.button("Reset System"):
    st.session_state.score = 0
    st.session_state.tool_index = 0
    st.session_state.stage = "start"
    st.session_state.height = 1.0
