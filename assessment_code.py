#These are all the modules i plan on using in the development
import pycountry_convert as pc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gp

def converting_country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except KeyError:
        if(country_name == "The Bahamas"):
            country_continent_name = 'North America'
        if(country_name == "Vatican City"):  
            country_continent_name = 'Europe'
        if(country_name == "Timor"):  
            country_continent_name = 'Asia'

    return country_continent_name
    
    

#First i get the data
data = pd.read_csv("Global_Education.csv" , encoding='ISO-8859-1')

# Assuming 'data' is a pandas DataFrame with the correct columns.
country = data["Countries and areas"]  # This should be a Series or list of country names.
unemployment = data["Unemployment_Rate"].astype(float)  # This should be a Series of floats.
continents = (country.apply(converting_country_to_continent)) #This gets the continents for each country

#Merging the continent and the unemployment rrate to one dataframe
continent_Unemployment_merged = pd.concat([continents , unemployment] , axis = 1) 

# Ensure the merged DataFrame has appropriate column names
continent_Unemployment_merged.columns = ['Continent', 'Unemployment_Rate']

# Grouping the data by the 'Continent' column
grouped_data = continent_Unemployment_merged.groupby('Continent')

# Calculating the mean unemployment rate per continent
mean_unemployment_per_continent = grouped_data.mean()



