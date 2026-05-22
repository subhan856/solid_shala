import streamlit as st
import time

st.set_page_config(page_title="SolidShala V5", layout="wide")

# =========================
# HEADER
# =========================
st.title("🛠️ SolidShala V5 - CAD Learning System")
st.write("Learn CAD like a visual game 🎮")

# =========================
# MODE SELECT
# =========================
mode = st.sidebar.radio("Select Mode", ["Learn Mode", "Practice Mode"])

tools = ["Extrude", "Revolve", "Cut", "Fillet", "Shell"]

# =========================
# ANIMATION FUNCTION (IMPORTANT)
# =========================
def animate_process(title, steps):
    placeholder = st.empty()
    st.subheader(title)

    for step in steps:
        placeholder.info(step)
        time.sleep(0.6)

    placeholder.success("Done ✅")

# =========================
# LEARN MODE
# =========================
if mode == "Learn Mode":

    st.header("📘 Learn CAD Tools")

    tool = st.selectbox("Select Tool", tools)

    st.markdown("---")

    if tool == "Extrude":
        st.write("2D shape → 3D solid (basic building block)")
        st.info("Example: box, brick, mobile body")

    elif tool == "Revolve":
        st.write("Shape rotates around axis → round object")
        st.info("Example: bottle, cup, cone")

    elif tool == "Cut":
        st.write("Material removal from solid")
        st.info("Example: hole drilling")

    elif tool == "Fillet":
        st.write("Sharp edges become smooth")
        st.info("Example: rounded corners")

    elif tool == "Shell":
        st.write("Solid becomes hollow")
        st.info("Example: cup, container")

    st.markdown("---")
    st.success("👉 Switch to Practice Mode to apply tools")

# =========================
# PRACTICE MODE
# =========================
elif mode == "Practice Mode":

    st.header("🛠️ Practice Lab")

    st.write("Step 1: Imagine sketch (canvas optional future upgrade)")
    st.write("Step 2: Apply tool")

    tool = st.selectbox("Choose Tool to Apply", tools)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Task")
        st.write(f"You selected: **{tool}**")
        st.write("Now watch how model is built step-by-step")

    with col2:
        st.subheader("⚙️ Action")

        if st.button("🚀 Build Model"):

            # =====================
            # EXTRUDE ANIMATION
            # =====================
            if tool == "Extrude":
                animate_process(
                    "Extrusion Process",
                    [
                        "Sketch detected...",
                        "Base profile created...",
                        "Material rising...",
                        "Solid forming...",
                        "3D box ready"
                    ]
                )

            # =====================
            # REVOLVE ANIMATION
            # =====================
            elif tool == "Revolve":
                animate_process(
                    "Revolve Process",
                    [
                        "Axis detected...",
                        "Profile selected...",
                        "Rotation started...",
                        "Shape forming...",
                        "Cylinder ready"
                    ]
                )

            # =====================
            # CUT
            # =====================
            elif tool == "Cut":
                animate_process(
                    "Cut Process",
                    [
                        "Target solid loaded...",
                        "Sketch for cut defined...",
                        "Removing material...",
                        "Hole created..."
                    ]
                )

            # =====================
            # FILLET
            # =====================
            elif tool == "Fillet":
                animate_process(
                    "Fillet Process",
                    [
                        "Edges detected...",
                        "Radius applied...",
                        "Smoothing corners...",
                        "Model softened..."
                    ]
                )

            # =====================
            # SHELL
            # =====================
            elif tool == "Shell":
                animate_process(
                    "Shell Process",
                    [
                        "Solid detected...",
                        "Thickness setting applied...",
                        "Removing inner material...",
                        "Hollow model created..."
                    ]
                )

    st.info("💡 Ye animation learning feel create karta hai (SolidWorks style concept)")
