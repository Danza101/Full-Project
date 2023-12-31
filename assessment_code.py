#These are all the modules i plan on using in the development
import pycountry_convert as pc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import geopandas as gpd
import contextily as ctx
 
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

class getting_the_world_map():
    
    def __init__(self, plot_data):
        self.plot_data = plot_data
    
    def getting_the_data(self):
        #First i get the data
        data = pd.read_csv("Global_Education.csv" , encoding='ISO-8859-1')
        
        # Filter out specific warnings from the pycountry library
        warnings.filterwarnings("ignore", message="Country's official_name not found. Country name provided instead.")
        warnings.filterwarnings("ignore", message="Country's common_name not found. Country name provided instead.")
        
        # Assuming 'data' is a pandas DataFrame with the correct columns.
        country = data["Countries and areas"]  # This should be a Series or list of country names.
        unemployment = data["Unemployment_Rate"].astype(float)  # This should be a Series of floats.
        continents = (country.apply(converting_country_to_continent)) #This gets the continents for each country
        
        return country , unemployment , continents , data

    def manipulating_the_data(self , country , unemployment , continents):
        #Merging the continent and the unemployment rrate to one dataframe
        continent_Unemployment_merged = pd.concat([continents , unemployment] , axis = 1) 

        # Ensure the merged DataFrame has appropriate column names
        continent_Unemployment_merged.columns = ['continent', 'Unemployment_Rate']

        # Grouping the data by the 'Continent' column
        grouped_data = continent_Unemployment_merged.groupby('continent')

        # Calculating the mean unemployment rate per continent
        mean_unemployment_per_continent = grouped_data.mean()

        # Reset the index to convert 'Continent' from an index to a column
        mean_unemployment_per_continent = mean_unemployment_per_continent.reset_index()

        #Changing the datatype to be a dictionary data type
        unemployment_dict = dict(zip(mean_unemployment_per_continent['continent'], mean_unemployment_per_continent['Unemployment_Rate']))
        
        return unemployment_dict

    def printing_the_data(self , unemployment_dict):
        # Load the shapefile
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        #This gets each country from world data and 
        world['Data'] = world['continent'].map(unemployment_dict)

        #This makes sure the graph only shows if the code is cqalled from this 
        if self.plot_data:
            # Create a plot
            fig, ax = plt.subplots(figsize=(12, 6))
            world.plot(ax=ax, column='Data', legend=True, cmap='OrRd')

            # Add a basemap
            ctx.add_basemap(ax, crs=world.crs.to_string())

            #This displays the heat map of average unemployment in different countries
            plt.show()
    

if __name__ == "__main__":
    world_map = getting_the_world_map(plot_data=True)
    country, unemployment, continents , data = world_map.getting_the_data()  # 'self' is passed implicitly
    unemployment_dict = world_map.manipulating_the_data(country, unemployment, continents)  # 'self' is passed implicitly
    world_map.printing_the_data(unemployment_dict)  # 'self' is passed implicitly, 'plot_data' is accessed via 'self.plot_data'
