"""Curated color palettes for Tufte-style Plotly charts.

Principles:
- Gray-first: muted tones that don't fight the data
- Spotlight: one saturated accent against desaturated context
- Colorblind-safe: tested against deuteranopia/protanopia
- Minimal: 3-5 colors max; if you need more, rethink the chart
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """A named color palette with a defined use case."""

    name: str
    colors: tuple[str, ...]
    description: str

    @property
    def colorway(self) -> list[str]:
        """Return as a list for Plotly's colorway parameter."""
        return list(self.colors)

    def spotlight(self, index: int = 0) -> list[str]:
        """Return palette with one color saturated, rest grayed out.

        Use this to direct attention to a single series.
        """
        gray = "#b0b0b0"
        return [c if i == index else gray for i, c in enumerate(self.colors)]


# --- Core palettes ---

# Classic Tufte: ink-like tones, understated, serious
INK = Palette(
    name="ink",
    colors=("#2b2b2b", "#636363", "#969696", "#bdbdbd", "#d9d9d9"),
    description="Grayscale ink tones. Maximum data-ink ratio.",
)

# Warm earth: for financial, business, human-interest data
EARTH = Palette(
    name="earth",
    colors=("#8c510a", "#d8b365", "#5ab4ac", "#01665e", "#636363"),
    description="Warm earth tones. Good for business/financial charts.",
)

# Cool slate: for technical, engineering, scientific data
SLATE = Palette(
    name="slate",
    colors=("#2166ac", "#67a9cf", "#ef8a62", "#b2182b", "#636363"),
    description="Cool blue-red diverging. Good for technical/scientific charts.",
)

# Qualitative: for categorical data, max 5 distinct groups
QUALITATIVE = Palette(
    name="qualitative",
    colors=("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"),
    description="Distinct categorical colors. Colorblind-safe (Tableau 10 subset).",
)

# Minimal duo: when you only have 2 series (the common case)
DUO = Palette(
    name="duo",
    colors=("#2b2b2b", "#e15759"),
    description="Two-color: dark ink + red accent. Most charts need only this.",
)

# Sequential: for ordered/continuous data
SEQUENTIAL = Palette(
    name="sequential",
    colors=("#f7f7f7", "#d9d9d9", "#969696", "#525252", "#252525"),
    description="Light-to-dark sequential. For heatmaps and ordered data.",
)

# All palettes, accessible by name
ALL: dict[str, Palette] = {
    p.name: p for p in [INK, EARTH, SLATE, QUALITATIVE, DUO, SEQUENTIAL]
}

# Default palette used by the template
DEFAULT = QUALITATIVE


def get(name: str) -> Palette:
    """Get a palette by name. Raises KeyError if not found."""
    if name not in ALL:
        available = ", ".join(sorted(ALL))
        msg = f"Unknown palette {name!r}. Available: {available}"
        raise KeyError(msg)
    return ALL[name]
