import streamlit as st
from streamlit_drawable_canvas import st_canvas
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="SolidShala V3", layout="wide")

# =========================
# TITLE
# =========================
st.title("🛠️ SolidShala V3 - CAD Learning Simulator")
st.write("Learn CAD like a game 🎮")

# =========================
# 3D FUNCTIONS
# =========================
def draw_box(l, w, h):
    x = [0, l, l, 0, 0, l, l, 0]
    y = [0, 0, w, w, 0, 0, w, w]
    z = [0, 0, 0, 0, h, h, h, h]

    fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, opacity=0.5)])
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig


def draw_cylinder(r, h):
    theta = np.linspace(0, 2*np.pi, 30)
    z = np.linspace(0, h, 2)
    theta_grid, z_grid = np.meshgrid(theta, z)

    x = r * np.cos(theta_grid)
    y = r * np.sin(theta_grid)

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z_grid)])
    fig.update_layout(scene=dict(aspectmode='data'))
    return fig


# =========================
# SIDEBAR MENU (5 TOOLS)
# =========================
menu = st.sidebar.radio(
    "🎯 Select Tool",
    [
        "Home",
        "Tool 1: Lamba Karo (Extrude)",
        "Tool 2: Ghumao Karo (Revolve)",
        "Tool 3: Kato Karo (Cut)",
        "Tool 4: Gol Kona (Fillet)",
        "Tool 5: Engineer Test",
    ]
)

# =========================
# HOME
# =========================
if menu == "Home":
    st.header("Welcome 🚀")
    st.write("Ye app tumhe CAD tools simple way me sikhayega")
    st.info("Tool select karo aur start karo")

# =========================
# TOOL 1 - EXTRUDE
# =========================
elif menu == "Tool 1: Lamba Karo (Extrude)":

    st.header("📦 Tool 1: Lamba Karo")

    col1, col2 = st.columns(2)

    with col1:
        st_canvas(
            fill_color="rgba(0,255,0,0.3)",
            stroke_width=3,
            height=300,
            width=300,
            drawing_mode="rect",
            key="t1"
        )

    with col2:
        l = st.slider("Length", 10, 100, 50)
        w = st.slider("Width", 10, 100, 30)
        h = st.slider("Height", 1, 50, 10)

        if st.button("🚀 Lamba Karo"):
            st.success("Extrusion started...")
            fig = draw_box(l, w, h)
            st.plotly_chart(fig)
            st.balloons()

# =========================
# TOOL 2 - REVOLVE
# =========================
elif menu == "Tool 2: Ghumao Karo (Revolve)":

    st.header("🔄 Tool 2: Ghumao Karo")

    col1, col2 = st.columns(2)

    with col1:
        st_canvas(
            fill_color="rgba(255,0,0,0.3)",
            stroke_width=3,
            height=300,
            width=300,
            drawing_mode="circle",
            key="t2"
        )

    with col2:
        r = st.slider("Radius", 5, 50, 10)
        h = st.slider("Height", 10, 100, 50)

        if st.button("🔄 Ghumao Karo"):
            st.success("Revolve started...")
            fig = draw_cylinder(r, h)
            st.plotly_chart(fig)
            st.balloons()

# =========================
# TOOL 3 - CUT
# =========================
elif menu == "Tool 3: Kato Karo (Cut)":

    st.header("✂️ Tool 3: Cut Feature")

    base = st.slider("Base Size", 10, 100, 50)
    cut = st.slider("Cut Depth", 1, 50, 10)

    if st.button("✂️ Cut Apply"):

        st.success("Hole created in model")
        fig = draw_box(base, base, base - cut)
        st.plotly_chart(fig)

# =========================
# TOOL 4 - FILLET
# =========================
elif menu == "Tool 4: Gol Kona (Fillet)":

    st.header("🔵 Tool 4: Fillet")

    st.write("Sharp edges → rounded edges concept")

    if st.button("🔵 Apply Fillet"):
        st.success("Edges rounded!")
        fig = draw_box(50, 50, 50)
        st.plotly_chart(fig)

# =========================
# TOOL 5 - ENGINEER TEST
# =========================
elif menu == "Tool 5: Engineer Test":

    st.header("🧠 Engineer Challenge")

    q = st.radio(
        "Bottle kis tool se banegi?",
        ["Extrude", "Revolve", "Cut"]
    )

    if st.button("Check"):

        if q == "Revolve":
            st.success("Correct! Bottle revolve se banti hai 🔥")
        else:
            st.error("Wrong answer. Soch real shape!")

        st.info("Practice makes engineer 💡")
