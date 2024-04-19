from altair import Chart
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    data = df[[x, y, target]]
    title = f"{y} by {x} for {target}"
    chart_obj = Chart(data, title=title).mark_circle(size=100).encode(
        x=x,
        y=y,
        color=target,
        tooltip=[x, y, target]
    ).properties(
        width=900,
        height=900,
        background='#202020',
        padding=10
    ).configure_axis(
        titleFontSize=25,
        labelFontSize=20
    ).configure_title(
        fontSize=24
    ).configure_legend(
        gradientLength=500,
        gradientThickness=20,
        titleFontSize=20,
        labelFontSize=20
    )
    return chart_obj
