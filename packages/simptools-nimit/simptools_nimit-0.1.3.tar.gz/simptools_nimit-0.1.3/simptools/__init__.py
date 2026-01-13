# Master package init
from . import math
from . import image
from . import graph
from . import data 

# Expose commonly used functions at top-level
from .math.basic import (
    add,
    subtract,
    multiply,
    divide,
    clamp,
    power
)
from .image.core import (
    load_image,
    show_image,
    save_image,
    resize_image,
    crop_image,
    flip_image,
    rotate_image,
    convert_color
)
from .graph.graphs import (
    save_graph,
    show_graph,
    line_graph,
    bar_graph,
    scatter_plot,
    histogram
)
from .data.data import (   # <- add all data functions
    average,
    middle,
    spread,
    deviation,
    normalize,
    zscore,
    flatten,
    split,
    unique,
    pairs,
    running,
    check,
    same,
    scale,
    shift,
    clip
)

__all__ = [
    "math",
    "image",
    "graph",
    "data",  # <- expose the data module

    # Math functions
    "add",
    "subtract",
    "multiply",
    "divide",
    "clamp",
    "power",

    # Image functions
    "load_image",
    "show_image",
    "save_image",
    "resize_image",
    "crop_image",
    "flip_image",
    "rotate_image",
    "convert_color",

    # Graph functions
    "save_graph",
    "show_graph",
    "line_graph",
    "bar_graph",
    "scatter_plot",
    "histogram",

    # Data functions
    "average",
    "middle",
    "spread",
    "deviation",
    "normalize",
    "zscore",
    "flatten",
    "split",
    "unique",
    "pairs",
    "running",
    "check",
    "same",
    "scale",
    "shift",
    "clip"
]
