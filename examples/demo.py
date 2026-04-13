import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import plotly.express as px

    import nolegend

    nolegend.activate(dark=mo.app_meta().theme == "dark")
    return mo, nolegend, px


@app.cell
def _(mo):
    mo.md("""
    # nolegend demo
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Line chart with direct labels
    """)
    return


@app.cell
def _(px):
    # --- Synthetic data ---
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    north = [12, 14, 18, 24, 30, 35, 38, 36, 28, 20, 15, 13]
    south = [8, 9, 10, 14, 18, 20, 22, 21, 17, 12, 9, 8]

    rows = []
    for m, n, s in zip(months, north, south, strict=False):
        rows.append({"month": m, "revenue": n, "region": "North"})
        rows.append({"month": m, "revenue": s, "region": "South"})

    fig_line = px.line(
        rows,
        x="month",
        y="revenue",
        color="region",
        template="tufte",
        title="North region drove 2x the revenue of South across all months",
    )
    return (fig_line,)


@app.cell
def _(fig_line, mo, nolegend):
    nolegend.direct_label(fig_line)
    fig_line.update_layout(
        yaxis_title="Revenue ($M)",
        margin={"r": 80},
    )
    mo.ui.plotly(fig_line)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Scatter with range frame and annotation
    """)
    return


@app.cell
def _(mo, nolegend, px):
    projects = {
        "name": [
            "Alpha",
            "Beta",
            "Gamma",
            "Delta",
            "Epsilon",
            "Zeta",
            "Eta",
            "Theta",
            "Iota",
            "Kappa",
        ],
        "cost": [120, 340, 200, 80, 450, 150, 290, 60, 380, 220],
        "impact": [45, 72, 58, 30, 90, 42, 68, 25, 85, 55],
    }

    fig_scatter = px.scatter(
        projects,
        x="cost",
        y="impact",
        hover_name="name",
        template="tufte",
        title="Epsilon and Iota dominate the efficiency frontier",
    )

    nolegend.range_frame(fig_scatter)
    nolegend.annotate_point(
        fig_scatter,
        x=450,
        y=90,
        text="Epsilon: highest ROI",
    )
    fig_scatter.update_layout(
        xaxis_title="Cost ($K)",
        yaxis_title="Impact score",
    )

    mo.ui.plotly(fig_scatter)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Horizontal bar chart
    """)
    return


@app.cell
def _(mo, nolegend, px):
    categories = {
        "category": [
            "Infrastructure",
            "Marketing",
            "R&D",
            "Support",
            "Sales",
        ],
        "spend": [420, 310, 580, 190, 350],
    }

    fig_bar = px.bar(
        categories,
        x="spend",
        y="category",
        orientation="h",
        template="tufte",
        title="R&D accounts for 31% of total spend",
    )

    nolegend.strip_chartjunk(fig_bar)
    fig_bar.update_layout(
        xaxis_title="Spend ($K)",
        yaxis_title=None,
    )

    mo.ui.plotly(fig_bar)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Sparkline KPI row
    """)
    return


@app.cell
def _(mo, nolegend):
    def kpi_spark(label, values, current):
        spark = nolegend.sparkline(values, width=120, height=30)
        return mo.vstack(
            [
                mo.md(f"**{label}**"),
                mo.ui.plotly(spark),
                mo.md(f"### {current}"),
            ]
        )

    mo.hstack(
        [
            kpi_spark("ARR", [8.1, 8.9, 9.4, 10.2, 10.8, 11.5, 12.4], "$12.4M"),
            kpi_spark("Churn", [3.8, 3.5, 3.1, 2.8, 2.5, 2.3, 2.1], "2.1%"),
            kpi_spark("NPS", [52, 55, 58, 61, 63, 65, 67], "67"),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Palette comparison — duo vs earth
    """)
    return


@app.cell
def _(mo, nolegend, px):
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    data_palette = []
    for q, a, b in zip(quarters, [40, 55, 70, 60], [30, 45, 50, 65], strict=False):
        data_palette.append({"quarter": q, "value": a, "series": "Product A"})
        data_palette.append({"quarter": q, "value": b, "series": "Product B"})

    fig_duo = px.line(
        data_palette,
        x="quarter",
        y="value",
        color="series",
        template=nolegend.with_palette("duo"),
        title="Product B overtook A in Q4",
    )
    nolegend.direct_label(fig_duo)
    fig_duo.update_layout(yaxis_title="Units (K)", margin={"r": 80})

    fig_earth = px.line(
        data_palette,
        x="quarter",
        y="value",
        color="series",
        template=nolegend.with_palette("earth"),
        title="Same data, earth palette",
    )
    nolegend.direct_label(fig_earth)
    fig_earth.update_layout(yaxis_title="Units (K)", margin={"r": 80})

    mo.hstack([mo.ui.plotly(fig_duo), mo.ui.plotly(fig_earth)])
    return


if __name__ == "__main__":
    app.run()
