import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False


st.set_page_config(page_title="SolidShala Stable", layout="wide")

st.title("🛠️ SolidShala - Stable CAD Learning Engine")


# =========================
# STATE (STABLE CORE)
# =========================
if "model" not in st.session_state:
    st.session_state.model = "cube"

if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# MODELS (FIXED)
# =========================
def cube():
    x = [0,1,1,0,0,1,1,0]
    y = [0,0,1,1,0,0,1,1]
    z = [0,0,0,0,1,1,1,1]
    return go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,opacity=0.5)])


def cylinder():
    t = np.linspace(0,2*np.pi,50)
    z = np.linspace(0,1,2)
    t,z = np.meshgrid(t,z)
    x = np.cos(t)
    y = np.sin(t)
    return go.Figure(data=[go.Surface(x=x,y=y,z=z)])


def render():
    return cube() if st.session_state.model == "cube" else cylinder()


# =========================
# TOOL ENGINE (SAFE ONLY)
# =========================
def apply_tool(tool):

    if tool == "Extrude":
        st.session_state.model = "cube"

    elif tool == "Revolve":
        st.session_state.model = "cylinder"

    st.session_state.history.append(tool)


# =========================
# ANIMATION (SIMPLE BUT STABLE)
# =========================
def animate(tool):
    box = st.empty()
    for s in ["Processing...", tool + " applied", "Done"]:
        box.info(s)
        time.sleep(0.3)
    box.success("Updated")


# =========================
# UI
# =========================
TOOLS = ["Extrude","Revolve","Cut","Fillet","Chamfer","Shell"]

tool = st.sidebar.selectbox("Tool", TOOLS)


col1, col2 = st.columns(2)


with col1:

    st.subheader("✏️ Canvas")

    if CANVAS_AVAILABLE:
        st_canvas(
            fill_color="rgba(0,0,255,0.1)",
            stroke_width=3,
            stroke_color="#000",
            background_color="#fff",
            height=350,
            drawing_mode="freedraw",
            key="canvas"
        )


with col2:

    st.subheader("🏗️ Model")

    st.plotly_chart(render(), use_container_width=True)

    if st.button("Apply Tool"):

        animate(tool)
        apply_tool(tool)
        st.rerun()


st.divider()

st.subheader("📜 History")

for i,h in enumerate(st.session_state.history,1):
    st.write(i, h)
