import streamlit as st
import numpy as np
import trimesh
import plotly.graph_objects as go

# =====================================================
# PAGE
# =====================================================
st.set_page_config(page_title="SolidShala REAL CAD", layout="wide")

st.title("🛠️ SolidShala REAL CAD Engine (Mini SolidWorks)")
st.write("True geometry-based modeling (not fake UI)")

# =====================================================
# STATE
# =====================================================
if "mesh" not in st.session_state:
    st.session_state.mesh = None

if "shape" not in st.session_state:
    st.session_state.shape = None

# =====================================================
# CREATE BASE SHAPES
# =====================================================
def create_box():
    mesh = trimesh.creation.box(extents=(1,1,1))
    st.session_state.mesh = mesh
    st.session_state.shape = "box"

def create_cylinder():
    mesh = trimesh.creation.cylinder(radius=0.5, height=1.0)
    st.session_state.mesh = mesh
    st.session_state.shape = "cylinder"

# =====================================================
# TOOLS (REAL GEOMETRY)
# =====================================================
def apply_tool(tool):

    mesh = st.session_state.mesh

    if mesh is None:
        return

    # -----------------------
    # EXTRUDE
    # -----------------------
    if tool == "Extrude":
        mesh.apply_scale((1,1,1.2))

    # -----------------------
    # CUT (slice top)
    # -----------------------
    elif tool == "Cut":
        plane_origin = [0,0,0.5]
        plane_normal = [0,0,1]

        mesh = mesh.slice_plane(plane_origin, plane_normal)
        st.session_state.mesh = mesh

    # -----------------------
    # SCALE
    # -----------------------
    elif tool == "Scale":
        mesh.apply_scale(1.2)

    # -----------------------
    # FLIP / MIRROR
    # -----------------------
    elif tool == "Mirror":
        mesh.apply_scale([-1,1,1])

    st.session_state.mesh = mesh

# =====================================================
# RENDER MESH
# =====================================================
def show_mesh(mesh):

    if mesh is None:
        return go.Figure()

    vertices = mesh.vertices
    faces = mesh.faces

    x, y, z = vertices[:,0], vertices[:,1], vertices[:,2]

    i, j, k = faces[:,0], faces[:,1], faces[:,2]

    fig = go.Figure(data=[
        go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            opacity=0.8
        )
    ])

    fig.update_layout(
        height=600,
        margin=dict(l=0,r=0,t=20,b=0),
        scene=dict(aspectmode="data")
    )

    return fig

# =====================================================
# UI
# =====================================================
col1, col2 = st.columns(2)

with col1:

    st.subheader("🧱 Create Shape")

    if st.button("Box"):
        create_box()

    if st.button("Cylinder"):
        create_cylinder()

    st.subheader("📦 Model View")

    st.plotly_chart(show_mesh(st.session_state.mesh), use_container_width=True)

with col2:

    st.subheader("⚙️ Tools")

    tool = st.selectbox(
        "Select Tool",
        ["Extrude", "Cut", "Scale", "Mirror"]
    )

    if st.button("Apply Tool"):

        apply_tool(tool)
        st.success(f"{tool} applied")

        st.rerun()

    st.subheader("🧠 Status")

    st.write("Shape:", st.session_state.shape)
