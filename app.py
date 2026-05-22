import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import io
import base64

st.set_page_config(page_title="SolidShala AI CAD", layout="wide")

st.title("🚀 SolidShala AI CAD Platform (Next Gen System)")

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "points" not in st.session_state:
    st.session_state.points = []

if "score" not in st.session_state:
    st.session_state.score = 0

# =========================
# AI TUTOR (ChatGPT Style Lite)
# =========================
def ai_tutor(msg):
    msg = msg.lower()

    if "extrude" in msg:
        return "Extrude 2D sketch ko 3D solid banata hai."
    if "cut" in msg:
        return "Cut material remove karta hai."
    if "revolve" in msg:
        return "Revolve rotation se shape create karta hai."
    if "gear" in msg:
        return "Gear torque transfer ke liye use hota hai."
    return "Engineering logic: shape + function + manufacturing samjho."

# =========================
# REAL SKETCH ENGINE (MOUSE DRAW)
# =========================
st.sidebar.header("✏️ Sketch Canvas (Mouse)")

canvas = st.sidebar.checkbox("Enable Sketch Mode")

if canvas:
    st.write("👉 Click points to draw shape (simulate CAD sketch)")

    x = st.slider("X point", 0.0, 10.0, 5.0)
    y = st.slider("Y point", 0.0, 10.0, 5.0)

    if st.button("Add Point"):
        st.session_state.points.append((x, y))

# =========================
# 3D ENGINE SIMULATION
# =========================
def render_engine():

    fig = go.Figure()

    # crankshaft
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    z = np.linspace(0, 5, 100)

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", name="Crankshaft"))

    # gearbox block
    fig.add_trace(go.Mesh3d(
        x=[0,2,2,0,0,2,2,0],
        y=[0,0,2,2,0,0,2,2],
        z=[0,0,0,0,2,2,2,2],
        opacity=0.5,
        name="Gearbox"
    ))

    fig.update_layout(height=500)
    return fig

# =========================
# UI TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 AI Tutor",
    "📐 Sketch CAD",
    "⚙️ 3D Engine",
    "🏆 Leaderboard"
])

# =========================
# AI CHAT
# =========================
with tab1:
    st.subheader("AI Tutor (ChatGPT Style)")

    user_input = st.text_input("Ask CAD question")

    if user_input:
        response = ai_tutor(user_input)
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("AI", response))

    for role, msg in st.session_state.chat[-10:]:
        st.write(f"**{role}:** {msg}")

# =========================
# SKETCH VIEW
# =========================
with tab2:
    st.subheader("Real Sketch System")

    if len(st.session_state.points) > 1:
        x, y = zip(*st.session_state.points)
        st.line_chart({"x": x, "y": y})
    else:
        st.info("Add points to create sketch")

# =========================
# 3D ENGINE
# =========================
with tab3:
    st.subheader("Engine + Gearbox + Crankshaft")

    st.plotly_chart(render_engine(), use_container_width=True)

# =========================
# LEADERBOARD (LOCAL MOCK)
# =========================
with tab4:
    st.subheader("Leaderboard System")

    st.session_state.score += len(st.session_state.points)

    st.write("Score:", st.session_state.score)
    st.write("Points:", len(st.session_state.points))
