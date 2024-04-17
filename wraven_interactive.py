import pandas as pd
import geopandas as gpd
import altair as alt

# Load the data
data = pd.read_csv('global_country_data.csv', skiprows=4)
df = pd.DataFrame(data)

# Filter rows where Indicator Name contains "Compulsory education, duration"
filtered_data = df[df['Indicator Name'].str.contains("Compulsory education, duration")]

# Load the world map shapefile using Geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world map dataframe with the filtered data
merged_data = world.merge(filtered_data, how='left', left_on='iso_a3', right_on='Country Code').fillna(0)

# Get the year input from the user
year = input("Enter the year (e.g., 2016): ")

# Create an Altair chart
chart = alt.Chart(merged_data).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.condition(
        alt.datum[year] == 0,
        alt.value('grey'),
        alt.Color(f'{year}:Q', scale=alt.Scale(scheme='viridis'), title='Compulsory education, duration')
    ),
    tooltip=['name:N', f'{year}:Q']
).properties(
    width=800,
    height=500,
    title=f'Compulsory education, duration in {year}'
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
chart.save(f'interactive_hover_map_{year}.html')
