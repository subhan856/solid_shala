import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# =========================================================
# OPTIONAL CANVAS
# =========================================================
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except:
    CANVAS_AVAILABLE = False

# =========================================================
# OPTIONAL AI DETECTION
# =========================================================
try:
    import cv2
    CV2_AVAILABLE = True
except:
    CV2_AVAILABLE = False

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SolidShala Ultimate AI CAD",
    layout="wide"
)

# =========================================================
# CUSTOM UI
# =========================================================
st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    background-color: #2563eb;
    color: white;
    border: none;
}

.block {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.metric-box {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
}

.tool-box {
    background: #1f2937;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.title("🛠️ SolidShala Ultimate AI CAD")
st.write("Sketch → AI Detection → CAD Modeling → Learning Engine")

# =========================================================
# SAFE SESSION STATE
# =========================================================
if "model" not in st.session_state or st.session_state.model is None:

    st.session_state.model = {

        "shape": None,

        "radius": 1.0,

        "width": 1.0,

        "height": 1.0,

        "cut_depth": 0.0,

        "chamfer": 0.0,

        "fillet": 0.0,

        "shell": 0.0,

        "mirror": False,

        "pattern": 1,

        "draft": 0,

        "thickness": 1.0,

        "scale": 1.0,

        "features": []
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
        "usage": "Machine parts, boxes, plates",
        "questions": [
            "Extrude kya karta hai?",
            "2D ko 3D kis tool se banate hain?",
            "Extrude ka use kaha hota hai?"
        ]
    },

    "Cut": {
        "desc": "Material remove karta hai.",
        "usage": "Holes, slots",
        "questions": [
            "Cut tool ka purpose kya hai?",
            "Hole kis tool se banta hai?",
            "Material remove tool?"
        ]
    },

    "Shell": {
        "desc": "Object ko hollow banata hai.",
        "usage": "Bottle, plastic bodies",
        "questions": [
            "Shell kya karta hai?",
            "Object hollow kaise hota hai?",
            "Thickness remove tool?"
        ]
    },

    "Fillet": {
        "desc": "Sharp edges smooth karta hai.",
        "usage": "Rounded safe edges",
        "questions": [
            "Fillet kya karta hai?",
            "Rounded edge tool?",
            "Smooth corner tool?"
        ]
    },

    "Chamfer": {
        "desc": "Edge ko angle pe cut karta hai.",
        "usage": "Mechanical edges",
        "questions": [
            "Chamfer kya karta hai?",
            "45 degree edge tool?",
            "Bevel edge ka tool?"
        ]
    }
}

# =========================================================
# TOOL LIST
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

    "Boss",

    "Rib",

    "HoleWizard",

    "Split",

    "Combine",

    "Reset"
]

# =========================================================
# AI SHAPE DETECTION
# =========================================================
def detect_shape(image_data):

    if image_data is None:
        return None

    if not CV2_AVAILABLE:
        return None

    img = image_data.astype("uint8")

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    _, thresh = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 500:
            continue

        approx = cv2.approxPolyDP(
            cnt,
            0.04 * cv2.arcLength(cnt, True),
            True
        )

        sides = len(approx)

        if sides == 4:
            return "square"

        elif sides > 6:
            return "circle"

    return None

# =========================================================
# CREATE SHAPES
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
# BUILD ANIMATION
# =========================================================
def auto_build_animation():

    bar = st.progress(0)

    for i in range(100):

        time.sleep(0.01)

        bar.progress(i + 1)

    st.success("CAD Product Generated ✅")

# =========================================================
# TOOL ANIMATION
# =========================================================
def animate(tool):

    box = st.empty()

    steps = [

        "Reading AI Sketch...",

        f"Applying {tool}...",

        "Calculating Geometry...",

        "Updating Dimensions...",

        "Building CAD Product..."
    ]

    for s in steps:

        box.info(s)

        time.sleep(0.3)

    box.success("Tool Applied Successfully")

