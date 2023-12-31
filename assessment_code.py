#These are all the modules i plan on using in the development
import pycountry_convert as pc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import geopandas as gpd
import contextily as ctx

def getting_the_data():
    
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

    def manipulating_the_data(self , unemployment , continents):
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
    
class LowerLiteracyRate:
    
    def __init__(self, plot_data):
        self.plot_data = plot_data
        
    #This gets the basic data i would need
    def get_data(self , column):
        country, unemployment, continents, data = getting_the_data()
        boys_without_primary_education = data.iloc[:, column]
        girls_without_primary_education = data.iloc[:, (column+1)]
        
        return country, unemployment, continents, boys_without_primary_education, girls_without_primary_education
    
    #Manipulating the data to get the people without further education
    def manipulate_data(self, continent , boys_without_primary_education, girls_without_primary_education):
        
        #Getting the average percent of people with education 
        education = (boys_without_primary_education + girls_without_primary_education) / 2
        
        #Merging the continent and the unemployment rrate to one dataframe
        continent_education_merged = pd.concat([continents , education] , axis = 1) 

        # Ensure the merged DataFrame has appropriate column names
        continent_education_merged.columns = ['continent', 'education']

        # Grouping the data by the 'Continent' column
        grouped_data = continent_education_merged.groupby('continent')

        # Calculating the mean unemployment rate per continent
        mean_education_per_continent = grouped_data.mean()

        # Reset the index to convert 'Continent' from an index to a column
        mean_education_per_continent = mean_education_per_continent.reset_index()

        #Changing the datatype to be a dictionary data type
        education_dict = dict(zip(mean_education_per_continent['continent'], mean_education_per_continent['education']))
        
        return education_dict

    #Printing out the results and creating a bar chart
    def graphs_showing_people_with_lower_education(self, education_dict):
        # Extract continents and education rates from the dictionary
        continents = list(education_dict.keys())
        education_rates = list(education_dict.values())

        plt.figure(figsize=(10, 6))
        plt.bar(continents, education_rates, color='blue')
        plt.xlabel('Continent')
        plt.ylabel('Average Rate of Out-of-School Students (%)')
        plt.title('Out-of-school rate for lower secondary age students')
        plt.xticks(rotation=45)  # Rotate continent names for better readability if needed
        plt.tight_layout()  # Adjust layout
        plt.show()

        

    
#if __name__ == "__main__":
    #world_map = getting_the_world_map(plot_data=True)
    #country, unemployment, continents , data = getting_the_data()  # 'self' is passed implicitly
   #unemployment_dict = world_map.manipulating_the_data(country, unemployment)  # 'self' is passed implicitly
    #world_map.printing_the_data(unemployment_dict)  # 'self' is passed implicitly, 'plot_data' is accessed via 'self.plot_data'

if __name__ == "__main__":
    # ... (other code to initialize and retrieve data)

    # Create an instance of LowerLiteracyRate
    lower_lit_rate = LowerLiteracyRate(plot_data=True)
    
    # Retrieve data using the get_data method
    country, unemployment, continents, boys_without_primary_education , girls_without_primary_education = lower_lit_rate.get_data(7)
    
    # Calculate the education rates dictionary
    education_dict = lower_lit_rate.manipulate_data(continents, boys_without_primary_education, girls_without_primary_education)
    
    # Plot the bar chart
    lower_lit_rate.graphs_showing_people_with_lower_education(education_dict)
