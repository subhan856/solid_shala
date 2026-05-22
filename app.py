import streamlit as st
import cadquery as cq
from streamlit_drawable_canvas import st_canvas
import os

st.set_page_config(
    page_title="SolidShala",
    page_icon="🛠️",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

.block {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🛠️ SolidShala")
st.sidebar.write("Mechanical Learning System")

page = st.sidebar.radio(
    "Choose Section",
    [
        "🏠 Home",
        "📘 Tool 1 - Lamba Karo",
        "🤖 Ustaad AI",
        "📈 Progress"
    ]
)

# =========================
# HOME PAGE
# =========================
if page == "🏠 Home":

    st.title("🛠️ SolidShala")
    st.subheader("Learn CAD Like a Real Engineer")

    st.markdown("""
    ### Tum yahan kya seekhoge?

    - CAD tools ka REAL use
    - Products kis tarah bante hain
    - 2D se 3D sochna
    - Engineer ki aankh develop karna
    - Beginner-friendly SolidWorks concepts
    """)

    st.success("Start karo: Tool 1 → Lamba Karo")

# =========================
# TOOL 1
# =========================
elif page == "📘 Tool 1 - Lamba Karo":

    st.title("📘 Tool 1: Lamba Karo")
    st.caption("Asli Naam: Extrude Boss/Base")

    # =========================
    # STAGE 1
    # =========================
    st.markdown("---")
    st.header("🎯 Stage 1: Tool Ki Kahani")

    with st.container():
        st.markdown("""
        <div class="block">
        <h3>Lamba Karo Tool kya karta hai?</h3>
        <p>
        Ye kisi bhi 2D shape ko motai dekar 3D part banata hai.
        </p>

        <h4>Real Life Examples:</h4>
        <ul>
            <li>Mobile body</li>
            <li>Table leg</li>
            <li>Brick</li>
            <li>Box</li>
            <li>Ice Cream Stick</li>
        </ul>

        <p>
        Yaad rakho: Ye sirf seedha lamba karta hai.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.info("2D Rectangle → Lamba Karo → 3D Box")

    # =========================
    # STAGE 2
    # =========================
    st.markdown("---")
    st.header("🧠 Stage 2: Dimagh Ka Test")

    q1 = st.radio(
        "Bottle banane ke liye konsa tool better hoga?",
        [
            "Lamba Karo",
            "Ghumao Karo"
        ]
    )

    if st.button("Jawab Check Karo"):

        if q1 == "Ghumao Karo":
            st.success("✅ Bilkul sahi! Bottle gol hoti hai.")
            st.balloons()
        else:
            st.error("❌ Galat. Bottle gol shape hoti hai.")

    # =========================
    # STAGE 3
    # =========================
    st.markdown("---")
    st.header("✍️ Stage 3: Khud Bana Ke Dikhao")

    st.write("Rectangle banao aur usko 3D part me convert karo")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("2D Sketch")

        canvas_result = st_canvas(
            fill_color="rgba(0,255,0,0.3)",
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
        width = st.slider("Width", 10, 100, 20)
        height = st.slider("Motai (Extrude)", 1, 50, 10)

        if st.button("🚀 Lamba Karo"):

            result = cq.Workplane("XY").box(length, width, height)

            file_name = "solidshala_part.step"
            cq.exporters.export(result, file_name)

            st.success("✅ 3D Part Ban Gaya!")
            st.info("Tumne abhi apna pehla CAD part banaya 🔥")

            with open(file_name, "rb") as f:
                st.download_button(
                    "⬇️ STEP File Download Karo",
                    f,
                    file_name=file_name
                )

    # =========================
    # STAGE 4
    # =========================
    st.markdown("---")
    st.header("👁️ Stage 4: Engineer Ki Aankh")

    st.markdown("""
    ### Product Thinking

    Ice Cream Stick ka base kya tha?

    ✅ Rectangle

    Tumne pehle 2D sketch banaya.
    Phir usko motai di.

    Isi tarah duniya ke bohat products bante hain.
    """)

    st.success("Engineer ki tarah sochna start karo 🔥")

# =========================
# USTAAD AI
# =========================
elif page == "🤖 Ustaad AI":

    st.title("🤖 Ustaad AI")
    st.subheader("Tumhara CAD Dost")

    problem = st.selectbox(
        "Kahan phase ho?",
        [
            "Line connect nahi ho rahi",
            "Sketch red aa raha",
            "Dimension samajh nahi aa raha",
            "Kaunsa tool use karna hai"
        ]
    )

    if st.button("Ustaad Se Pucho"):

        if problem == "Line connect nahi ho rahi":
            st.info("2 lines ke endpoints connect karo.")

        elif problem == "Sketch red aa raha":
            st.info("Sketch open hai. Koi gap reh gaya hai.")

        elif problem == "Dimension samajh nahi aa raha":
            st.info("Smart Dimension tool use karo.")

        elif problem == "Kaunsa tool use karna hai":
            st.info("Seedha shape = Lamba Karo, Gol shape = Ghumao Karo")

# =========================
# PROGRESS
# =========================
elif page == "📈 Progress":

    st.title("📈 Student Progress")

    progress = 20

    st.progress(progress / 100)

    st.metric("Learning Progress", f"{progress}%")

    st.write("✅ Tool 1 Complete")
    st.write("⬜ Tool 2 Locked")
    st.write("⬜ Tool 3 Locked")

    st.success("Roz practice karo. Engineer ki aankh develop hogi 🔥")

```

---

# Deploy Karne Ka Tarika

## Step 1

GitHub pe new repository banao:

```txt
SolidShala
```

## Step 2

Ye dono files upload karo.

## Step 3

Open:

```txt
https://share.streamlit.io
```

## Step 4

GitHub repo select karo.

## Step 5

Deploy button dabao.

---

# Important

Agar cadquery error de:

requirements.txt me:

```txt
cadquery==2.4.0
```

ko replace karke:

```txt
cadquery
```

kar dena.
