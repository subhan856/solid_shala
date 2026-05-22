import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

st.set_page_config(page_title="SolidShala V2", layout="wide")

st.title("🛠️ SolidShala V2 - CAD Learning Simulator")

# Sidebar
menu = st.sidebar.radio(
    "Choose Tool",
    ["Home", "Tool 1: Lamba Karo", "Tool 2: Ghumao Karo", "Progress"]
)

# ========================
# HOME
# ========================
if menu == "Home":
    st.write("Welcome 🚀")
    st.write("Yahan tum CAD tools ko drawing + action se seekhoge")

# ========================
# TOOL 1 - EXTRUDE
# ========================
elif menu == "Tool 1: Lamba Karo":

    st.header("📘 Lamba Karo (Extrude Feel)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("✏️ Draw Sketch")

        st_canvas(
            fill_color="rgba(0,255,0,0.3)",
            stroke_width=3,
            height=300,
            width=300,
            drawing_mode="rect",
            key="canvas1"
        )

    with col2:
        st.subheader("⚙️ Controls")

        length = st.slider("Length", 10, 100, 50)
        width = st.slider("Width", 10, 100, 30)
        height = st.slider("Height", 1, 50, 10)

        if st.button("🚀 Lamba Karo"):

            st.write("Step 1: Sketch ready...")
            time.sleep(0.5)

            st.write("Step 2: Extrusion start...")
            time.sleep(0.5)

            st.write("Step 3: Material add ho raha hai...")
            time.sleep(0.5)

            st.success("✅ 3D Box Ready!")

            st.balloons()

    with col3:
        st.subheader("📦 Result")

        st.info("Ye ek simple 3D box hai jo extrusion se bana")

        st.write(f"Length: {length}")
        st.write(f"Width: {width}")
        st.write(f"Height: {height}")

# ========================
# TOOL 2 - REVOLVE
# ========================
elif menu == "Tool 2: Ghumao Karo":

    st.header("🔄 Ghumao Karo (Revolve Feel)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("✏️ Profile")

        st_canvas(
            fill_color="rgba(255,0,0,0.3)",
            stroke_width=3,
            height=300,
            width=300,
            drawing_mode="circle",
            key="canvas2"
        )

    with col2:
        st.subheader("⚙️ Action")

        shape = st.selectbox("Select Object", ["Bottle", "Cup", "Cone"])

        if st.button("🔄 Ghumao Karo"):

            st.write("Step 1: Profile detect ho raha hai...")
            time.sleep(0.5)

            st.write("Step 2: Axis set ho rahi hai...")
            time.sleep(0.5)

            st.write("Step 3: 360° rotation...")
            time.sleep(0.5)

            st.success(f"✅ {shape} Ready!")

            st.balloons()

    with col3:
        st.subheader("📦 Result")

        if shape == "Bottle":
            st.info("Thin curved profile → bottle shape")
        elif shape == "Cup":
            st.info("Hollow revolve → cup shape")
        else:
            st.info("Tapered revolve → cone shape")

# ========================
# PROGRESS
# ========================
elif menu == "Progress":

    st.header("📈 Progress Tracker")

    st.progress(0.5)

    st.write("✔ Tool 1 done")
    st.write("✔ Tool 2 done (basic)")
    st.write("🔒 Tool 3 coming soon")

    st.success("Keep going 🔥")
