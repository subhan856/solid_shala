import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False


st.set_page_config(page_title="SolidShala V13", layout="wide")

st.title("🛠️ SolidShala V13 - CAD GAME LEARNING ENGINE")
st.write("🎮 Build Real Products Step-by-Step (Like a Game)")


# =========================
# SESSION STATE (GAME ENGINE)
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "product" not in st.session_state:
    st.session_state.product = "Bottle"

if "history" not in st.session_state:
    st.session_state.history = []

if "score" not in st.session_state:
    st.session_state.score = 0


# =========================
# PRODUCTS (MISSIONS)
# =========================
PRODUCTS = {
    "Bottle": ["Sketch Circle", "Revolve", "Shell", "Fillet Finish"],
    "Box": ["Sketch Square", "Extrude", "Cut Hole", "Chamfer Finish"],
    "Stand": ["Sketch Base", "Extrude", "Cut Slot", "Fillet Finish"]
}


# =========================
# 3D MODELS
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


def render_model():
    if st.session_state.product == "Bottle":
        return cylinder()
    return cube()


# =========================
# ANIMATION ENGINE (IMPORTANT)
# =========================
def animate(text):
    box = st.empty()

    steps = [
        "Analyzing sketch...",
        text,
        "Applying transformation...",
        "Updating model...",
        "Done ✅"
    ]

    for s in steps:
        box.info(s)
        time.sleep(0.3)

    box.success("Step Completed 🎯")


# =========================
# TOOL SIMULATION ENGINE
# =========================
def apply_step(step_name):

    if "Sketch" in step_name:
        st.session_state.score += 1

    elif "Extrude" in step_name:
        st.session_state.score += 2

    elif "Revolve" in step_name:
        st.session_state.score += 2

    elif "Cut" in step_name:
        st.session_state.score += 3

    elif "Shell" in step_name:
        st.session_state.score += 3

    elif "Fillet" in step_name:
        st.session_state.score += 1

    st.session_state.history.append(step_name)


# =========================
# SIDEBAR (GAME CONTROL)
# =========================
st.sidebar.header("🎮 Game Panel")

st.session_state.product = st.sidebar.selectbox("Select Product Mission", list(PRODUCTS.keys()))

step_list = PRODUCTS[st.session_state.product]

st.sidebar.write("📌 Steps:")
for i, s in enumerate(step_list, 1):
    st.sidebar.write(f"{i}. {s}")

st.sidebar.metric("⭐ Score", st.session_state.score)


# =========================
# MAIN GAME UI
# =========================
col1, col2 = st.columns([1,1])


# =========================
# CANVAS (MAIN INPUT)
# =========================
with col1:

    st.subheader("✏️ Sketch Area")

    if CANVAS_AVAILABLE:
        canvas = st_canvas(
            fill_color="rgba(0, 0, 255, 0.2)",
            stroke_width=3,
            stroke_color="#000",
            background_color="#fff",
            height=350,
            drawing_mode="freedraw",
            key="canvas"
        )
    else:
        st.warning("Install streamlit-drawable-canvas")


# =========================
# MODEL VIEW + GAME ACTION
# =========================
with col2:

    st.subheader("🏗️ Live Product Builder")

    st.plotly_chart(render_model(), use_container_width=True)

    if st.session_state.step < len(step_list):

        current_step = step_list[st.session_state.step]

        st.info(f"Next Step: {current_step}")

        if st.button("▶ Apply Step"):

            animate(current_step)

            apply_step(current_step)

            st.session_state.step += 1

            st.rerun()

    else:
        st.success("🎉 Product Completed!")

        st.balloons()


# =========================
# HISTORY SYSTEM (REPLAY FEEL)
# =========================
st.divider()

st.subheader("📜 Build History")

if st.session_state.history:
    for i, h in enumerate(st.session_state.history, 1):
        st.write(f"Step {i}: {h}")
else:
    st.info("No steps yet")
