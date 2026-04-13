"""Tufte chart helpers for Plotly.

Post-processing functions that apply Tufte patterns to existing figures.
Designed for the px → go refinement workflow:

    fig = px.line(df, x="year", y="value")
    tufte.range_frame(fig)
    tufte.direct_label(fig)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go

if TYPE_CHECKING:
    from collections.abc import Sequence


def range_frame(fig: go.Figure, pad: float = 0.02) -> go.Figure:
    """Trim axes to span only the data range (Tufte's range frame).

    Instead of axes extending to round numbers, they start and end
    at the actual data min/max. This removes non-data ink.

    Args:
        fig: A Plotly figure to modify in place.
        pad: Fractional padding beyond data range (0.02 = 2%).

    Returns:
        The modified figure (for chaining).
    """
    x_vals: list[float] = []
    y_vals: list[float] = []

    for trace in fig.data:
        if hasattr(trace, "x") and trace.x is not None:
            x_vals.extend(v for v in trace.x if v is not None)
        if hasattr(trace, "y") and trace.y is not None:
            y_vals.extend(v for v in trace.y if v is not None)

    if x_vals:
        x_min, x_max = min(x_vals), max(x_vals)
        x_pad = (x_max - x_min) * pad if x_max != x_min else 1
        fig.update_xaxes(range=[x_min - x_pad, x_max + x_pad])

    if y_vals:
        y_min, y_max = min(y_vals), max(y_vals)
        y_pad = (y_max - y_min) * pad if y_max != y_min else 1
        fig.update_yaxes(range=[y_min - y_pad, y_max + y_pad])

    return fig


def direct_label(
    fig: go.Figure,
    position: str = "right",
    font_size: int = 11,
) -> go.Figure:
    """Add direct labels to line traces, replacing the legend.

    Places the trace name at the end (or start) of each line,
    eliminating the need for a separate legend box.

    Args:
        fig: A Plotly figure to modify in place.
        position: "right" (label at last point) or "left" (at first point).
        font_size: Label font size.

    Returns:
        The modified figure (for chaining).
    """
    fig.update_layout(showlegend=False)

    for trace in fig.data:
        if not hasattr(trace, "x") or trace.x is None:
            continue
        if not hasattr(trace, "y") or trace.y is None:
            continue
        if not trace.name:
            continue

        xs = list(trace.x)
        ys = list(trace.y)
        if not xs or not ys:
            continue

        idx = -1 if position == "right" else 0
        xanchor = "left" if position == "right" else "right"
        x_offset = 8 if position == "right" else -8

        color = None
        if hasattr(trace, "line") and trace.line and trace.line.color:
            color = trace.line.color
        elif hasattr(trace, "marker") and trace.marker and trace.marker.color:
            color = trace.marker.color

        fig.add_annotation(
            x=xs[idx],
            y=ys[idx],
            text=trace.name,
            xanchor=xanchor,
            yanchor="middle",
            xshift=x_offset,
            showarrow=False,
            font={
                "size": font_size,
                "color": color or "#333333",
            },
        )

    return fig


def sparkline(
    values: Sequence[float],
    width: int = 200,
    height: int = 40,
    color: str = "#333333",
    show_endpoints: bool = True,
    template: str = "tufte",
) -> go.Figure:
    """Create a Tufte sparkline — a word-sized graphic.

    A minimal inline chart showing trend without axes, labels, or chrome.

    Args:
        values: The data series.
        width: Figure width in pixels.
        height: Figure height in pixels.
        color: Line color.
        show_endpoints: Dot on first and last value.
        template: Plotly template name.

    Returns:
        A minimal Plotly figure.
    """
    vals = list(values)
    xs = list(range(len(vals)))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=vals,
            mode="lines",
            line={"color": color, "width": 1.5},
            hoverinfo="y",
        )
    )

    if show_endpoints and len(vals) >= 2:
        fig.add_trace(
            go.Scatter(
                x=[xs[0], xs[-1]],
                y=[vals[0], vals[-1]],
                mode="markers",
                marker={"color": color, "size": 4},
                hoverinfo="y",
            )
        )

    fig.update_layout(
        template=template,
        width=width,
        height=height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0, "pad": 0},
        xaxis={"visible": False},
        yaxis={"visible": False},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return fig


def annotate_point(
    fig: go.Figure,
    x: float,
    y: float,
    text: str,
    ay: int = -30,
) -> go.Figure:
    """Annotate a specific data point with an arrow.

    Use to call out events, anomalies, or key moments in the data.

    Args:
        fig: A Plotly figure to modify in place.
        x: X coordinate of the point.
        y: Y coordinate of the point.
        text: Annotation text.
        ay: Arrow y-offset in pixels (negative = above).

    Returns:
        The modified figure (for chaining).
    """
    fig.add_annotation(
        x=x,
        y=y,
        text=text,
        showarrow=True,
        arrowhead=0,
        arrowwidth=1,
        arrowcolor="#636363",
        ax=0,
        ay=ay,
        font={"size": 10, "color": "#333333"},
    )
    return fig


def strip_chartjunk(fig: go.Figure) -> go.Figure:
    """Remove common chartjunk from any Plotly figure.

    Applies even without the tufte template — useful for cleaning up
    figures generated by px before further refinement.

    Args:
        fig: A Plotly figure to modify in place.

    Returns:
        The modified figure (for chaining).
    """
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor="#333333",
        ticks="outside",
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor="#333333",
        ticks="outside",
    )
    return fig
