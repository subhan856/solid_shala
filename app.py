import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# =========================================================
# OPTIONAL DRAWING CANVAS
# =========================================================
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SolidShala Ultimate",
    layout="wide"
)

# =========================================================
# CUSTOM CSS (BETTER UI)
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

.tool-card {
    background: #1b1f2a;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.dimension-box {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
}

.history-box {
    background: #1f2937;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.title("🛠️ SolidShala Ultimate CAD Engine")
st.write("Sketch → Learn → Apply Tools → Build Product")

# =========================================================
# SAFE SESSION STATE
# =========================================================
if "model" not in st.session_state:

    st.session_state.model = {
        "shape": None,
        "radius": 1.0,
        "width": 1.0,
        "height": 1.0,
        "cut_depth": 0.0,
        "features": [],
    }

if "history" not in st.session_state:
    st.session_state.history = []

if "score" not in st.session_state:
    st.session_state.score = 0

# =========================================================
# LEARNING DATABASE
# =========================================================
LEARNING = {
    "Extrude": {
        "desc": "2D sketch ko 3D solid mein convert karta hai.",
        "usage": "Boxes, machine parts, plates",
        "questions": [
            "Extrude kya karta hai?",
            "Extrude ka use kaha hota hai?",
            "2D ko 3D banane wala tool konsa hai?"
        ]
    },

    "Cut": {
        "desc": "Material remove karta hai.",
        "usage": "Holes, slots, pockets",
        "questions": [
            "Cut ka purpose kya hai?",
            "Material remove kaunsa tool karta hai?",
            "Hole banane ke liye kya use hota hai?"
        ]
    },

    "Shell": {
        "desc": "Solid object ko hollow banata hai.",
        "usage": "Bottle, container, plastic body",
        "questions": [
            "Shell kya karta hai?",
            "Bottle hollow kaise hoti hai?",
            "Thickness remove ka tool konsa hai?"
        ]
    },

    "Fillet": {
        "desc": "Sharp edges ko smooth karta hai.",
        "usage": "Safe edges, design improvement",
        "questions": [
            "Fillet ka use kya hai?",
            "Edges smooth kaise hoti hain?",
            "Rounded corners kis tool se bante hain?"
        ]
    },

    "Chamfer": {
        "desc": "Edges ko angle pe cut karta hai.",
        "usage": "Mechanical parts, bolts",
        "questions": [
            "Chamfer kya karta hai?",
            "Bevel edge ka tool konsa hai?",
            "45 degree edge cut kis se hota hai?"
        ]
    }
}

# =========================================================
# ALL TOOLS
# =========================================================
TOOLS = [
    "Extrude",
    "Cut",
    "Shell",
    "Fillet",
    "Chamfer",
    "Scale",
    "Move",
    "Rotate",
    "Mirror",
    "Pattern",
    "Loft",
    "Sweep",
    "Offset",
    "Thicken",
    "Draft",
    "Union",
    "Subtract",
    "Intersect",
    "Revolve",
    "Reset"
]

# =========================================================
# MODEL CREATION
# =========================================================
def create_circle():

    model = st.session_state.model

    model["shape"] = "circle"
    model["radius"] = 1.0
    model["height"] = 1.0

    st.session_state.model = model


def create_square():

    model = st.session_state.model

    model["shape"] = "square"
    model["width"] = 1.0
    model["height"] = 1.0

    st.session_state.model = model


# =========================================================
# LIVE CAD RENDER
# =========================================================
def render_model():

    model = st.session_state.model

    # =========================
    # CIRCLE MODEL
    # =========================
    if model["shape"] == "circle":

        t = np.linspace(0, 2*np.pi, 100)
        z = np.linspace(0, model["height"], 2)

        t, z = np.meshgrid(t, z)

        x = model["radius"] * np.cos(t)
        y = model["radius"] * np.sin(t)

        fig = go.Figure(
            data=[
                go.Surface(
                    x=x,
                    y=y,
                    z=z
                )
            ]
        )

    # =========================
    # SQUARE MODEL
    # =========================
    elif model["shape"] == "square":

        x = [0,1,1,0,0,1,1,0]
        y = [0,0,1,1,0,0,1,1]

        z = [
            0,
            0,
            0,
            0,
            model["height"],
            model["height"],
            model["height"],
            model["height"]
        ]

        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=x,
                    y=y,
                    z=z,
                    opacity=0.5
                )
            ]
        )

    else:

        fig = go.Figure()

        fig.add_annotation(
            text="Create Sketch First",
            showarrow=False,
            font=dict(size=24)
        )

    fig.update_layout(
        height=500,
        margin=dict(l=0,r=0,t=30,b=0)
    )

    return fig

