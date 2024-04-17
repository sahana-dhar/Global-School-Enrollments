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

# Create list of column names for dropdown menu
years = ([str(year) for year in range(1960, 2023)])

# Create a dropdown menu for selecting the column to plot
column_selector = alt.binding_select(options=years)
column_dropdown = alt.selection_point(fields=['key'], bind=column_selector, name='Select')

# Create an Altair chart
chart = alt.Chart(merged_data).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.condition(
        column_dropdown,
        alt.Color('data:Q', scale=alt.Scale(scheme='orangered'), title='Compulsory education, duration (years)'),
        alt.value('lightgray')  # Default color when no column is selected
    ),
    tooltip=['name:N', alt.Tooltip('data:Q', format='.0f')]  # Show the selected column's value
).properties(
    width=800,
    height=500,
    title='Compulsory education, duration (years)'
).project(
    type='naturalEarth1'
).add_params(
    column_dropdown
).transform_filter(
    column_dropdown
).interactive()

# Save the Altair chart as an HTML file
chart.save('Wraven_interactive.html')
