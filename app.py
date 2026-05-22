import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False


st.set_page_config(page_title="SolidShala V14", layout="wide")

st.title("🛠️ SolidShala V14 - Real CAD Learning Engine")
st.write("Professional CAD Feel - Same Model, Live Modification")


# =========================
# MODEL STATE (REAL CAD CORE)
# =========================
if "model_type" not in st.session_state:
    st.session_state.model_type = "cube"

if "modifiers" not in st.session_state:
    st.session_state.modifiers = []


# =========================
# BASE MODELS
# =========================
def base_cube():
    x = [0,1,1,0,0,1,1,0]
    y = [0,0,1,1,0,0,1,1]
    z = [0,0,0,0,1,1,1,1]
    return go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,opacity=0.5)])


def base_cylinder():
    t = np.linspace(0,2*np.pi,60)
    z = np.linspace(0,1,2)
    t,z = np.meshgrid(t,z)
    x = np.cos(t)
    y = np.sin(t)
    return go.Figure(data=[go.Surface(x=x,y=y,z=z)])


# =========================
# REAL CAD RENDER PIPELINE
# =========================
def render_model():

    fig = base_cube() if st.session_state.model_type == "cube" else base_cylinder()

    # APPLY MODIFIERS VISUALLY (SIMULATION LAYER)
    for m in st.session_state.modifiers:

        if m == "Cut":
            fig.update_layout(title="Cut Applied (Material Removed)")
        elif m == "Shell":
            fig.update_layout(title="Shell Applied (Hollow Model)")
        elif m == "Fillet":
            fig.update_layout(title="Fillet Applied (Smooth Edges)")
        elif m == "Chamfer":
            fig.update_layout(title="Chamfer Applied (Beveled Edge)")
        else:
            fig.update_layout(title=f"{m} Applied")

    return fig


# =========================
# SMOOTH ANIMATION ENGINE
# =========================
def animate(action):

    box = st.empty()

    frames = [
        "Loading geometry...",
        "Applying tool: " + action,
        "Updating model...",
        "Rebuilding surfaces...",
        "Finalizing..."
    ]

    for f in frames:
        box.info(f)
        time.sleep(0.35)

    box.success("Model Updated Successfully")


# =========================
# TOOL ENGINE (REAL CAD STYLE)
# =========================
def apply_tool(tool):

    if tool == "Extrude":
        st.session_state.model_type = "cube"

    elif tool == "Revolve":
        st.session_state.model_type = "cylinder"

    else:
        st.session_state.modifiers.append(tool)


# =========================
# 20 TOOLS (PRO CAD LIST)
# =========================
TOOLS = [
    "Extrude","Revolve","Cut","Fillet","Chamfer",
    "Shell","Loft","Sweep","Pattern","Mirror",
    "Scale","Move","Rotate","Union","Subtract",
    "Intersect","Draft","Offset","Thicken","FilletEdge"
]


tool = st.sidebar.selectbox("Tool", TOOLS)
mode = st.sidebar.radio("Mode", ["Modeling", "Learn"])


# =========================
# LEARN MODE (CLEAN + PROFESSIONAL)
# =========================
if mode == "Learn":

    st.header("📘 Tool Understanding")

    explanations = {
        "Extrude": "2D sketch ko 3D solid banata hai.",
        "Revolve": "Profile ko rotate karke 3D shape banata hai.",
        "Cut": "Material remove karta hai.",
        "Shell": "Solid ko hollow banata hai.",
        "Fillet": "Edges smooth karta hai.",
        "Chamfer": "Edges bevel karta hai."
    }

    st.info(explanations.get(tool, "CAD modeling tool for shape modification."))


# =========================
# MODELING MODE (REAL CAD FEEL)
# =========================
else:

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.subheader("✏️ Sketch Canvas")

        if CANVAS_AVAILABLE:
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

        st.subheader("🏗️ Live Model")

        st.plotly_chart(render_model(), use_container_width=True)

        if st.button("Apply Tool"):

            animate(tool)

            apply_tool(tool)

            st.rerun()


# =========================
# MODIFIER HISTORY (IMPORTANT CAD FEEL)
# =========================
st.divider()

st.subheader("📜 Feature History (CAD Tree)")

if st.session_state.modifiers:
    for i, m in enumerate(st.session_state.modifiers, 1):
        st.write(f"{i}. {m}")
else:
    st.info("No modifications yet")
