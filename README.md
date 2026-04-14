# nolegend

*Remove the legend to become one.*

Tufte-style templates and helpers for Plotly. One import, beautiful charts.

Based on Edward Tufte's *The Visual Display of Quantitative Information*:
maximize data-ink ratio, remove chartjunk, direct-label instead of legends,
use range frames, and apply colorblind-safe palettes.

## Why this exists

There is no Tufte package for Plotly on PyPI. matplotlib has `matplotx`,
plotnine has `theme_tufte()`, ggplot2 has `ggthemes` — Plotly has nothing.
The closest built-in template (`simple_white`) removes gridlines but stops
there. The default Plotly output is noisy: legends, gridlines, aggressive
colors, titles that describe axes instead of insights.

nolegend fills that gap with opinionated defaults and easy overrides.

## What this is NOT

- Not a general visualization framework. Plotly only.
- Not a dashboard framework. Use marimo for layout.
- Not a Tufte orthodoxy enforcer. We take the useful parts (data-ink ratio,
  range frames, direct labeling, small multiples) and skip the dogma.
- Not a replacement for domain judgment. The library guides chart selection
  and color use, but the human picks the story.

## Install

```bash
uv add nolegend
```

### Claude Code skill

nolegend ships a visualization skill that teaches Claude Code the
px → go workflow, Tufte principles, color rules, and marimo patterns.

```bash
npx skills add mojzis/nolegend
```

Once installed, Claude Code will automatically apply nolegend conventions
whenever you create Plotly charts.

## Quick start

```python
import plotly.express as px
import nolegend

nolegend.activate()  # set as default template for all figures

df = px.data.gapminder().query("continent == 'Europe' and year == 2007")
fig = px.bar(df.nlargest(10, "gdpPercap"), x="country", y="gdpPercap")
fig.show()
```

## The px → go workflow

Start fast with Plotly Express, then refine:

```python
import plotly.express as px
import nolegend

# 1. Quick draft with px
fig = px.line(
    df, x="year", y="revenue", color="product",
    template="tufte",
)

# 2. Refine: axes span only the data
nolegend.range_frame(fig)

# 3. Refine: labels on the lines, not in a legend box
nolegend.direct_label(fig)

# 4. Refine: call out the key moment
nolegend.annotate_point(fig, x=2023, y=peak, text="Record quarter")

fig.show()
```

## Color palettes

Six curated, colorblind-safe palettes:

| Palette | Use case |
|---------|----------|
| `qualitative` | Categorical data (default) |
| `ink` | Grayscale, maximum data-ink |
| `duo` | Two series (dark + red accent) |
| `earth` | Business/financial |
| `slate` | Technical/scientific |
| `sequential` | Ordered/continuous data |

```python
# Use a specific palette
fig = px.line(df, ..., template=nolegend.with_palette("earth"))

# Spotlight: highlight one series, gray out the rest
colors = nolegend.QUALITATIVE.spotlight(index=2)
```

Hard ceiling of 5 colors per chart. Gray is a deliberate design tool, not
a leftover.

## Sparklines

Word-sized graphics, inline with text:

```python
spark = nolegend.sparkline([1, 4, 2, 5, 3, 7], width=150, height=30)
spark.show()
```

## Dark mode

```python
nolegend.activate(dark=True)
# or per-figure:
fig = px.scatter(df, ..., template="tufte_dark")
```

## In marimo notebooks

```python
import marimo as mo
import nolegend

# Auto-detect marimo theme
nolegend.activate(dark=mo.app_meta().theme == "dark")

# Reactive plotly charts
fig = px.scatter(df, x="x", y="y", template="tufte")
chart = mo.ui.plotly(fig)
```

## API

| Function | What it does |
|----------|-------------|
| `activate(dark=False)` | Set tufte as default template |
| `with_palette(name, dark=False)` | Register + return template with specific palette |
| `range_frame(fig, pad=0.02)` | Trim axes to data range |
| `direct_label(fig, position="right")` | Label lines directly, remove legend |
| `sparkline(values, ...)` | Create a word-sized trend graphic |
| `annotate_point(fig, x, y, text)` | Arrow annotation on a data point |
| `strip_chartjunk(fig)` | Quick cleanup of any Plotly figure |

## License

MIT
