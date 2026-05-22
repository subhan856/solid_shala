# =========================================================
# SAFE & WORKING render_model()
# REPLACE YOUR OLD render_model() WITH THIS
# =========================================================

def render_model():

    model = st.session_state.model

    fig = go.Figure()

    # =====================================================
    # CIRCLE MODEL
    # =====================================================
    if model["shape"] == "circle":

        radius = max(
            0.2,
            model.get("radius", 1.0)
            - model.get("cut_depth", 0.0) * 0.1
        )

        scale = model.get("scale", 1.0)

        radius = radius * scale

        height = model.get("height", 1.0)

        theta = np.linspace(0, 2*np.pi, 60)

        z = np.linspace(0, height, 30)

        theta, z = np.meshgrid(theta, z)

        x = radius * np.cos(theta)

        y = radius * np.sin(theta)

        # MAIN CYLINDER
        fig.add_trace(go.Surface(
            x=x,
            y=y,
            z=z,
            opacity=0.9
        ))

        # =================================================
        # SHELL EFFECT
        # =================================================
        shell = model.get("shell", 0.0)

        if shell > 0:

            inner_radius = max(
                0.1,
                radius - shell * 0.2
            )

            x2 = inner_radius * np.cos(theta)

            y2 = inner_radius * np.sin(theta)

            fig.add_trace(go.Surface(
                x=x2,
                y=y2,
                z=z,
                opacity=0.3
            ))

        # =================================================
        # PATTERN EFFECT
        # =================================================
        pattern = model.get("pattern", 1)

        for i in range(1, pattern):

            fig.add_trace(go.Surface(
                x=x + (i * 2.5),
                y=y,
                z=z,
                opacity=0.4
            ))

    # =====================================================
    # SQUARE MODEL
    # =====================================================
    elif model["shape"] == "square":

        scale = model.get("scale", 1.0)

        chamfer = model.get("chamfer", 0.0)

        height = model.get("height", 1.0)

        size = 1.0 * scale

        c = min(chamfer, 0.3)

        # SAFE BOX POINTS
        x = [
            c, size-c, size, size,
            size-c, c, 0, 0
        ]

        y = [
            0,0,c,size-c,
            size,size,size-c,c
        ]

        z_bottom = [0]*8

        z_top = [height]*8

        # BOTTOM
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z_bottom,
            mode='lines'
        ))

        # TOP
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z_top,
            mode='lines'
        ))

        # VERTICAL EDGES
        for i in range(8):

            fig.add_trace(go.Scatter3d(
                x=[x[i], x[i]],
                y=[y[i], y[i]],
                z=[0, height],
                mode='lines'
            ))

        # =================================================
        # MIRROR EFFECT
        # =================================================
        mirror = model.get("mirror", False)

        if mirror:

            x2 = [-v for v in x]

            fig.add_trace(go.Scatter3d(
                x=x2,
                y=y,
                z=z_bottom,
                mode='lines'
            ))

            fig.add_trace(go.Scatter3d(
                x=x2,
                y=y,
                z=z_top,
                mode='lines'
            ))

        # =================================================
        # PATTERN EFFECT
        # =================================================
        pattern = model.get("pattern", 1)

        if pattern > 1:

            for p in range(1, pattern):

                shift = p * 2

                x_shift = [v + shift for v in x]

                fig.add_trace(go.Scatter3d(
                    x=x_shift,
                    y=y,
                    z=z_bottom,
                    mode='lines'
                ))

                fig.add_trace(go.Scatter3d(
                    x=x_shift,
                    y=y,
                    z=z_top,
                    mode='lines'
                ))

    # =====================================================
    # EMPTY SCREEN
    # =====================================================
    else:

        fig.add_annotation(
            text="Draw Shape First",
            showarrow=False,
            font=dict(size=26)
        )

    # =====================================================
    # FINAL SETTINGS
    # =====================================================
    fig.update_layout(

        height=600,

        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        ),

        scene=dict(
            aspectmode='data'
        )
    )

    return fig
