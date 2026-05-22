import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

st.set_page_config(page_title="SolidShala V6", layout="wide")

st.title("🛠️ SolidShala V6 - Interactive CAD Learning")

# =========================
# SIDEBAR MODE
# =========================
mode = st.sidebar.radio("Select Mode", ["Learn Mode", "Practice Mode"])

tools = ["Extrude", "Revolve", "Cut", "Fillet", "Shell"]

# =========================
# SAFE ANIMATION FUNCTION
# =========================
def show_animation(title, steps):
    st.subheader(title)
    box = st.empty()

    for s in steps:
        box.info(s)
        time.sleep(0.5)

    box.success("Model Ready ✅")

# =========================
# LEARN MODE
# =========================
if mode == "Learn Mode":

    st.header("📘 Learn CAD Tools")

    tool = st.selectbox("Select Tool", tools)

    st.markdown("---")

    if tool == "Extrude":
        st.write("2D → 3D solid banata hai")
        st.info("Example: box, brick")

    elif tool == "Revolve":
        st.write("Shape ko rotate karke 3D banata hai")
        st.info("Example: bottle, cup")

    elif tool == "Cut":
        st.write("Material remove karta hai")
        st.info("Example: hole")

    elif tool == "Fillet":
        st.write("Edges smooth karta hai")

    elif tool == "Shell":
        st.write("Solid ko hollow banata hai")

# =========================
# PRACTICE MODE (FIXED)
# =========================
elif mode == "Practice Mode":

    st.header("🛠️ Practice Lab")

    tool = st.selectbox("Choose Tool", tools)

    col1, col2 = st.columns(2)

    # =========================
    # CANVAS (FIXED KEY ISSUE)
    # =========================
    with col1:
        st.subheader("✏️ Draw Sketch")

        canvas = st_canvas(
            fill_color="rgba(0, 255, 0, 0.2)",
            stroke_width=3,
            height=350,
            width=350,
            drawing_mode="rect",
            key=f"canvas_{tool}"   # ✅ IMPORTANT FIX
        )

        if canvas.image_data is not None:
            st.caption("Sketch captured ✔")

    # =========================
    # ACTION PANEL
    # =========================
    with col2:

        st.subheader("⚙️ Tool Action")

        if st.button("🚀 Apply Tool", key=f"btn_{tool}"):

            # =========================
            # EXTRUDE
            # =========================
            if tool == "Extrude":

                show_animation(
                    "Extrusion Process",
                    [
                        "Sketch detect ho raha hai...",
                        "Profile analyze ho raha hai...",
                        "Height generate ho rahi hai...",
                        "3D solid build ho raha hai..."
                    ]
                )

                st.success("📦 Final Product: BOX CREATED")

            # =========================
            # REVOLVE
            # =========================
            elif tool == "Revolve":

                show_animation(
                    "Revolve Process",
                    [
                        "Axis detect ho raha hai...",
                        "Profile rotate ho raha hai...",
                        "Surface generate ho rahi hai...",
                        "3D shape ready..."
                    ]
                )

                st.success("🍶 Final Product: CYLINDER CREATED")

            # =========================
            # CUT
            # =========================
            elif tool == "Cut":

                show_animation(
                    "Cut Process",
                    [
                        "Solid load ho raha hai...",
                        "Sketch apply ho raha hai...",
                        "Material remove ho raha hai...",
                        "Hole create ho gaya..."
                    ]
                )

                st.success("🕳️ Final Product: CUT DONE")

            # =========================
            # FILLET
            # =========================
            elif tool == "Fillet":

                show_animation(
                    "Fillet Process",
                    [
                        "Edges detect ho rahi hain...",
                        "Radius apply ho raha hai...",
                        "Smooth transition ban raha hai..."
                    ]
                )

                st.success("🔵 Final Product: SMOOTH MODEL")

            # =========================
            # SHELL
            # =========================
            elif tool == "Shell":

                show_animation(
                    "Shell Process",
                    [
                        "Solid analyze ho raha hai...",
                        "Thickness set ho rahi hai...",
                        "Inner material remove ho raha hai...",
                        "Hollow object ready..."
                    ]
                )

                st.success("🥤 Final Product: HOLLOW OBJECT")

    st.info("👉 Ab ye app step-by-step CAD feel deta hai (no duplicate error)")