# =========================================================
# TOOL ENGINE
# =========================================================
def apply_tool(tool):

    model = st.session_state.model

    # =============================================
    # BASIC TOOLS
    # =============================================
    if tool == "Extrude":

        model["height"] += 0.5

    elif tool == "Cut":

        model["cut_depth"] += 0.2

        model["height"] -= 0.1

    elif tool == "Shell":

        model["shell"] += 0.15

    elif tool == "Fillet":

        model["fillet"] += 0.08

    elif tool == "Chamfer":

        model["chamfer"] += 0.08

    elif tool == "Scale":

        model["scale"] += 0.1

    elif tool == "Mirror":

        model["mirror"] = True

    elif tool == "Pattern":

        model["pattern"] += 1

    elif tool == "Draft":

        model["draft"] += 2

    elif tool == "Thicken":

        model["thickness"] += 0.1

    elif tool == "Reset":

        model["height"] = 1.0

        model["radius"] = 1.0

        model["cut_depth"] = 0.0

        model["chamfer"] = 0.0

        model["fillet"] = 0.0

        model["shell"] = 0.0

        model["pattern"] = 1

        model["features"] = []

    # =============================================
    # EXTRA FEATURES
    # =============================================
    elif tool == "Boss":

        model["height"] += 1

    elif tool == "Rib":

        model["thickness"] += 0.2

    elif tool == "HoleWizard":

        model["cut_depth"] += 0.5

    elif tool == "Combine":

        model["pattern"] += 2

    elif tool == "Split":

        model["height"] *= 0.8

    model["features"].append(tool)

    st.session_state.model = model

    st.session_state.history.append({

        "tool": tool,

        "time": str(datetime.now())
    })

# =========================================================
# CAD MODEL RENDER
# =========================================================
def render_model():

    model = st.session_state.model

    # =============================================
    # CIRCLE MODEL
    # =============================================
    if model["shape"] == "circle":

        scale = model["scale"]

        radius = (
            model["radius"]
            - model["cut_depth"] * 0.1
        )

        radius *= scale

        t = np.linspace(0, 2*np.pi, 100)

        z = np.linspace(
            0,
            model["height"],
            2
        )

        t, z = np.meshgrid(t, z)

        x = radius * np.cos(t)

        y = radius * np.sin(t)

        fig = go.Figure()

        fig.add_trace(go.Surface(
            x=x,
            y=y,
            z=z
        ))

        # =========================================
        # SHELL EFFECT
        # =========================================
        if model["shell"] > 0:

            inner_radius = radius - model["shell"] * 0.2

            x2 = inner_radius * np.cos(t)

            y2 = inner_radius * np.sin(t)

            fig.add_trace(go.Surface(
                x=x2,
                y=y2,
                z=z,
                opacity=0.4
            ))

        # =========================================
        # PATTERN EFFECT
        # =========================================
        if model["pattern"] > 1:

            for i in range(1, model["pattern"]):

                fig.add_trace(go.Surface(
                    x=x + (i * 2),
                    y=y,
                    z=z,
                    opacity=0.3
                ))

    # =============================================
    # SQUARE MODEL
    # =============================================
    elif model["shape"] == "square":

        h = model["height"]

        c = model["chamfer"]

        scale = model["scale"]

        x = np.array([
            c,1-c,1,1,1-c,c,0,0,
            c,1-c,1,1,1-c,c,0,0
        ]) * scale

        y = np.array([
            0,0,c,1-c,1,1,1-c,c,
            0,0,c,1-c,1,1,1-c,c
        ]) * scale

        z = np.array([
            0,0,0,0,0,0,0,0,
            h,h,h,h,h,h,h,h
        ])

        fig = go.Figure()

        fig.add_trace(go.Mesh3d(
            x=x,
            y=y,
            z=z,
            opacity=0.6
        ))

        # =========================================
        # MIRROR EFFECT
        # =========================================
        if model["mirror"]:

            fig.add_trace(go.Mesh3d(
                x=-x,
                y=y,
                z=z,
                opacity=0.4
            ))

        # =========================================
        # PATTERN EFFECT
        # =========================================
        if model["pattern"] > 1:

            for i in range(1, model["pattern"]):

                fig.add_trace(go.Mesh3d(
                    x=x + (i * 1.5),
                    y=y,
                    z=z,
                    opacity=0.3
                ))

    else:

        fig = go.Figure()

        fig.add_annotation(
            text="Draw Shape on Canvas",
            showarrow=False,
            font=dict(size=24)
        )

    fig.update_layout(

        height=550,

        margin=dict(l=0,r=0,t=30,b=0)
    )

    return fig

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

