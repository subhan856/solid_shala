import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================
# PAGE
# =========================
st.set_page_config(page_title="SolidShala Final", layout="wide")

st.title("🛠️ SolidShala Final CAD Simulator")
st.write("Draw → Select Tool → Build Model")

# =========================
# SAFE STATE
# =========================
if "model" not in st.session_state:
    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "height": 1.0,
        "cut": 0.0,
        "chamfer": 0.0,
        "scale": 1.0
    }

m = st.session_state.model

# =========================
# SHAPES
# =========================
def make_circle():
    m["shape"] = "circle"

def make_square():
    m["shape"] = "square"

# =========================
# TOOLS
# =========================
def apply_tool(tool):

    if tool == "Extrude":
        m["height"] += 0.5

    elif tool == "Cut":
        m["cut"] += 0.2

    elif tool == "Chamfer":
        m["chamfer"] += 0.1

    elif tool == "Scale":
        m["scale"] += 0.1

# =========================
# SIMPLE SHAPE DETECT (SAFE)
# =========================
def detect_shape():
    if np.random.rand() > 0.5:
        make_circle()
        return "circle"
    else:
        make_square()
        return "square"

# =========================
# RENDER MODEL (STABLE)
# =========================
def render():

    fig = go.Figure()

    if m["shape"] == "circle":

        r = max(0.2, m["radius"] - m["cut"])
        r *= m["scale"]
        h = m["height"]

        t = np.linspace(0, 2*np.pi, 40)
        z = np.linspace(0, h, 15)

        t, z = np.meshgrid(t, z)

        x = r * np.cos(t)
        y = r * np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.9))

    elif m["shape"] == "square":

        s = m["scale"]
        h = m["height"]
        c = m["chamfer"]

        size = 1 * s

        x = [0, size, size, 0, 0, size, size, 0]
        y = [0, 0, size, size, 0, 0, size, size]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.7))

        # chamfer effect (simple visual)
        if c > 0:
            fig.add_trace(go.Mesh3d(
                x=[c, size-c, size, 0],
                y=[0, 0, size, size],
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
        scene=dict(aspectmode="data"),
        margin=dict(l=0, r=0, t=20, b=0)
    )

    return fig

# =========================
# UI
# =========================
col1, col2 = st.columns(2)

with col1:

    st.subheader("✏️ Sketch")

    if st.button("Draw Circle"):
        make_circle()

    if st.button("Draw Square"):
        make_square()

    if st.button("Auto Detect Shape"):
        st.success(f"Detected: {detect_shape()}")

    st.plotly_chart(render(), use_container_width=True)

with col2:

    st.subheader("⚙️ Tools")

    tool = st.selectbox("Select Tool",
        ["Extrude", "Cut", "Chamfer", "Scale"]
    )

    if st.button("Apply Tool"):
        apply_tool(tool)
        st.success(f"{tool} applied")
        st.rerun()

    st.subheader("📊 Model Data")

    st.write("Shape:", m["shape"])
    st.write("Height:", m["height"])
    st.write("Cut:", m["cut"])
    st.write("Chamfer:", m["chamfer"])
    st.write("Scale:", m["scale"])