# =========================================================
# ANIMATION
# =========================================================
def animate(tool):

    box = st.empty()

    steps = [
        "Reading Sketch...",
        f"Applying {tool}...",
        "Calculating Geometry...",
        "Updating Dimensions...",
        "Rendering Final Product..."
    ]

    for s in steps:
        box.info(s)
        time.sleep(0.3)

    box.success("Tool Applied Successfully ✅")

# =========================================================
# TOOL ENGINE
# =========================================================
def apply_tool(tool):

    model = st.session_state.model

    if tool == "Extrude":
        model["height"] += 0.5

    elif tool == "Cut":
        model["cut_depth"] += 0.3
        model["height"] -= 0.2

    elif tool == "Shell":
        model["cut_depth"] += 0.5

    elif tool == "Scale":

        model["height"] *= 1.1

        if model["shape"] == "circle":
            model["radius"] *= 1.1

    elif tool == "Fillet":

        if model["shape"] == "circle":
            model["radius"] *= 1.05

    elif tool == "Chamfer":

        if model["shape"] == "square":
            model["width"] *= 0.95

    elif tool == "Reset":

        model["features"] = []
        model["height"] = 1
        model["radius"] = 1
        model["cut_depth"] = 0

    model["features"].append(tool)

    st.session_state.model = model

    st.session_state.history.append({
        "tool": tool,
        "time": str(datetime.now())
    })

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🎛️ CAD Controls")

mode = st.sidebar.radio(
    "Choose Mode",
    [
        "Modeling Mode",
        "Learning Mode",
        "History Mode"
    ]
)

selected_tool = st.sidebar.selectbox(
    "Select Tool",
    TOOLS
)

shape = st.sidebar.selectbox(
    "Select Sketch Shape",
    [
        "circle",
        "square"
    ]
)

# =========================================================
# CREATE SKETCH
# =========================================================
if st.sidebar.button("🎯 Create Sketch"):

    if shape == "circle":
        create_circle()

    else:
        create_square()

    st.success("Sketch Created Successfully")

# =========================================================
# MODELING MODE
# =========================================================
if mode == "Modeling Mode":

    col1, col2 = st.columns([1.2,1])

    # =====================================================
    # LEFT SIDE
    # =====================================================
    with col1:

        st.subheader("✏️ Sketch Canvas")

        if CANVAS_AVAILABLE:

            st_canvas(
                fill_color="rgba(0,0,255,0.1)",
                stroke_width=3,
                stroke_color="#FFFFFF",
                background_color="#111827",
                height=400,
                drawing_mode="freedraw",
                key="canvas"
            )

        else:
            st.warning(
                "Install canvas:\n\npip install streamlit-drawable-canvas"
            )

        st.subheader("🏗️ Final Product")

        st.plotly_chart(
            render_model(),
            use_container_width=True
        )

    # =====================================================
    # RIGHT SIDE
    # =====================================================
    with col2:

        st.subheader("📏 AI Dimensions")

        model = st.session_state.model

        st.markdown(f"""
<div class="dimension-box">

<h4>Shape: {model["shape"]}</h4>

<p>Radius: {round(model["radius"],2)}</p>

<p>Height: {round(model["height"],2)}</p>

<p>Cut Depth: {round(model["cut_depth"],2)}</p>

</div>
""", unsafe_allow_html=True)

        st.subheader("⚙️ Apply Tool")

        if st.button("🚀 Apply Selected Tool"):

            if model["shape"] is None:

                st.warning("Create sketch first")

            else:

                animate(selected_tool)

                apply_tool(selected_tool)

                st.session_state.score += 5

                st.rerun()

        st.subheader("🧠 Active Features")

        for feature in model["features"][-10:]:

            st.markdown(f"""
<div class="tool-card">
✅ {feature}
</div>
""", unsafe_allow_html=True)

        st.metric("⭐ Learning Score", st.session_state.score)

# =========================================================
# LEARNING MODE
# =========================================================
elif mode == "Learning Mode":

    st.header(f"📘 Learning: {selected_tool}")

    if selected_tool in LEARNING:

        data = LEARNING[selected_tool]

        st.info(data["desc"])

        st.success(f"💡 Usage: {data['usage']}")

        st.subheader("❓ Practice Questions")

        for i, q in enumerate(data["questions"],1):

            st.write(f"{i}. {q}")

    else:

        st.info("This tool modifies geometry in CAD modeling.")

# =========================================================
# HISTORY MODE
# =========================================================
else:

    st.header("📜 CAD Feature History")

    if st.session_state.history:

        for item in reversed(st.session_state.history):

            st.markdown(f"""
<div class="history-box">

🔧 {item["tool"]}

⏰ {item["time"]}

</div>
""", unsafe_allow_html=True)

    else:

        st.info("No CAD actions yet")

# =========================================================
# FOOTER
# =========================================================
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Features",
    len(st.session_state.model["features"])
)

c2.metric(
    "History",
    len(st.session_state.history)
)

c3.metric(
    "Score",
    st.session_state.score
)
