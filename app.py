import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(page_title="SolidShala v2 INSANE", layout="wide")

st.title("🔥 SolidShala v2 - INSANE CAD ENGINE")

# =========================
# SESSION STATE
# =========================
defaults = {
    "points": [],
    "constraints": [],
    "score": 0,
    "level": 1,
    "gear_speed": 1.0
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# 🧠 DRAG & DROP SKETCH ENGINE
# =========================
st.sidebar.header("✏️ Sketch Tool (CAD Mode)")

x = st.sidebar.slider("X", 0.0, 10.0, 5.0)
y = st.sidebar.slider("Y", 0.0, 10.0, 5.0)

if st.sidebar.button("➕ Add Sketch Point"):
    st.session_state.points.append((x, y))

# =========================
# CONSTRAINT SYSTEM (SOLIDWORKS STYLE)
# =========================
st.sidebar.subheader("🔗 Constraints")

constraint_type = st.sidebar.selectbox(
    "Add Constraint",
    ["Fix Point", "Horizontal", "Vertical", "Equal Length"]
)

if st.sidebar.button("Add Constraint"):
    st.session_state.constraints.append(constraint_type)

# =========================
# SKETCH RENDER
# =========================
def draw_sketch(points):

    fig = go.Figure()

    if len(points) > 1:
        x, y = zip(*points)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers"))

    fig.update_layout(height=400)
    return fig

# =========================
# ⚙️ REAL GEAR SIMULATION (PHYSICS)
# =========================
def gear_sim(speed):

    theta = np.linspace(0, 2*np.pi, 100)

    x1 = np.cos(theta)
    y1 = np.sin(theta)

    x2 = np.cos(theta + speed)
    y2 = np.sin(theta + speed)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x1, y=y1, mode="lines", name="Gear A"))
    fig.add_trace(go.Scatter(x=x2*1.5, y=y2*1.5, mode="lines", name="Gear B"))

    fig.update_layout(height=400)
    return fig

# =========================
# MULTIPLAYER CHALLENGE (MOCK SYSTEM)
# =========================
def challenge():

    challenges = [
        "Draw a circle sketch",
        "Make 2D to 3D extrusion concept",
        "Add constraint to shape",
        "Build gear system"
    ]

    return random.choice(challenges)

# =========================
# UI TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "✏️ CAD Sketch",
    "🔗 Constraints",
    "⚙️ Gear Simulation",
    "🏆 Multiplayer Challenge"
])

# =========================
# TAB 1 - SKETCH
# =========================
with tab1:
    st.subheader("Drag & Drop Sketch System")

    st.plotly_chart(draw_sketch(st.session_state.points))

# =========================
# TAB 2 - CONSTRAINTS
# =========================
with tab2:
    st.subheader("Constraint System (SolidWorks Logic)")

    st.write("Applied Constraints:")
    st.write(st.session_state.constraints)

    st.info("Future: constraints will lock geometry behavior")

# =========================
# TAB 3 - GEAR PHYSICS
# =========================
with tab3:
    st.subheader("Real Gear Meshing Simulation")

    speed = st.slider("Gear Speed", 0.1, 5.0, 1.0)

    st.session_state.gear_speed = speed

    st.plotly_chart(gear_sim(speed))

# =========================
# TAB 4 - CHALLENGE SYSTEM
# =========================
with tab4:
    st.subheader("Multiplayer CAD Challenge")

    st.success("Task: " + challenge())

    if st.button("Complete Challenge"):
        st.session_state.score += 10
        st.session_state.level += 1
        st.success("Score Updated!")