# =========================================================
# MODELING MODE
# =========================================================
if mode == "Modeling Mode":

    left, right = st.columns([1.3,1])

    # =============================================
    # LEFT SIDE
    # =============================================
    with left:

        st.subheader("✏️ AI Sketch Canvas")

        if CANVAS_AVAILABLE:

            canvas_result = st_canvas(

                fill_color="rgba(0,0,255,0.1)",

                stroke_width=5,

                stroke_color="#FFFFFF",

                background_color="#111827",

                height=400,

                drawing_mode="freedraw",

                key="canvas"
            )

            # =====================================
            # AI DETECTION
            # =====================================
            if st.button("🤖 AI Detect Shape"):

                detected = detect_shape(
                    canvas_result.image_data
                )

                if detected == "circle":

                    create_circle()

                    st.success("AI detected: Circle")

                elif detected == "square":

                    create_square()

                    st.success("AI detected: Square")

                else:

                    st.warning(
                        "Shape not detected. Draw bigger shape."
                    )

        else:

            st.error(
                "Install streamlit-drawable-canvas"
            )

        st.subheader("🏗️ Final CAD Product")

        st.plotly_chart(
            render_model(),
            use_container_width=True
        )

    # =============================================
    # RIGHT SIDE
    # =============================================
    with right:

        model = st.session_state.model

        st.subheader("📏 AI Dimensions")

        st.markdown(f"""
<div class="metric-box">

<h4>Shape: {model["shape"]}</h4>

<p>Radius: {round(model["radius"],2)}</p>

<p>Height: {round(model["height"],2)}</p>

<p>Cut Depth: {round(model["cut_depth"],2)}</p>

<p>Chamfer: {round(model["chamfer"],2)}</p>

<p>Shell: {round(model["shell"],2)}</p>

<p>Scale: {round(model["scale"],2)}</p>

</div>
""", unsafe_allow_html=True)

        # =========================================
        # AI ANALYSIS
        # =========================================
        st.subheader("🤖 AI CAD Analysis")

        if model["shape"] == "circle":

            volume = round(

                np.pi *
                model["radius"]**2 *
                model["height"],

                2
            )

            st.success(
                f"Estimated Volume: {volume}"
            )

        elif model["shape"] == "square":

            volume = round(

                model["height"] *
                model["scale"],

                2
            )

            st.success(
                f"Estimated Volume: {volume}"
            )

        # =========================================
        # AI SUGGESTIONS
        # =========================================
        if model["cut_depth"] > 0.5:

            st.info(
                "AI Suggestion: Apply Fillet"
            )

        if model["height"] > 2:

            st.info(
                "AI Suggestion: Apply Shell"
            )

        if model["pattern"] > 2:

            st.info(
                "AI Suggestion: Use Mirror"
            )

        # =========================================
        # APPLY TOOL
        # =========================================
        st.subheader("⚙️ Apply CAD Tool")

        if st.button("🚀 Apply Tool"):

            if model["shape"] is None:

                st.warning(
                    "Draw shape first"
                )

            else:

                animate(selected_tool)

                auto_build_animation()

                apply_tool(selected_tool)

                st.session_state.score += 5

                st.rerun()

        # =========================================
        # FEATURES
        # =========================================
        st.subheader("🧠 Feature Stack")

        for feature in model["features"][-10:]:

            st.markdown(f"""
<div class="tool-box">
✅ {feature}
</div>
""", unsafe_allow_html=True)

        st.metric(
            "⭐ Learning Score",
            st.session_state.score
        )

# =========================================================
# LEARNING MODE
# =========================================================
elif mode == "Learning Mode":

    st.header(f"📘 Learning: {selected_tool}")

    if selected_tool in LEARNING:

        data = LEARNING[selected_tool]

        st.info(data["desc"])

        st.success(
            f"💡 Usage: {data['usage']}"
        )

        st.subheader("❓ Practice Questions")

        for i, q in enumerate(data["questions"],1):

            st.write(f"{i}. {q}")

    else:

        st.info(
            "This tool modifies geometry."
        )

# =========================================================
# HISTORY MODE
# =========================================================
else:

    st.header("📜 CAD History")

    if st.session_state.history:

        for item in reversed(st.session_state.history):

            st.markdown(f"""
<div class="block">

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
