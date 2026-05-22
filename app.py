import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# optional canvas
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS = True
except:
    CANVAS = False

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(page_title="SolidShala CAD", layout="wide")

st.title("🛠️ SolidShala AI CAD Engine")
st.write("Sketch → Detect → Modify → Build Model")

# =====================================================
# SESSION STATE
# =====================================================
if "model" not in st.session_state:
    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "height": 1.0,
        "cut_depth": 0.0,
        "chamfer": 0.0,
        "scale": 1.0,
        "features": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# SHAPES
# =====================================================
def create_circle():
    st.session_state.model["shape"] = "circle"
    st.session_state.model["radius"] = 1.0
    st.session_state.model["height"] = 1.0

def create_square():
    st.session_state.model["shape"] = "square"
    st.session_state.model["height"] = 1.0

# =====================================================
# SIMPLE AI DETECT (SAFE)
# =====================================================
def detect_shape():
    # simple toggle demo (real AI nahi, stable version)
    if np.random.random() > 0.5:
        create_circle()
        return "circle"
    else:
        create_square()
        return "square"

# =====================================================
# TOOL ENGINE
# =====================================================
def apply_tool(tool):

    m = st.session_state.model

    if tool == "Extrude":
        m["height"] += 0.5

    elif tool == "Cut":
        m["cut_depth"] += 0.2
        m["height"] = max(0.3, m["height"] - 0.1)

    elif tool == "Chamfer":
        m["chamfer"] += 0.05

    elif tool == "Scale":
        m["scale"] += 0.1

    m["features"].append(tool)

    st.session_state.history.append({
        "tool": tool,
        "time": str(datetime.now())
    })

# =====================================================
# SAFE RENDER MODEL (IMPORTANT)
# =====================================================
def render_model():

    m = st.session_state.model
    fig = go.Figure()

    shape = m["shape"]

    # =========================
    # CYLINDER
    # =========================
    if shape == "circle":

        r = max(0.2, m["radius"] - m["cut_depth"] * 0.1)
        r *= m["scale"]

        h = m["height"]

        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 15)

        t, z = np.meshgrid(t, z)

        x = r * np.cos(t)
        y = r * np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.9))

    # =========================
    # BOX
    # =========================
    elif shape == "square":

        s = 1 * m["scale"]
        h = m["height"]
        c = m["chamfer"]

        x = [0, s, s, 0, 0, s, s, 0]
        y = [0, 0, s, s, 0, 0, s, s]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            opacity=0.7
        ))

        # chamfer visual (safe fake effect)
        if c > 0:
            fig.add_trace(go.Mesh3d(
                x=[c, s-c, s, 0],
                y=[0, 0, s, s],
                z=[h, h, h, h],
                opacity=0.3
            ))

    else:
        fig.add_annotation(
            text="Draw Shape First",
            showarrow=False,
            font=dict(size=20)
        )

    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=20, b=0),
        scene=dict(aspectmode="data")
    )

    return fig

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("CAD Tools")

tool = st.sidebar.selectbox(
    "Select Tool",
    ["Extrude", "Cut", "Chamfer", "Scale"]
)

# =====================================================
# LAYOUT
# =====================================================
col1, col2 = st.columns(2)

# =========================
# LEFT: CANVAS
# =========================
with col1:

    st.subheader("✏️ Sketch Area")

    if CANVAS:

        canvas = st_canvas(
            stroke_width=3,
            background_color="#111827",
            height=300,
            drawing_mode="freedraw",
            key="canvas"
        )

    if st.button("🤖 Detect Shape"):

        result = detect_shape()
        st.success(f"Detected: {result}")

    st.plotly_chart(render_model(), use_container_width=True)

# =========================
# RIGHT: CONTROLS
# =========================
with col2:

    st.subheader("⚙️ Actions")

    if st.button("Apply Tool"):

        apply_tool(tool)
        st.success(f"{tool} applied")

        st.rerun()

    st.subheader("📏 Model Info")

    m = st.session_state.model

    st.write("Shape:", m["shape"])
    st.write("Height:", m["height"])
    st.write("Cut:", m["cut_depth"])
    st.write("Chamfer:", m["chamfer"])

    st.subheader("🧠 History")

    for h in reversed(st.session_state.history[-5:]):
        st.write(h["tool"], h["time"])
