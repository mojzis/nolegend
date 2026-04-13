"""Tufte-style Plotly templates.

Registers `tufte` and `tufte_dark` templates with plotly.io.
Based on Edward Tufte's principles from
"The Visual Display of Quantitative Information":

- Maximize data-ink ratio
- Remove non-data ink (chartjunk)
- Use range frames (axes span data, not plot)
- Direct-label instead of legends
- Serif typography
- Off-white or muted backgrounds
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

from . import colors

# --- Typography ---
# Georgia is the most widely available serif web font.
# Fall back to Times New Roman → generic serif.
FONT_FAMILY = "Georgia, 'Times New Roman', serif"
FONT_COLOR = "#333333"
FONT_COLOR_DARK = "#d4d4d4"


def _make_axis(dark: bool = False) -> dict:
    """Shared axis configuration for Tufte style."""
    color = FONT_COLOR_DARK if dark else FONT_COLOR
    line_color = "#555555" if dark else "#333333"
    return {
        "showgrid": False,
        "zeroline": False,
        "showline": True,
        "linewidth": 1,
        "linecolor": line_color,
        "ticks": "outside",
        "tickwidth": 1,
        "tickcolor": line_color,
        "ticklen": 4,
        "tickfont": {"size": 11},
        "title": {"font": {"size": 15}},
        "color": color,
        "automargin": True,
    }


def _make_template(dark: bool = False) -> go.layout.Template:
    """Build a Tufte template."""
    bg = "#1a1a1a" if dark else "#fffff8"
    font_color = FONT_COLOR_DARK if dark else FONT_COLOR
    palette = colors.DEFAULT

    # Slightly desaturate colors in dark mode
    colorway = palette.colorway

    return go.layout.Template(
        layout=go.Layout(
            # Background
            plot_bgcolor=bg,
            paper_bgcolor=bg,
            # Typography
            font={
                "family": FONT_FAMILY,
                "size": 12,
                "color": font_color,
            },
            title={
                "font": {"size": 18},
                "x": 0.0,
                "xanchor": "left",
                "y": 0.98,
                "yanchor": "top",
            },
            # No legend by default — direct-label instead
            showlegend=False,
            # Axes: minimal, data-driven
            xaxis=_make_axis(dark),
            yaxis=_make_axis(dark),
            # Colors
            colorway=colorway,
            # Margins: tight but readable
            margin={"l": 60, "r": 30, "t": 60, "b": 50, "pad": 4},
            # Hover: clean, no spikes
            hovermode="closest",
            hoverlabel={
                "bgcolor": "white" if not dark else "#2a2a2a",
                "font_size": 11,
                "font_family": FONT_FAMILY,
            },
            # Annotations default style
            annotationdefaults={
                "font": {"size": 11, "color": font_color},
                "showarrow": False,
            },
        ),
        # Trace defaults: reduce visual noise
        data={
            "scatter": [
                go.Scatter(
                    marker={"size": 6, "line": {"width": 0}},
                    line={"width": 2},
                )
            ],
            "bar": [
                go.Bar(
                    marker={
                        "line": {"width": 0},
                    },
                )
            ],
        },
    )


# Build and register templates on import — intentional side effect so that
# ``template="tufte"`` works immediately after ``import nolegend``.
TUFTE = _make_template(dark=False)
TUFTE_DARK = _make_template(dark=True)

pio.templates["tufte"] = TUFTE
pio.templates["tufte_dark"] = TUFTE_DARK


def activate(dark: bool = False) -> None:
    """Set `tufte` (or `tufte_dark`) as the default Plotly template."""
    pio.templates.default = "tufte_dark" if dark else "tufte"


def with_palette(palette_name: str, dark: bool = False) -> str:
    """Register and return a tufte variant using a specific palette.

    Usage:
        template_name = tufte.with_palette("earth")
        fig = px.line(df, ..., template=template_name)
    """
    name = f"tufte_{palette_name}" + ("_dark" if dark else "")

    if name in pio.templates:
        return name

    palette = colors.get(palette_name)
    base = _make_template(dark)
    base.layout.colorway = palette.colorway  # type: ignore[assignment]
    pio.templates[name] = base
    return name
