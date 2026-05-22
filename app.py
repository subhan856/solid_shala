# =========================================================
# NEW ADVANCED render_model()
# REPLACE OLD render_model() WITH THIS
# =========================================================

def render_model():

    model = st.session_state.model

    fig = go.Figure()

    # =====================================================
    # CIRCLE / CYLINDER MODEL
    # =====================================================
    if model["shape"] == "circle":

        radius = max(
            0.2,
            model["radius"]
            - model["cut_depth"] * 0.1
        )

        radius *= model["scale"]

        height = model["height"]

        theta = np.linspace(0, 2*np.pi, 80)

        z = np.linspace(0, height, 40)

        theta, z = np.meshgrid(theta, z)

        x = radius * np.cos(theta)

        y = radius * np.sin(theta)

        # =============================================
        # MAIN CYLINDER
        # =============================================
        fig.add_trace(go.Surface(
            x=x,
            y=y,
            z=z,
            opacity=0.9
        ))

        # =============================================
        # SHELL EFFECT
        # =============================================
        if model["shell"] > 0:

            inner_radius = max(
                0.1,
                radius - model["shell"] * 0.2
            )

            x2 = inner_radius * np.cos(theta)

            y2 = inner_radius * np.sin(theta)

            fig.add_trace(go.Surface(
                x=x2,
                y=y2,
                z=z,
                opacity=0.3
            ))

        # =============================================
        # PATTERN EFFECT
        # =============================================
        for i in range(1, model["pattern"]):

            fig.add_trace(go.Surface(
                x=x + (i * 2.5),
                y=y,
                z=z,
                opacity=0.5
            ))

    # =====================================================
    # BOX MODEL
    # =====================================================
    elif model["shape"] == "square":

        scale = model["scale"]

        chamfer = model["chamfer"]

        height = model["height"]

        size = 1.0 * scale

        c = chamfer

        # =============================================
        # BOX VERTICES
        # =============================================
        vertices = np.array([

            [c,0,0],
            [size-c,0,0],
            [size,c,0],
            [size,size-c,0],
            [size-c,size,0],
            [c,size,0],
            [0,size-c,0],
            [0,c,0],

            [c,0,height],
            [size-c,0,height],
            [size,c,height],
            [size,size-c,height],
            [size-c,size,height],
            [c,size,height],
            [0,size-c,height],
            [0,c,height],

        ])

        x = vertices[:,0]
        y = vertices[:,1]
        z = vertices[:,2]

        # =============================================
        # MAIN BOX
        # =============================================
        fig.add_trace(go.Mesh3d(
            x=x,
            y=y,
            z=z,
            alphahull=0,
            opacity=0.75
        ))

        # =============================================
        # MIRROR EFFECT
        # =============================================
        if model["mirror"]:

            fig.add_trace(go.Mesh3d(
                x=-x,
                y=y,
                z=z,
                alphahull=0,
                opacity=0.4
            ))

        # =============================================
        # PATTERN EFFECT
        # =============================================
        for i in range(1, model["pattern"]):

            fig.add_trace(go.Mesh3d(
                x=x + (i * 2),
                y=y,
                z=z,
                alphahull=0,
                opacity=0.4
            ))

    # =====================================================
    # EMPTY MODEL
    # =====================================================
    else:

        fig.add_annotation(
            text="Draw Shape First",
            showarrow=False,
            font=dict(size=28)
        )

    # =====================================================
    # FINAL LAYOUT
    # =====================================================
    fig.update_layout(

        scene=dict(
            aspectmode="data"
        ),

        height=600,

        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        )
    )

    return fig
