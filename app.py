import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================
# PAGE
# =========================
st.set_page_config(page_title="SolidShala Stable CAD", layout="wide")

st.title("🛠️ SolidShala Stable CAD Engine V3")
st.write("No crash | All tools | Learning mode included")

# =========================
# SESSION STATE
# =========================
if "model" not in st.session_state:
    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "height": 1.0,
        "cut": 0.0,
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

# =========================
# SHAPES
# =========================
def create_circle():
    m["shape"] = "circle"

def create_square():
    m["shape"] = "square"

# =========================
# TOOL ENGINE (SAFE)
# =========================
def apply_tool(tool):

    if tool == "Extrude":
        m["height"] += 0.5

    elif tool == "Cut":
        m["cut"] += 0.2

    elif tool == "Chamfer":
        m["chamfer"] += 0.1

    elif tool == "Fillet":
        m["fillet"] += 0.1

    elif tool == "Shell":
        m["shell"] += 0.1

    elif tool == "Scale":
        m["scale"] += 0.1

    elif tool == "Mirror":
        m["mirror"] = True

    elif tool == "Pattern":
        m["pattern"] += 1

    elif tool == "Reset":
        st.session_state.model = {
            "shape": None,
            "radius": 1.0,
            "height": 1.0,
            "cut": 0.0,
            "chamfer": 0.0,
            "fillet": 0.0,
            "shell": 0.0,
            "scale": 1.0,
            "mirror": False,
            "pattern": 1,
            "features": []
        }

    m["features"].append(tool)

    st.session_state.history.append({
        "tool": tool,
        "time": str(datetime.now())
    })

# =========================
# SIMPLE SHAPE DETECT
# =========================
def detect_shape():
    if np.random.rand() > 0.5:
        create_circle()
        return "circle"
    else:
        create_square()
        return "square"

# =========================
# SAFE RENDER (NO CRASH)
# =========================
def render_model():

    fig = go.Figure()

    # =====================
    # CIRCLE MODEL
    # =====================
    if m["shape"] == "circle":

        r = max(0.2, m["radius"] - m["cut"] * 0.1)
        r *= m["scale"]

        h = m["height"]

        t = np.linspace(0, 2*np.pi, 50)
        z = np.linspace(0, h, 20)

        t, z = np.meshgrid(t, z)

        x = r * np.cos(t)
        y = r * np.sin(t)

        fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.9))

        # shell effect
        if m["shell"] > 0:
            r2 = max(0.1, r - m["shell"] * 0.2)

            fig.add_trace(go.Surface(
                x=r2*np.cos(t),
                y=r2*np.sin(t),
                z=z,
                opacity=0.3
            ))

    # =====================
    # BOX MODEL
    # =====================
    elif m["shape"] == "square":

        s = m["scale"]
        h = m["height"]
        c = m["chamfer"]

        size = 1 * s

        x = [0, size, size, 0, 0, size, size, 0]
        y = [0, 0, size, size, 0, 0, size, size]
        z = [0, 0, 0, 0, h, h, h, h]

        fig.add_trace(go.Mesh3d(x=x, y=y, z=z, opacity=0.7))

        # chamfer (visual only safe)
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

# =========================
# LEARNING MODE DATA
# =========================
LEARN = {
    "Extrude": "2D shape ko 3D banata hai (height increase)",
    "Cut": "Material remove karta hai",
    "Chamfer": "Edge ko angled cut deta hai",
    "Fillet": "Edge ko smooth round banata hai",
    "Shell": "Solid ko hollow banata hai",
    "Scale": "Model size increase/decrease",
    "Mirror": "Duplicate flip karta hai",
    "Pattern": "Copy multiple times"
}

# =========================
# UI
# =========================
col1, col2 = st.columns(2)

with col1:

    st.subheader("✏️ Shape Controls")

    if st.button("Circle"):
        create_circle()

    if st.button("Square"):
        create_square()

    if st.button("Random Detect"):
        st.success(detect_shape())

    st.plotly_chart(render_model(), use_container_width=True)

with col2:

    st.subheader("⚙️ Tools")

    tool = st.selectbox(
        "Select Tool",
        list(LEARN.keys())
    )

    if st.button("Apply Tool"):
        apply_tool(tool)
        st.success(f"{tool} applied")
        st.rerun()

    st.subheader("📘 Learning Mode")

    st.info(LEARN.get(tool, ""))

    st.subheader("📊 Model Info")

    st.write("Shape:", m["shape"])
    st.write("Height:", m["height"])
    st.write("Cut:", m["cut"])
    st.write("Chamfer:", m["chamfer"])
    st.write("Shell:", m["shell"])
    st.write("Scale:", m["scale"])

    st.subheader("🧠 History")

    for h in reversed(st.session_state.history[-6:]):
        st.write(h["tool"], h["time"])
