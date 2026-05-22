import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

st.set_page_config(page_title="SolidShala V6", layout="wide")

# =========================
# TITLE
# =========================
st.title("🛠️ SolidShala V6 - Real CAD Feel System")
st.write("Sketch karo → Model banta dekho 🎮")

# =========================
# MODE
# =========================
mode = st.sidebar.radio("Select Mode", ["Learn Mode", "Practice Mode"])

tools = ["Extrude", "Revolve", "Cut", "Fillet", "Shell"]

# =========================
# ANIMATION ENGINE (REAL FEEL)
# =========================
def run_animation(name, steps):
    box = st.empty()
    st.subheader(f"⚙️ {name}")

    for i, s in enumerate(steps):
        box.info(f"Step {i+1}: {s}")
        time.sleep(0.7)

    box.success("✔ Model Ready!")

# =========================
# LEARN MODE
# =========================
if mode == "Learn Mode":

    st.header("📘 Learn CAD Tools")

    tool = st.selectbox("Tool choose karo", tools)

    st.markdown("---")

    if tool == "Extrude":
        st.write("👉 2D shape ko 3D solid me convert karta hai")
        st.image("https://i.imgur.com/8Q1zQyO.png")

    elif tool == "Revolve":
        st.write("👉 Shape ko ghumakar round object banata hai")

    elif tool == "Cut":
        st.write("👉 Solid me se material remove karta hai")

    elif tool == "Fillet":
        st.write("👉 Sharp edges ko smooth banata hai")

    elif tool == "Shell":
        st.write("👉 Solid ko hollow banata hai")

    st.success("Switch to Practice Mode 🚀")

# =========================
# PRACTICE MODE
# =========================
elif mode == "Practice Mode":

    st.header("🛠️ Practice CAD Lab")

    col1, col2 = st.columns(2)

    # =========================
    # SKETCH AREA
    # =========================
    with col1:

        st.subheader("✏️ Draw Your Sketch")

        canvas_result = st_canvas(
            fill_color="rgba(0, 255, 0, 0.2)",
            stroke_width=3,
            background_color="#ffffff",
            height=400,
            width=400,
            drawing_mode="rect",
            key="canvas"
        )

        if canvas_result.image_data is not None:
            st.caption("📌 Sketch captured ✔")

    # =========================
    # TOOL AREA
    # =========================
    with col2:

        st.subheader("⚙️ Apply Tool")

        tool = st.selectbox("Select Tool", tools)

        st.write("👉 Pehle sketch banao, phir tool apply karo")

        if st.button("🚀 Build 3D Model"):

            # EXTRUDE
            if tool == "Extrude":
                run_animation("Extrusion Process", [
                    "Sketch detect ho raha hai",
                    "Profile lock ho rahi hai",
                    "Material rise ho raha hai",
                    "3D shape form ho rahi hai"
                ])

            # REVOLVE
            elif tool == "Revolve":
                run_animation("Revolve Process", [
                    "Axis detect ho raha hai",
                    "Profile attach ho rahi hai",
                    "Rotation start",
                    "Round body create ho rahi hai"
                ])

            # CUT
            elif tool == "Cut":
                run_animation("Cut Process", [
                    "Target solid load ho raha hai",
                    "Cut profile detect",
                    "Material remove ho raha hai",
                    "Hole create ho gaya"
                ])

            # FILLET
            elif tool == "Fillet":
                run_animation("Fillet Process", [
                    "Edges detect ho rahi hain",
                    "Radius apply ho raha hai",
                    "Corners smooth ho rahe hain"
                ])

            # SHELL
            elif tool == "Shell":
                run_animation("Shell Process", [
                    "Solid analyze ho raha hai",
                    "Thickness apply ho rahi hai",
                    "Inner material remove",
                    "Hollow model ready"
                ])

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("💡 SolidShala V6 - From Sketch to Engineering Mind")
