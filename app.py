import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="SolidShala", layout="wide")

# ========================
# TITLE
# ========================
st.title("🛠️ SolidShala")
st.subheader("Learn CAD Concepts in Simple Way")

# ========================
# SIDEBAR
# ========================
menu = st.sidebar.radio(
    "Choose",
    ["Home", "Tool 1: Lamba Karo", "Progress"]
)

# ========================
# HOME
# ========================
if menu == "Home":
    st.write("Welcome to SolidShala 🚀")
    st.write("Yahan tum CAD tools ko easy way me seekhoge.")

# ========================
# TOOL 1
# ========================
elif menu == "Tool 1: Lamba Karo":

    st.header("📘 Tool 1: Lamba Karo (Extrude Concept)")

    st.write("Ye tool 2D shape ko 3D object me convert karta hai.")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2D Sketch")

        st_canvas(
            fill_color="rgba(0, 255, 0, 0.3)",
            stroke_width=3,
            stroke_color="#ffffff",
            background_color="#1e293b",
            height=300,
            width=400,
            drawing_mode="rect",
            key="canvas",
        )

    with col2:
        st.subheader("3D Controls")

        length = st.slider("Length", 10, 100, 50)
        width = st.slider("Width", 10, 100, 30)
        height = st.slider("Height", 1, 50, 10)

        if st.button("🚀 Lamba Karo"):

            st.success("✅ 3D Box Ready!")

            st.write("### Dimensions")
            st.write("Length:", length)
            st.write("Width:", width)
            st.write("Height:", height)

            st.info("Socho ye ek real mechanical part hai 🔥")

            st.balloons()

    # Quiz
    st.markdown("---")
    st.subheader("🧠 Viva Test")

    q = st.radio(
        "Bottle banane ke liye kaunsa tool use hoga?",
        ["Lamba Karo", "Ghumao Karo"]
    )

    if st.button("Check Answer"):
        if q == "Ghumao Karo":
            st.success("Correct! Bottle gol hoti hai.")
        else:
            st.error("Galat! Bottle revolved shape hoti hai.")

# ========================
# PROGRESS
# ========================
elif menu == "Progress":

    st.header("📈 Progress")

    progress = 33

    st.progress(progress / 100)

    st.write("✔ Tool 1 Completed")
    st.write("🔒 Tool 2 Locked")

    st.success("Roz practice karo 🔥")
