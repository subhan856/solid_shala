import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="SolidShala V4", layout="wide")

# =========================
# TITLE
# =========================
st.title("🛠️ SolidShala V4")
st.write("Learn CAD step-by-step like a game 🎮")

# =========================
# MODE SELECT
# =========================
mode = st.sidebar.radio(
    "🎯 Select Mode",
    ["Learn Mode", "Practice Mode"]
)

# =========================
# LEARN MODE
# =========================
if mode == "Learn Mode":

    st.header("📘 Learn CAD Tools")

    tool = st.selectbox(
        "Tool select karo",
        ["Extrude", "Revolve", "Cut", "Fillet", "Shell"]
    )

    st.write("### Concept Explanation")

    if tool == "Extrude":
        st.write("2D shape ko 3D solid me convert karta hai")
        st.info("Example: box, brick, mobile body")
        st.image("https://i.imgur.com/8Q1zQyO.png")

    elif tool == "Revolve":
        st.write("Shape ko axis ke around ghumata hai")
        st.info("Example: bottle, cup, cone")
        st.image("https://i.imgur.com/0Z8QZ9h.png")

    elif tool == "Cut":
        st.write("Material remove karta hai")
        st.info("Example: hole in block")

    elif tool == "Fillet":
        st.write("Sharp edges ko round karta hai")
        st.info("Example: smooth corners")

    elif tool == "Shell":
        st.write("Solid ko hollow banata hai")
        st.info("Example: cup, container")

    st.success("👉 Ab Practice Mode try karo")

# =========================
# PRACTICE MODE
# =========================
elif mode == "Practice Mode":

    st.header("🛠️ Practice Area")

    col1, col2 = st.columns(2)

    # =====================
    # DRAW AREA
    # =====================
    with col1:

        st.subheader("✏️ Sketch Area")

        canvas = st_canvas(
            fill_color="rgba(0,255,0,0.3)",
            stroke_width=3,
            height=400,
            width=400,
            drawing_mode="rect",
            key="canvas_practice"
        )

    # =====================
    # TOOL AREA
    # =====================
    with col2:

        st.subheader("⚙️ Apply Tool")

        tool = st.selectbox(
            "Tool select karo",
            ["Extrude", "Revolve", "Cut", "Fillet", "Shell"]
        )

        if st.button("🚀 Apply Tool"):

            st.write("Processing your sketch...")

            if tool == "Extrude":
                st.success("3D Box created 🔥 (Extrude Applied)")

            elif tool == "Revolve":
                st.success("Cylinder created 🔥 (Revolve Applied)")

            elif tool == "Cut":
                st.success("Hole created 🔥 (Cut Applied)")

            elif tool == "Fillet":
                st.success("Edges rounded 🔥 (Fillet Applied)")

            elif tool == "Shell":
                st.success("Object hollowed 🔥 (Shell Applied)")

            st.balloons()

    st.info("👉 Pehle draw karo, phir tool apply karo")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("💡 SolidShala - Learn CAD in simple way")
