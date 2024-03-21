# Install the module
import pandas as pd
import altair as alt
from vega_datasets import data  # import vega_datasets
cars = data.cars()
chart = alt.Chart(cars).mark_point().encode(
    alt.Y('Miles_per_Gallon:Q'),
    alt.X('Horsepower:Q'),
    alt.Size('Acceleration:Q'),
    alt.Color('Cylinders:O'),
    alt.OpacityValue(.5)
)
chart.save('chart1.html')