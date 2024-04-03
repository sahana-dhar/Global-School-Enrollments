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

# Create a dropdown menu for selecting the column to plot
column_dropdown = alt.binding_select(options=[str(year) for year in range(1960, 2023)])
column_select = alt.selection_single(fields=['column'], bind=column_dropdown, name='Select')

# Create an Altair chart
chart = alt.Chart(merged_data).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.condition(
        column_select,
        alt.Color('data:Q', scale=alt.Scale(scheme='orangered'), title='Number of Deaths'),
        alt.value('lightgray')  # Default color when no column is selected
    ),
    tooltip=['name:N', alt.Tooltip('data:Q', format='.0f')]  # Show the selected column's value
).properties(
    width=800,
    height=500,
    title='Number of Deaths Ages 20-24 Years by Country'
).project(
    type='naturalEarth1'
).add_selection(
    column_select
).transform_calculate(
    data=alt.expr.if_(column_select, f'datum["{{column_select}}"]', alt.value(0))  # Correctly handle no selection
).transform_filter(
    column_select
).interactive()

# Save the Altair chart as an HTML file
chart.save('interactive_map_with_dropdown.html')
