import pandas as pd
import geopandas as gpd
import altair as alt
import numpy as np

# Load the data
data = pd.read_csv('global_country_data.csv', skiprows=4)
df = pd.DataFrame(data)

# Filter rows where Indicator Name contains "Number of deaths ages 20-24 years"
filtered_data = df[df['Indicator Name'].str.contains("Number of deaths ages 20-24 years")]

#print(filtered_data)


filtered_data = filtered_data.drop(["Indicator Code", "Indicator Name",  "Unnamed: 67"], axis=1)

#print(filtered_data)

list = filtered_data.columns.values.tolist()
print(list[-1])

#print(np.dtype(f))

print(range(1960,2022))