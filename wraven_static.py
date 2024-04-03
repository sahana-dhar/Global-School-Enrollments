import pandas as pd
import geopandas as gpd
import altair as alt

# Load the data
data = pd.read_csv('global_country_data.csv', skiprows=4)
df = pd.DataFrame(data)

# Filter rows where Indicator Name contains "Number of deaths ages 20-24 years"
filtered_data = df[df['Indicator Name'].str.contains("Number of deaths ages 20-24 years")]

# Load the world map shapefile using Geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world map dataframe with the filtered data
merged_data = world.merge(filtered_data, how='left', left_on='iso_a3', right_on='Country Code')

# Create an Altair chart
chart = alt.Chart(merged_data).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.Color('2016:Q', scale=alt.Scale(scheme='orangered'), title='Number of Deaths'),
    tooltip=['name:N', '2016:Q']
).properties(
    width=800,
    height=500,
    title='Number of Deaths Ages 20-24 Years by Country in 2016'
).project(
    type='naturalEarth1'
).configure_title(
    fontSize=14,
    font='Arial',
    color='black'
).configure_axis(
    titleColor='black',
    titleFontSize=12,
    labelFontSize=10,
    labelColor='black'
).configure_legend(
    titleColor='black',
    titleFontSize=12,
    labelFontSize=10,
    labelColor='black'
).configure_view(
    strokeWidth=0
).configure_title(
    anchor='start'
).interactive()

# Save the Altair chart as an HTML file
chart.save('interactive_hover_map.html')
