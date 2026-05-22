import streamlit as st
import numpy as np
import time
from streamlit_drawable_canvas import st_canvas
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title="SolidShala V6", layout="wide")

st.title("🛠️ SolidShala V6 - Real CAD Feel Simulator")
st.write("Sketch → Animate → 3D Model → Final Product 🔥")

# =========================
# SIDEBAR MODE
# =========================
mode = st.sidebar.radio("Select Mode", ["Learn + Build Mode"])

tool = st.sidebar.selectbox(
    "Select Tool",
    ["Extrude", "Revolve (Basic)", "Cut (Basic)"]
)

# =========================
# IMAGE UPLOAD (NEW FEATURE)
# =========================
st.sidebar.subheader("📷 Reference Image (Optional)")
img_file = st.sidebar.file_uploader("Upload product image")

if img_file:
    image = Image.open(img_file)
    st.sidebar.image(image, caption="Reference")

# =========================
# CANVAS
# =========================
st.subheader("✏️ Step 1: Sketch Area")

canvas = st_canvas(
    fill_color="rgba(0, 255, 0, 0.2)",
    stroke_width=3,
    height=400,
    width=400,
    drawing_mode="rect",
    key="canvas"
)

# =========================
# EXTRUDE FUNCTION (REAL FEEL ANIMATION)
# =========================
def extrude_animation(height):

    placeholder = st.empty()

    for i in range(1, 11):

        h = height * (i / 10)

        # simple box model growing
        x = [0, 1, 1, 0, 0, 1, 1, 0]
        y = [0, 0, 1, 1, 0, 0, 1, 1]
        z = [0, 0, 0, 0, h, h, h, h]

        fig = go.Figure(data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                opacity=0.6
            )
        ])

        fig.update_layout(
            scene=dict(aspectmode="data"),
            margin=dict(l=0, r=0, t=0, b=0)
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.2)

    return fig

# =========================
# REVOLVE SIMULATION
# =========================
def revolve_animation():

    placeholder = st.empty()

    for i in range(1, 11):

        theta = np.linspace(0, 2*np.pi*i/10, 30)
        z = np.linspace(0, 2, 2)

        theta_grid, z_grid = np.meshgrid(theta, z)

        r = 1
        x = r * np.cos(theta_grid)
        y = r * np.sin(theta_grid)

        fig = go.Figure(data=[
            go.Surface(x=x, y=y, z=z_grid, opacity=0.7)
        ])

        fig.update_layout(scene=dict(aspectmode="data"))

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.2)

    return fig

# =========================
# MAIN ACTION BUTTON
# =========================
st.subheader("⚙️ Step 2: Build Model")

if st.button("🚀 Generate 3D Model"):

    st.info("Processing sketch...")

    # default height
    height = 3

    # TOOL LOGIC
    if tool == "Extrude":
        final_model = extrude_animation(height)

    elif tool == "Revolve (Basic)":
        final_model = revolve_animation()

    elif tool == "Cut (Basic)":
        st.warning("Cut simulation (simple demo)")
        final_model = extrude_animation(2)
        st.error("Hole created (simulation)")

    # =========================
    # FINAL OUTPUT
    # =========================
    st.success("✅ Final Product Ready")

    st.subheader("🏁 Final Model View")
    st.plotly_chart(final_model, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("💡 SolidShala V6 - Learning CAD Like a Game Engine")
