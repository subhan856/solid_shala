import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# =========================
# OPTIONAL CANVAS
# =========================
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS = True
except:
    CANVAS = False


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="SolidShala Pro V2", layout="wide")

st.title("🛠️ SolidShala Pro V2 - CAD Learning Engine")
st.caption("Professional SolidWorks-like Learning Simulator")


# =========================
# SESSION STATE INIT
# =========================
if "shape" not in st.session_state:
    st.session_state.shape = "cube"

if "features" not in st.session_state:
    st.session_state.features = []

if "history" not in st.session_state:
    st.session_state.history = []

if "steps" not in st.session_state:
    st.session_state.steps = 0

if "log" not in st.session_state:
    st.session_state.log = []


# =========================
# TOOLS LIST (20 CAD TOOLS)
# =========================
TOOLS = [
    "Extrude","Revolve","Cut","Fillet","Chamfer",
    "Shell","Loft","Sweep","Mirror","Pattern",
    "Move","Rotate","Scale","Offset","Thicken",
    "Union","Subtract","Intersect","Draft","FilletEdge"
]


# =========================
# BASE MODELS
# =========================
def cube():
    x = [0,1,1,0,0,1,1,0]
    y = [0,0,1,1,0,0,1,1]
    z = [0,0,0,0,1,1,1,1]
    return go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,opacity=0.5,color="lightblue")])


def cylinder():
    t = np.linspace(0, 2*np.pi, 60)
    z = np.linspace(0, 1, 2)
    t, z = np.meshgrid(t, z)
    x = np.cos(t)
    y = np.sin(t)
    return go.Figure(data=[go.Surface(x=x,y=y,z=z)])


# =========================
# MODEL RENDER ENGINE
# =========================
def render_model():

    if st.session_state.shape == "cube":
        fig = cube()
    else:
        fig = cylinder()

    # apply feature tags visually
    title = "Base Model"
    if st.session_state.features:
        title = " | ".join(st.session_state.features[-3:])

    fig.update_layout(
        title=title,
        margin=dict(l=0,r=0,t=30,b=0)
    )

    return fig


# =========================
# ANIMATION ENGINE (SMOOTH)
# =========================
def animate(tool):

    box = st.empty()

    steps = [
        f"Reading sketch...",
        f"Analyzing tool: {tool}",
        "Generating geometry...",
        "Applying constraints...",
        "Updating model...",
        "Finalizing..."
    ]

    for s in steps:
        box.info(s)
        time.sleep(0.2)

    box.success(f"{tool} applied successfully")


# =========================
# TOOL ENGINE (REAL CAD LOGIC)
# =========================
def apply_tool(tool):

    st.session_state.log.append({
        "time": str(datetime.now()),
        "tool": tool
    })

    # BASE SHAPES
    if tool == "Extrude":
        st.session_state.shape = "cube"

    elif tool == "Revolve":
        st.session_state.shape = "cylinder"

    # MODIFIERS
    elif tool in ["Cut","Shell","Fillet","Chamfer","FilletEdge"]:
        st.session_state.features.append(tool)

    elif tool == "Mirror":
        st.session_state.features.append("Mirrored")

    elif tool == "Pattern":
        st.session_state.features.append("Patterned")

    elif tool == "Union":
        st.session_state.features.append("Union Applied")

    elif tool == "Subtract":
        st.session_state.features.append("Subtracted")

    elif tool == "Intersect":
        st.session_state.features.append("Intersected")

    elif tool == "Draft":
        st.session_state.features.append("Draft Angle")

    elif tool == "Offset":
        st.session_state.features.append("Offset Surface")

    elif tool == "Thicken":
        st.session_state.features.append("Thickened Surface")

    else:
        st.session_state.features.append(tool)


# =========================
# SIDEBAR UI
# =========================
st.sidebar.header("🎛️ CAD Controls")

tool = st.sidebar.selectbox("Select Tool", TOOLS)

mode = st.sidebar.radio("Mode", ["Modeling","History","Learn"])


# =========================
# LEARN MODE
# =========================
if mode == "Learn":

    st.subheader("📘 Tool Learning Panel")

    desc = {
        "Extrude":"2D sketch ko 3D solid mein convert karta hai",
        "Revolve":"Profile rotate karke 3D shape banata hai",
        "Cut":"Material remove karta hai",
        "Shell":"Solid ko hollow banata hai",
        "Fillet":"Edges smooth karta hai",
        "Chamfer":"Edges bevel karta hai"
    }

    st.info(desc.get(tool,"CAD tool for geometry modification"))

    st.write("💡 Industry use: Mechanical design, product design, simulation")


# =========================
# MODELING MODE
# =========================
elif mode == "Modeling":

    col1, col2 = st.columns([1.2,1])

    with col1:

        st.subheader("✏️ Sketch Canvas")

        if CANVAS:
            st_canvas(
                fill_color="rgba(0,0,255,0.1)",
                stroke_width=3,
                stroke_color="#000",
                background_color="#fff",
                height=400,
                drawing_mode="freedraw",
                key="canvas"
            )
        else:
            st.warning("Install streamlit-drawable-canvas")


    with col2:

        st.subheader("🏗️ Live Model Viewer")

        st.plotly_chart(render_model(), use_container_width=True)

        if st.button("🚀 Apply Tool"):

            animate(tool)
            apply_tool(tool)

            st.session_state.steps += 1

            st.rerun()


# =========================
# HISTORY MODE
# =========================
else:

    st.subheader("📜 CAD Feature History Tree")

    if st.session_state.log:

        for i, item in enumerate(st.session_state.log, 1):
            st.write(f"{i}. {item['tool']}  |  {item['time']}")

    else:
        st.info("No history yet")


# =========================
# FOOTER STATS
# =========================
st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Shape Type", st.session_state.shape)
col2.metric("Features", len(st.session_state.features))
col3.metric("Steps", st.session_state.steps)
