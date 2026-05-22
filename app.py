import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="SolidShala Final Pro", layout="wide")

st.title("🛠️ SolidShala Final Pro - CAD Learning Simulator")
st.write("Sketch → Model → Tools → Live CAD Simulation")

# =========================
# SAFE SESSION STATE INIT
# =========================
if "model" not in st.session_state or st.session_state.model is None:
    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "height": 1.0,
        "width": 1.0,
        "cut": 0.0,
        "features": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# MODEL CREATION (SKETCH)
# =========================
def create_circle():
    m = st.session_state.model
    m["shape"] = "circle"
    m["radius"] = 1.0
    m["height"] = 1.0
    st.session_state.model = m

def create_square():
    m = st.session_state.model
    m["shape"] = "square"
    m["width"] = 1.0
    m["height"] = 1.0
    st.session_state.model = m

# =========================
# RENDER ENGINE (LIVE MODEL)
# =========================
def render_model():

    m = st.session_state.model

    if m["shape"] == "circle":

        t = np.linspace(0, 2*np.pi, 80)
        z = np.linspace(0, m["height"], 2)
        t, z = np.meshgrid(t, z)

        x = m["radius"] * np.cos(t)
        y = m["radius"] * np.sin(t)

        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])

    elif m["shape"] == "square":

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]
        z = [0,0,0,0,m["height"],m["height"],m["height"],m["height"]]

        fig = go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,opacity=0.5)])

    else:
        fig = go.Figure()
        fig.add_annotation(text="Create Sketch First", showarrow=False)

    fig.update_layout(margin=dict(l=0,r=0,t=40,b=0))
    return fig

# =========================
# ANIMATION ENGINE
# =========================
def animate(tool):

    box = st.empty()

    steps = [
        "Reading sketch...",
        f"Applying {tool}...",
        "Updating geometry...",
        "Rebuilding model...",
        "Done ✅"
    ]

    for s in steps:
        box.info(s)
        time.sleep(0.2)

    box.success(f"{tool} applied")

# =========================
# TOOL ENGINE (REAL PARAMETRIC LOGIC)
# =========================
def apply_tool(tool):

    m = st.session_state.model

    if tool == "Extrude":
        m["height"] += 0.5

    elif tool == "Cut":
        m["height"] -= 0.3
        m["cut"] += 0.3

    elif tool == "Shell":
        m["cut"] += 0.5

    elif tool == "Fillet":
        m["radius"] *= 1.05

    elif tool == "Chamfer":
        m["width"] *= 0.95

    elif tool == "Scale":
        m["height"] *= 1.1
        m["radius"] *= 1.1

    elif tool == "Revolve":
        m["shape"] = "circle"

    else:
        m["features"].append(tool)

    st.session_state.history.append({
        "tool": tool,
        "time": str(datetime.now())
    })

    st.session_state.model = m

# =========================
# TOOLS (20 CAD TOOLS)
# =========================
TOOLS = [
    "Extrude","Revolve","Cut","Shell","Fillet",
    "Chamfer","Scale","Move","Rotate","Mirror",
    "Pattern","Loft","Sweep","Union","Subtract",
    "Intersect","Offset","Thicken","Draft","Reset"
]

# =========================
# SIDEBAR
# =========================
tool = st.sidebar.selectbox("Select Tool", TOOLS)

shape = st.sidebar.selectbox("Sketch Shape", ["circle","square"])

if st.sidebar.button("Create Sketch"):
    if shape == "circle":
        create_circle()
    else:
        create_square()
    st.success("Sketch Created")

# =========================
# MAIN UI
# =========================
col1, col2 = st.columns([1.2,1])

with col1:

    st.subheader("✏️ Sketch Input")
    st.info("Parametric CAD Sketch System")

    st.subheader("🏗️ Live Model")
    st.plotly_chart(render_model(), use_container_width=True)

    if st.button("Apply Tool"):

        if st.session_state.model["shape"] is None:
            st.warning("Pehle sketch create karo")
        else:
            animate(tool)
            apply_tool(tool)
            st.rerun()

with col2:

    st.subheader("📏 AI Dimensions Panel")

    m = st.session_state.model

    st.write("Shape:", m["shape"])
    st.write("Radius:", m["radius"])
    st.write("Height:", m["height"])
    st.write("Cut:", m["cut"])

    st.subheader("⚙️ Features")
    for f in m["features"]:
        st.write("•", f)

# =========================
# HISTORY
# =========================
st.divider()

st.subheader("📜 CAD History")

for h in st.session_state.history:
    st.write(h["tool"], "|", h["time"])
