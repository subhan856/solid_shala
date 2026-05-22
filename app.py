import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="SolidShala V6", layout="wide")

st.title("🛠️ SolidShala V6 - Learning Engine")
st.write("Sketch → Animate → 3D Model → Quiz")

# =========================
# TOOL DATABASE (SCALABLE)
# =========================
TOOLS = {
    "Extrude": {
        "desc": "2D shape ko 3D solid banata hai",
        "quiz": [
            ("Extrude kya karta hai?", "2D → 3D"),
            ("Example?", "Box"),
        ]
    },
    "Revolve": {
        "desc": "Shape ko rotate karke 3D banata hai",
        "quiz": [
            ("Revolve kya banata hai?", "Cylinder"),
            ("Best example?", "Bottle"),
        ]
    },
    "Cut": {
        "desc": "Material remove karta hai",
        "quiz": [
            ("Cut kya karta hai?", "Material remove"),
        ]
    }
}

# =========================
# 3D FUNCTIONS
# =========================
def box():
    x = [0,1,1,0,0,1,1,0]
    y = [0,0,1,1,0,0,1,1]
    z = [0,0,0,0,1,1,1,1]
    fig = go.Figure(data=[go.Mesh3d(x=x,y=y,z=z,opacity=0.5)])
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig

def cylinder():
    t = np.linspace(0,2*np.pi,30)
    z = np.linspace(0,1,2)
    t,z = np.meshgrid(t,z)
    x = np.cos(t)
    y = np.sin(t)
    fig = go.Figure(data=[go.Surface(x=x,y=y,z=z)])
    return fig

# =========================
# ANIMATION ENGINE
# =========================
def animate(texts):
    box = st.empty()
    for t in texts:
        box.info(t)
        time.sleep(0.5)
    box.success("Model Ready ✅")

# =========================
# SIDEBAR
# =========================
mode = st.sidebar.radio("Mode", ["Learn Mode", "Practice Mode"])
tool = st.sidebar.selectbox("Tool", list(TOOLS.keys()))

# =========================
# LEARN MODE
# =========================
if mode == "Learn Mode":

    st.header(f"📘 {tool} Learning")

    st.write(TOOLS[tool]["desc"])

    st.markdown("### Quiz")

    for q, a in TOOLS[tool]["quiz"]:
        st.write(f"❓ {q}")
        st.write(f"👉 {a}")

# =========================
# PRACTICE MODE
# =========================
else:

    st.header("🛠️ Practice Lab")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✏️ Sketch Area")
        st.write("Canvas (future upgrade AI sketch detection)")
        st.empty()

    with col2:
        st.subheader("⚙️ Action")

        if st.button("🚀 Build Model"):

            if tool == "Extrude":

                animate([
                    "Sketch detected...",
                    "Extruding shape...",
                    "Height increasing...",
                    "Solid forming..."
                ])

                fig = box()
                st.plotly_chart(fig, key="extrude_model")

            elif tool == "Revolve":

                animate([
                    "Axis detected...",
                    "Rotating profile...",
                    "Generating surface..."
                ])

                fig = cylinder()
                st.plotly_chart(fig, key="revolve_model")

            elif tool == "Cut":

                animate([
                    "Material loading...",
                    "Cutting volume...",
                    "Hole created..."
                ])

                st.success("Cut Applied")

    st.info("👉 Ye engine scalable hai (20 tools easily add ho sakte hain)")
