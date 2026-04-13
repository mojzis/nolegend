from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

from nolegend.template import (
    FONT_COLOR,
    FONT_COLOR_DARK,
    TUFTE,
    TUFTE_DARK,
    _make_axis,
    _make_template,
    activate,
    with_palette,
)


class TestMakeAxis:
    def test_light_colors(self):
        ax = _make_axis(dark=False)
        assert ax["color"] == FONT_COLOR
        assert ax["linecolor"] == "#333333"

    def test_dark_colors(self):
        ax = _make_axis(dark=True)
        assert ax["color"] == FONT_COLOR_DARK
        assert ax["linecolor"] == "#555555"

    def test_no_grid(self):
        ax = _make_axis()
        assert ax["showgrid"] is False
        assert ax["zeroline"] is False
        assert ax["showline"] is True


class TestMakeTemplate:
    def test_returns_template(self):
        t = _make_template()
        assert isinstance(t, go.layout.Template)

    def test_light_background(self):
        t = _make_template(dark=False)
        assert t.layout.plot_bgcolor == "#fffff8"
        assert t.layout.paper_bgcolor == "#fffff8"

    def test_dark_background(self):
        t = _make_template(dark=True)
        assert t.layout.plot_bgcolor == "#1a1a1a"
        assert t.layout.paper_bgcolor == "#1a1a1a"

    def test_colorway_set(self):
        t = _make_template()
        assert len(t.layout.colorway) > 0


class TestRegistration:
    def test_templates_registered(self):
        assert "tufte" in pio.templates
        assert "tufte_dark" in pio.templates

    def test_tufte_matches_module_constant(self):
        assert pio.templates["tufte"] == TUFTE
        assert pio.templates["tufte_dark"] == TUFTE_DARK


class TestActivate:
    def test_activate_light(self):
        activate(dark=False)
        assert pio.templates.default == "tufte"

    def test_activate_dark(self):
        activate(dark=True)
        assert pio.templates.default == "tufte_dark"


class TestWithPalette:
    def test_returns_name(self):
        name = with_palette("earth")
        assert name == "tufte_earth"

    def test_dark_variant_name(self):
        name = with_palette("earth", dark=True)
        assert name == "tufte_earth_dark"

    def test_registers_template(self):
        name = with_palette("slate")
        assert name in pio.templates

    def test_uses_palette_colorway(self):
        from nolegend.colors import EARTH

        # Remove cached entry to force fresh creation
        name = "tufte_earth"
        if name in pio.templates:
            del pio.templates[name]
        result = with_palette("earth")
        assert result == name
        t = pio.templates[name]
        assert list(t.layout.colorway) == EARTH.colorway

    def test_cached_on_second_call(self):
        name = with_palette("duo")
        assert with_palette("duo") == name
