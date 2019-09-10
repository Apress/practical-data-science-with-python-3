import altair as alt
from vega_datasets import data

source = data.anscombe()

base = alt.Chart(
    source, title = "Anscombe's Quartets"
).mark_circle(color = 'red').encode(
    alt.X('X', scale = alt.Scale(zero = True)),
    alt.Y('Y', scale = alt.Scale(zero = True)),
    column = 'Series'
).properties(
    width = 150,
    height = 150
).interactive()

base
