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

# List of columns to drop
columns_to_drop = [
    '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
    '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
    '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
    '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994'
]

years_kept = ['1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
       '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
       '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

# Drop the columns
merged_data.drop(columns=columns_to_drop, inplace=True)

# Melt the DataFrame
melted_data = pd.melt(
    merged_data,
    id_vars=['name', 'iso_a3', 'geometry', 'Country Code', 'Indicator Name'],
    value_vars=years_kept,
    var_name='year',
    value_name='duration'
)

# Create a selection with initial value
year_dropdown = alt.binding_select(options=years_kept)
year_selection = alt.selection_single(fields=['year'], bind=year_dropdown, name="Select", value='1995')

# Create the choropleth map
chart = alt.Chart(melted_data).transform_filter(
    year_selection
).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.condition(
        alt.datum['duration'] == 0,
        alt.value('grey'),
        alt.Color('duration:Q', scale=alt.Scale(scheme='viridis'), title='Duration')
    ),
    tooltip=['name:N', 'duration:Q']
).add_selection(
    year_selection
).properties(
    width=800,
    height=500,
    title={
        "text": f'Duration of compulsory education (Years)',
        "subtitle": "Countries with no data provided are marked in grey",
        "fontSize": 16,
        "font": "Arial",
        "color": "black"
    }
).project(
    type='naturalEarth1'
)

# Save the chart to an HTML file
chart.save("wraven_interactive_map.html")
