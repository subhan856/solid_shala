import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False

st.set_page_config(page_title="SolidShala V9", layout="wide")

st.title("🛠️ SolidShala V9 - CAD Learning Classroom + Engine")
st.write("Sketch → Learn → Animate → Build 3D Model")


# =========================
# 20 TOOLS + EDUCATION DATA
# =========================
TOOLS = {
    "Extrude": {
        "desc": "Extrude 2D shape ko 3D solid banata hai.",
        "example": "Box, brick",
        "quiz": [
            ("Extrude kya karta hai?", "2D to 3D"),
            ("Example?", "Box"),
            ("Extrude kis kaam aata hai?", "Solid banane"),
            ("Input kya hota hai?", "2D sketch"),
            ("Output kya hota hai?", "3D model"),
            ("Industry use?", "CAD modeling"),
            ("Shape type?", "Solid"),
            ("Direction kya hoti hai?", "Linear"),
            ("Tool type?", "Modeling"),
            ("Used in?", "Engineering")
        ]
    },

    "Revolve": {
        "desc": "Profile ko rotate karke 3D shape banata hai.",
        "example": "Bottle, glass",
        "quiz": [
            ("Revolve kya karta hai?", "Rotation"),
            ("Example?", "Bottle"),
            ("Axis kya hota hai?", "Center line"),
            ("Shape output?", "Cylindrical"),
            ("Input?", "2D profile"),
            ("Process?", "Rotation"),
            ("Use?", "Mechanical parts"),
            ("Industry?", "CAD"),
            ("Tool type?", "3D modeling"),
            ("Result?", "Solid")
        ]
    },

    "Cut": {
        "desc": "Material remove karta hai.",
        "example": "Hole, cavity",
        "quiz": [
            ("Cut kya karta hai?", "Remove material"),
            ("Example?", "Hole"),
            ("Use?", "Modify shape"),
            ("Process?", "Subtraction"),
            ("Input?", "Solid"),
            ("Output?", "Modified solid"),
            ("Tool type?", "Editing"),
            ("Industry?", "Manufacturing"),
            ("Operation?", "Boolean"),
            ("Result?", "Hollow or shape change"),
        ]
    },

    "Fillet": {
        "desc": "Edges ko smooth round karta hai.",
        "example": "Rounded corner",
        "quiz": [
            ("Fillet kya karta hai?", "Round edges"),
            ("Example?", "Corner smoothing"),
            ("Use?", "Safety + design"),
            ("Shape?", "Rounded"),
            ("Tool type?", "Modification"),
            ("Industry?", "Mechanical"),
            ("Benefit?", "Less stress"),
            ("Edge type?", "Soft"),
            ("Input?", "Sharp edge"),
            ("Output?", "Smooth edge"),
        ]
    }
}

# Fill remaining tools quickly (same pattern)
ALL_TOOLS = list(TOOLS.keys()) + [
    "Chamfer","Loft","Sweep","Shell","Pattern","Mirror",
    "Scale","Move","Rotate","Union","Subtract",
    "Intersect","Draft","Offset","Thicken","FilletEdge"
]

for t in ALL_TOOLS:
    if t not in TOOLS:
        TOOLS[t] = {
            "desc": f"{t} CAD operation used in modeling.",
            "example": "Engineering part",
            "quiz": [(f"{t} kya hai?", "CAD operation")] * 10
        }


# =========================
# 3D MODELS
# =========================
def box():
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


# =========================
# ANIMATION
# =========================
def animate(tool):
    steps = [
        "Sketch reading...",
        f"{tool} analyzing...",
        "Geometry processing...",
        "Model generating...",
        "Final output ready..."
    ]

    box = st.empty()
    for s in steps:
        box.info(s)
        time.sleep(0.3)
    box.success("Done ✅")


# =========================
# SIDEBAR
# =========================
mode = st.sidebar.radio("Mode", ["Learn Mode", "Practice Mode"])
tool = st.sidebar.selectbox("Tool", ALL_TOOLS)


# =========================
# LEARN MODE (NEW CLASSROOM)
# =========================
if mode == "Learn Mode":

    st.header(f"📘 Learning Classroom: {tool}")

    data = TOOLS[tool]

    st.subheader("🧠 Concept")
    st.write(data["desc"])

    st.subheader("📌 Example")
    st.info(data["example"])

    st.subheader("📚 10 Questions (Practice)")

    for i, (q, a) in enumerate(data["quiz"], 1):
        st.write(f"Q{i}: {q}")
        st.write(f"👉 Answer: {a}")


# =========================
# PRACTICE MODE
# =========================
else:

    st.header("🛠️ Practice Lab")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✏️ Sketch Canvas")

        if CANVAS_AVAILABLE:
            st_canvas(
                fill_color="rgba(0, 0, 255, 0.2)",
                stroke_width=3,
                stroke_color="#000",
                background_color="#fff",
                height=400,
                drawing_mode="freedraw",
                key="canvas"
            )
        else:
            st.warning("Install streamlit-drawable-canvas")

    with col2:

        st.subheader("⚙️ Build Engine")

        if st.button("🚀 Run Tool"):

            animate(tool)

            if tool == "Extrude":
                st.plotly_chart(box())
            elif tool == "Revolve":
                st.plotly_chart(cylinder())
            else:
                st.success(f"{tool} executed successfully")

    st.divider()

    st.subheader("📜 History")
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("💾 Save Tool"):
        st.session_state.history.append(tool)

    st.write(st.session_state.history)
