#These are all the modules i plan on using in the development
import pycountry_convert as pc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import geopandas as gpd
import contextily as ctx

#This is the method i used to get the world map
def get_world_map():
    world_map = getting_the_world_map(plot_data=True)
    country, unemployment, continents , data = getting_the_data()  # 'self' is passed implicitly
    unemployment_dict = world_map.manipulating_the_data(continents, unemployment)  # 'self' is passed implicitly
    world_map.printing_the_data(unemployment_dict) 
    
def drawing_OOSR_by_age(age_group, column_index, age_group_name):
    oosr_instance = OOSRate(plot_data=True)  # Create an instance of OOSRate

    # Retrieve data using the get_data method with the specified column index
    country, unemployment, continents, boys_without_education, girls_without_education = oosr_instance.get_data(column_index)
    
    # Calculate the education rates dictionaries for boys, girls, and average
    education_dict_boys = oosr_instance.manipulate_data(continents, boys_without_education, girls_without_education, "boys")
    education_dict_girls = oosr_instance.manipulate_data(continents, boys_without_education, girls_without_education, "girls")
    education_dict_average = oosr_instance.manipulate_data(continents, boys_without_education, girls_without_education, "average")

    # Plot the bar charts for boys, girls, and average
    oosr_instance.graphs_showing_people_education(education_dict_boys, f"Out Of School Rate for Boys {age_group_name}")
    oosr_instance.graphs_showing_people_education(education_dict_girls, f"Out Of School Rate for Girls {age_group_name}")
    oosr_instance.graphs_showing_people_education(education_dict_average, f"Average Out Of School Rate of people {age_group_name}")

    
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

    def manipulating_the_data(self , continents , unemployment):
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
    
class OOSRate:
    
    def __init__(self, plot_data):
        self.plot_data = plot_data
        
    #This gets the basic data i would need
    def get_data(self , column):
        country, unemployment, continents, data = getting_the_data()
        boys_without_primary_education = data.iloc[:, column]
        girls_without_primary_education = data.iloc[:, (column+1)]
        
        return country, unemployment, continents, boys_without_primary_education, girls_without_primary_education
    
    #Manipulating the data to get the people without further education
    def manipulate_data(self, continents , boys_without_primary_education, girls_without_primary_education , gender):
        
        #Getting the average percent of people with education 
        if(gender == "boys"):
            education = boys_without_primary_education
        elif(gender == "girls"):
            education = girls_without_primary_education
        else:
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
    def graphs_showing_people_education(self, education_dict , title):
        # Extract continents and education rates from the dictionary
        continents = list(education_dict.keys())
        education_rates = list(education_dict.values())

        plt.figure(figsize=(10, 6))
        plt.bar(continents, education_rates, color='blue')
        plt.xlabel('Continent')
        plt.ylabel('Average Rate of Out-of-School Students (%)')
        plt.title(title)
        plt.xticks(rotation=45)  # Rotate continent names for better readability if needed
        plt.tight_layout()  # Adjust layout
        plt.show()

if __name__ == "__main__":

    #First graph of the world map
    get_world_map()
    
    # Now, you can call the function with specific parameters for each age group
    drawing_OOSR_by_age("Primary Age", 5, "aged 5-11")
    drawing_OOSR_by_age("Lower Secondary Age", 7, "aged 12-14")
    drawing_OOSR_by_age("Upper Secondary Age", 9, "aged 16-19")

