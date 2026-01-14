import numpy as np
import sympy as sp
import plotly.graph_objects as go

def plot_3d(exprs,var,labels=None,colormap=None,title="3D Plot",xlabel="x",ylabel="y",show_colorbar=True,
            zlabel="Value",xlim=None,ylim=None,zlim=None,resolution=100,show=True,width=800,height=700):
    
    """
    Plots 3D surfaces from symbolic expressions using Plotly.

    Parameters:
        exprs      : SymPy expression or list of expressions
        var        : (x_sym, x_range, y_sym, y_range)
        labels     : List of labels for surfaces
        colormap   : None, string, or list of strings 
                     Can be Plotly colormap names (e.g., 'Viridis') or 
                     single colors (e.g., 'red', 'blue', '#FF5733', 'rgb(100,150,200)')
        resolution : Grid resolution per axis
        show       : Whether to display the plot

    Returns:
        plotly.graph_objects.Figure
    """

    DEFAULT_COLORMAP = "Viridis"
    
    # Common single color names that should be treated as solid colors
    SINGLE_COLOR_NAMES = {
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 
        'cyan', 'magenta', 'brown', 'gray', 'grey', 'black', 'white',
        'navy', 'teal', 'lime', 'olive', 'maroon', 'aqua', 'fuchsia',
        'silver', 'gold', 'indigo', 'violet', 'crimson', 'coral'
    }

    def is_single_color(color_str):
        """Check if the string represents a single color rather than a colorscale."""
        if color_str is None:
            return False
        color_lower = color_str.lower()
        # Check if it's a named color, hex color, or rgb/rgba color
        return (color_lower in SINGLE_COLOR_NAMES or 
                color_str.startswith('#') or 
                color_str.startswith('rgb'))

    def create_colorscale_from_color(color):
        """Create a uniform colorscale (no gradient) for a single color."""
        # Use the same color at all points - true single color
        return [
            [0.0, color],
            [1.0, color]
        ]

    if not isinstance(exprs, list):
        exprs = [exprs]

    if not isinstance(var, tuple) or len(var) != 4:
        raise ValueError("`var` must be (x_sym, x_range, y_sym, y_range)")

    x_sym, x_range, y_sym, y_range = var

    if colormap is None:
        colormaps = None
    elif isinstance(colormap, (list, tuple)):
        colormaps = list(colormap)
    else:
        colormaps = [colormap]

    x_vals = np.linspace(float(x_range[0]), float(x_range[1]), resolution)
    y_vals = np.linspace(float(y_range[0]), float(y_range[1]), resolution)
    X, Y = np.meshgrid(x_vals, y_vals)

    fig = go.Figure()

    for i, expr in enumerate(exprs):
        expr = sp.sympify(expr)

        label = (
            labels[i]
            if labels and i < len(labels)
            else f"Expr {i + 1}"
        )

        # Determine colormap/color for this surface
        if colormaps and i < len(colormaps):
            cmap = colormaps[i]
        else:
            cmap = DEFAULT_COLORMAP
        
        # Check if it's a single color and convert to colorscale if needed
        if is_single_color(cmap):
            colorscale = create_colorscale_from_color(cmap)
        else:
            colorscale = cmap

        f = sp.lambdify((x_sym, y_sym), expr, modules="numpy")
        Z = f(X, Y)

        if np.isscalar(Z):
            Z = np.full_like(X, Z, dtype=float)


        fig.add_trace(
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                name=label,
                colorscale=colorscale,
                showscale=show_colorbar,
                opacity=0.7,
            )
        )

    fig.update_layout(
        title=title,
        autosize=False,
        width=width,
        height=height,
        scene=dict(
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            zaxis_title=zlabel,
            xaxis=dict(range=list(xlim) if xlim else None),
            yaxis=dict(range=list(ylim) if ylim else None),
            zaxis=dict(range=list(zlim) if zlim else None),
            aspectratio=dict(x=1, y=1, z=1),
            camera=dict(eye=dict(x=1.87, y=0.88, z=1.5)),
        ),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(x=0, y=1),
    )

    if show:
        fig.show()

    return fig