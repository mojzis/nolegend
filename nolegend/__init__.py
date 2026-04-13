"""nolegend: Tufte-style templates and helpers for Plotly.

Usage:
    import nolegend
    nolegend.activate()  # set as default template

    # Or per-figure:
    fig = px.line(df, x="year", y="gdp", template="tufte")

    # Refine with helpers:
    nolegend.range_frame(fig)
    nolegend.direct_label(fig)

    # Sparklines:
    spark = nolegend.sparkline([1, 3, 2, 5, 4])

    # Color palettes:
    fig = px.bar(df, ..., template=nolegend.with_palette("earth"))
"""

from __future__ import annotations

# Color palettes
from .colors import (
    ALL as palettes,
)
from .colors import (
    DEFAULT,
    DUO,
    EARTH,
    INK,
    QUALITATIVE,
    SEQUENTIAL,
    SLATE,
    Palette,
)
from .colors import (
    get as get_palette,
)

# Helpers for the px → go refinement workflow
from .helpers import (
    annotate_point,
    direct_label,
    range_frame,
    sparkline,
    strip_chartjunk,
)

# Importing template registers "tufte" and "tufte_dark" with plotly.io
from .template import TUFTE, TUFTE_DARK, activate, with_palette

__version__ = "0.1.0"

__all__ = [
    # Colors
    "DEFAULT",
    "DUO",
    "EARTH",
    "INK",
    "QUALITATIVE",
    "SEQUENTIAL",
    "SLATE",
    # Templates
    "TUFTE",
    "TUFTE_DARK",
    "Palette",
    "activate",
    # Helpers
    "annotate_point",
    "direct_label",
    "get_palette",
    "palettes",
    "range_frame",
    "sparkline",
    "strip_chartjunk",
    "with_palette",
]
