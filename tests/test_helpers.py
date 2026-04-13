from __future__ import annotations

import plotly.graph_objects as go

from nolegend.helpers import (
    annotate_point,
    direct_label,
    range_frame,
    sparkline,
    strip_chartjunk,
)


def _line_fig(xs=None, ys=None, name="A"):
    """Helper: simple line figure."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs or [1, 2, 3],
            y=ys or [10, 20, 30],
            mode="lines",
            name=name,
            line={"color": "#ff0000"},
        )
    )
    return fig


class TestRangeFrame:
    def test_sets_axis_range(self):
        fig = _line_fig(xs=[1, 2, 3], ys=[10, 20, 30])
        result = range_frame(fig, pad=0.0)
        assert result is fig
        assert fig.layout.xaxis.range[0] == 1
        assert fig.layout.xaxis.range[1] == 3
        assert fig.layout.yaxis.range[0] == 10
        assert fig.layout.yaxis.range[1] == 30

    def test_padding(self):
        fig = _line_fig(xs=[0, 10], ys=[0, 100])
        range_frame(fig, pad=0.1)
        assert fig.layout.xaxis.range[0] < 0
        assert fig.layout.xaxis.range[1] > 10
        assert fig.layout.yaxis.range[0] < 0
        assert fig.layout.yaxis.range[1] > 100

    def test_empty_figure(self):
        fig = go.Figure()
        result = range_frame(fig)
        assert result is fig

    def test_multiple_traces(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2], y=[10, 20], name="A"))
        fig.add_trace(go.Scatter(x=[3, 4], y=[5, 40], name="B"))
        range_frame(fig, pad=0.0)
        assert fig.layout.xaxis.range[0] == 1
        assert fig.layout.xaxis.range[1] == 4
        assert fig.layout.yaxis.range[0] == 5
        assert fig.layout.yaxis.range[1] == 40

    def test_single_value_uses_unit_pad(self):
        fig = _line_fig(xs=[5, 5], ys=[10, 10])
        range_frame(fig, pad=0.02)
        # When range is 0, pad defaults to 1
        assert fig.layout.xaxis.range[0] == 4
        assert fig.layout.xaxis.range[1] == 6


class TestDirectLabel:
    def test_adds_annotations(self):
        fig = _line_fig()
        direct_label(fig)
        assert len(fig.layout.annotations) == 1
        assert fig.layout.annotations[0].text == "A"

    def test_hides_legend(self):
        fig = _line_fig()
        direct_label(fig)
        assert fig.layout.showlegend is False

    def test_position_right(self):
        fig = _line_fig(xs=[1, 2, 3], ys=[10, 20, 30])
        direct_label(fig, position="right")
        ann = fig.layout.annotations[0]
        assert ann.x == 3
        assert ann.y == 30

    def test_position_left(self):
        fig = _line_fig(xs=[1, 2, 3], ys=[10, 20, 30])
        direct_label(fig, position="left")
        ann = fig.layout.annotations[0]
        assert ann.x == 1
        assert ann.y == 10

    def test_skips_unnamed_trace(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4], name=""))
        direct_label(fig)
        assert len(fig.layout.annotations) == 0

    def test_extracts_line_color(self):
        fig = _line_fig()
        direct_label(fig)
        assert fig.layout.annotations[0].font.color == "#ff0000"

    def test_extracts_marker_color(self):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[1, 2],
                y=[3, 4],
                name="B",
                mode="markers",
                marker={"color": "#00ff00"},
            )
        )
        direct_label(fig)
        assert fig.layout.annotations[0].font.color == "#00ff00"

    def test_skips_trace_without_xy(self):
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=["a", "b"], values=[1, 2]))
        fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4], name="ok"))
        direct_label(fig)
        assert len(fig.layout.annotations) == 1
        assert fig.layout.annotations[0].text == "ok"

    def test_returns_figure(self):
        fig = _line_fig()
        assert direct_label(fig) is fig


class TestSparkline:
    def test_basic(self):
        fig = sparkline([1, 3, 2, 5, 4])
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2  # line + endpoints

    def test_dimensions(self):
        fig = sparkline([1, 2, 3], width=300, height=50)
        assert fig.layout.width == 300
        assert fig.layout.height == 50

    def test_no_endpoints(self):
        fig = sparkline([1, 2, 3], show_endpoints=False)
        assert len(fig.data) == 1

    def test_axes_hidden(self):
        fig = sparkline([1, 2, 3])
        assert fig.layout.xaxis.visible is False
        assert fig.layout.yaxis.visible is False

    def test_single_value_no_endpoints(self):
        fig = sparkline([42])
        # < 2 values, no endpoints trace
        assert len(fig.data) == 1

    def test_custom_color(self):
        fig = sparkline([1, 2], color="#abcdef")
        assert fig.data[0].line.color == "#abcdef"


class TestAnnotatePoint:
    def test_adds_annotation(self):
        fig = go.Figure()
        result = annotate_point(fig, x=5, y=10, text="peak")
        assert result is fig
        assert len(fig.layout.annotations) == 1
        ann = fig.layout.annotations[0]
        assert ann.x == 5
        assert ann.y == 10
        assert ann.text == "peak"
        assert ann.showarrow is True

    def test_custom_offset(self):
        fig = go.Figure()
        annotate_point(fig, x=0, y=0, text="t", ay=-50)
        assert fig.layout.annotations[0].ay == -50


class TestStripChartjunk:
    def test_white_background(self):
        fig = go.Figure()
        strip_chartjunk(fig)
        assert fig.layout.plot_bgcolor == "white"
        assert fig.layout.paper_bgcolor == "white"

    def test_no_legend(self):
        fig = go.Figure()
        strip_chartjunk(fig)
        assert fig.layout.showlegend is False

    def test_axes_configured(self):
        fig = go.Figure()
        strip_chartjunk(fig)
        assert fig.layout.xaxis.showgrid is False
        assert fig.layout.xaxis.showline is True
        assert fig.layout.yaxis.showgrid is False
        assert fig.layout.yaxis.showline is True

    def test_returns_figure(self):
        fig = go.Figure()
        assert strip_chartjunk(fig) is fig
