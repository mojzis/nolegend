from __future__ import annotations

import pytest

from nolegend.colors import (
    ALL,
    DEFAULT,
    DUO,
    EARTH,
    INK,
    QUALITATIVE,
    SEQUENTIAL,
    SLATE,
    Palette,
    get,
)


class TestPalette:
    def test_frozen(self):
        p = Palette(name="test", colors=("#aaa",), description="d")
        with pytest.raises(AttributeError):
            p.name = "other"  # type: ignore[misc]  # ty: ignore[invalid-assignment]

    def test_colorway_returns_list(self):
        p = Palette(name="t", colors=("#111", "#222"), description="d")
        cw = p.colorway
        assert cw == ["#111", "#222"]
        assert isinstance(cw, list)

    def test_spotlight_highlights_index(self):
        p = Palette(name="t", colors=("#aa0000", "#00bb00", "#0000cc"), description="d")
        result = p.spotlight(1)
        assert result[0] == "#b0b0b0"
        assert result[1] == "#00bb00"
        assert result[2] == "#b0b0b0"

    def test_spotlight_default_index(self):
        p = Palette(name="t", colors=("#aa0000", "#00bb00"), description="d")
        result = p.spotlight()
        assert result[0] == "#aa0000"
        assert result[1] == "#b0b0b0"

    def test_spotlight_out_of_bounds(self):
        p = Palette(name="t", colors=("#aa0000",), description="d")
        # spotlight with out-of-range index just produces all gray
        result = p.spotlight(5)
        assert result == ["#b0b0b0"]


class TestPredefined:
    def test_all_palettes_registered(self):
        expected = {"ink", "earth", "slate", "qualitative", "duo", "sequential"}
        assert set(ALL.keys()) == expected

    def test_names_match_keys(self):
        for key, palette in ALL.items():
            assert palette.name == key

    def test_default_is_qualitative(self):
        assert DEFAULT is QUALITATIVE

    @pytest.mark.parametrize(
        "palette",
        [INK, EARTH, SLATE, QUALITATIVE, DUO, SEQUENTIAL],
    )
    def test_palette_has_colors(self, palette: Palette):
        assert len(palette.colors) >= 2
        assert all(c.startswith("#") for c in palette.colors)


class TestGet:
    def test_get_existing(self):
        assert get("ink") is INK
        assert get("duo") is DUO

    def test_get_unknown_raises(self):
        with pytest.raises(KeyError, match="Unknown palette 'nope'"):
            get("nope")

    def test_get_error_lists_available(self):
        with pytest.raises(KeyError, match="Available:"):
            get("nope")
