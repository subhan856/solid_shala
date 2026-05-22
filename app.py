import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# optional canvas
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS = True
except:
    CANVAS = False

# =====================================================
# PAGE
# =====================================================
st.set_page_config(page_title="SolidShala CAD", layout="wide")

st.title("🛠️ SolidShala AI CAD Engine")
st.write("Stable Version (No Crash + Full Tools)")

# =====================================================
# SAFE MODEL INIT (IMPORTANT FIX)
# =====================================================
if "model" not in st.session_state:
    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "height": 1.0,
        "cut_depth": 0.0,
        "chamfer": 0.0,
        "fillet": 0.0,
        "shell": 0.0,
        "scale": 1.0,
        "mirror": False,
        "pattern": 1,
        "features": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

m = st.session_state.model

# =====================================================
# SHAPES
# =====================================================
def create_circle():
    m["shape"] = "circle"

def create_square():
    m["shape"] = "square"

# =====================================================
# SIMPLE DETECT
# =====================================================
def detect_shape():
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

    if tool == "Extrude":
        m["height"] += 0.5

    elif tool == "Cut":
        m["cut_depth"] += 0.2
        m["height"] = max(0.3, m["height"] - 0.1)

    elif tool == "Chamfer":
        m["chamfer"] += 0.05

    elif tool == "Fillet":
        m["fillet"] += 0.05

    elif tool == "Shell":
        m["shell"] += 0.1

    elif tool == "Scale":
        m["scale"] += 0.1

    elif tool == "Mirror":
        m["mirror"] = True

    elif tool == "Pattern":
        m["pattern"] += 1

    elif tool == "Reset":
        m.update({
            "shape": None,
            "radius": 1.0,
            "height": 1.0,
            "cut_depth": 0.0,
            "chamfer": 0.0,
            "fillet": 0.0,
            "shell": 0.0,
            "scale": 1.0,
            "mirror": False,
            "pattern": 1,
            "features": []
        })

    m["features"].append(tool)

    st.session_state.history.append({
        "tool": tool,
        "time": str(datetime.now())
    })

# =====================================================
# SAFE RENDER (FIXED + STABLE)
# =====================================================
def render_model():

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
        z = np.linspace(0, h, 20)

        t, z = np.meshgrid(t, z)

        x = r * np.cos(t)
        y = r * np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.9))

        # shell
        if m["shell"] > 0:
            r2 = max(0.1, r - m["shell"] * 0.2)

            fig.add_trace(go.Surface(
                x=r2*np.cos(t),
                y=r2*np.sin(t),
                z=z,
                opacity=0.3
            ))

    # =========================
    # BOX
    # =========================
    elif shape == "square":

        s = m["scale"]
        h = m["height"]
        c = m["chamfer"]

        size = 1 * s

        x = [0, size, size, 0, 0, size, size, 0]
        y = [0, 0, size, size, 0, 0, size, size]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.7))

        # chamfer (visual safe)
        if c > 0:
            fig.add_trace(go.Mesh3d(
                x=[c, size-c, size, 0],
                y=[0, 0, size, size],
                z=[h, h, h, h],
                opacity=0.3
            ))

        # mirror
        if m["mirror"]:
            fig.add_trace(go.Mesh3d(
                x=[-i for i in x],
                y=y,
                z=z,
                opacity=0.4
            ))

        # pattern
        for i in range(1, m["pattern"]):
            fig.add_trace(go.Mesh3d(
                x=[v + i*2 for v in x],
                y=y,
                z=z,
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

# =====================================================
# TOOLS
# =====================================================
TOOLS = [
    "Extrude",
    "Cut",
    "Chamfer",
    "Fillet",
    "Shell",
    "Scale",
    "Mirror",
    "Pattern",
    "Reset"
]

# =====================================================
# UI
# =====================================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("✏️ Canvas")

    if CANVAS:
        st_canvas(
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

with col2:

    st.subheader("⚙️ Tools")

    tool = st.selectbox("Select Tool", TOOLS)

    if st.button("Apply Tool"):
        apply_tool(tool)
        st.success(f"{tool} applied")
        st.rerun()

    st.subheader("📊 Model Info")

    st.write("Shape:", m["shape"])
    st.write("Height:", m["height"])
    st.write("Cut:", m["cut_depth"])
    st.write("Chamfer:", m["chamfer"])
    st.write("Shell:", m["shell"])
    st.write("Pattern:", m["pattern"])

    st.subheader("🧠 History")

    for h in reversed(st.session_state.history[-6:]):
        st.write(h["tool"], h["time"])
