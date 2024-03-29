#These are all the modules i plan on using in the development
import pycountry_convert as pc
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import geopandas as gpd
import contextily as ctx

def highest_and_lowest_unemployment_rates():
    rate_extractor = countries_unemployment_rate(plot_data=True)
    extreme_unemployment_df = rate_extractor.get_extreme_unemployment_by_continent()
    rate_extractor.plot_extreme_unemployment_by_continent()
    
#This is the method i used to get the world map
def get_world_map():
    world_map = getting_the_world_map(plot_data=True)
    country, unemployment, continents , data = getting_the_data() 
    unemployment_dict = world_map.manipulating_the_data(continents, unemployment)  # 'self' is passed implicitly
    world_map.printing_the_data(unemployment_dict) 
    
def drawing_OOSR_by_age(column_index, age_group_name):
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
    country_continent_name = "Unknown"  # Initialize with a default value
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except KeyError:
        if country_name == "The Bahamas":
            country_continent_name = 'North America'
        elif country_name == "Vatican City":  
            country_continent_name = 'Europe'
        elif country_name == "Timor":  
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

class countries_unemployment_rate:
    def __init__(self, plot_data):
        self.plot_data = plot_data
        self.country, self.unemployment, self.continents, self.data = getting_the_data()
        self.data['Continent'] = self.continents  # assuming 'self.continents' is a Series from 'getting_the_data()'

    def get_extreme_unemployment_by_continent(self):
        # Check if the necessary columns are present
        if 'Continent' not in self.data.columns or 'Unemployment_Rate' not in self.data.columns:
            raise ValueError("Dataframe must contain 'Continent' and 'Unemployment_Rate' columns")

        # Group by 'Continent' and get the index of the max and min 'Unemployment_Rate' in each group
        idx_max = self.data.groupby('Continent')['Unemployment_Rate'].idxmax()
        idx_min = self.data.groupby('Continent')['Unemployment_Rate'].idxmin()

        # Retrieve the rows for max and min unemployment rates
        max_unemployment_countries = self.data.loc[idx_max, ['Continent', 'Countries and areas', 'Unemployment_Rate']]
        min_unemployment_countries = self.data.loc[idx_min, ['Continent', 'Countries and areas', 'Unemployment_Rate']]

        # Rename columns for clarity
        max_unemployment_countries.rename(columns={'Countries and areas': 'Country', 'Unemployment_Rate': 'Max Unemployment Rate'}, inplace=True)
        min_unemployment_countries.rename(columns={'Countries and areas': 'Country', 'Unemployment_Rate': 'Min Unemployment Rate'}, inplace=True)

        # Merge the results into a single DataFrame for output
        extreme_unemployment = pd.merge(
            max_unemployment_countries.reset_index(drop=True), 
            min_unemployment_countries.reset_index(drop=True), 
            on='Continent', 
            suffixes=('_Max', '_Min')
        )

        return extreme_unemployment
    
    def plot_extreme_unemployment_by_continent(self):
        
        if(self.plot_data == True):
            extreme_unemployment = self.get_extreme_unemployment_by_continent()

        # Get unique list of continents
        continents = extreme_unemployment['Continent'].unique()

        # Loop through continents and plot each one separately
        for continent in continents:
            # Filter data for the current continent
            continent_data = self.data[self.data['Continent'] == continent]

            # Find the country with the max unemployment rate
            max_unemployment = continent_data['Unemployment_Rate'].max()
            max_country = continent_data[continent_data['Unemployment_Rate'] == max_unemployment]['Countries and areas'].iloc[0]

            # Find the country with the min non-zero unemployment rate
            non_zero_min_data = continent_data[continent_data['Unemployment_Rate'] > 0]
            if not non_zero_min_data.empty:
                min_unemployment = non_zero_min_data['Unemployment_Rate'].min()
                min_country = non_zero_min_data[non_zero_min_data['Unemployment_Rate'] == min_unemployment]['Countries and areas'].iloc[0]
            else:
                min_unemployment = None
                min_country = "N/A"

            # Create a new figure for each continent
            plt.figure(figsize=(8, 4))

            # Plot the bar chart
            labels = ['Max Unemployment Country', 'Min Unemployment Country']
            values = [max_unemployment, min_unemployment if min_unemployment else 0]
            bars = plt.bar(labels, values, color=['red', 'green'])
            plt.title(f"{continent} - Unemployment Rates")
            plt.ylabel("Unemployment Rate (%)")
            plt.xticks(labels, [max_country, min_country])
            plt.ylim(0, max(values) + 5)  # Set y-axis limit to add some space at the top

            # Adding the text on top of the bars
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

            # Display each plot
            plt.show()


        
if __name__ == "__main__":

    #First graph of the world map
    get_world_map()
    
    # Now, you can call the function with specific parameters for each age group
    drawing_OOSR_by_age(5, "aged 5-11")
    drawing_OOSR_by_age(7, "aged 12-14")
    drawing_OOSR_by_age(9, "aged 16-19")
    
    #This will be code which draws countries with the highest and the lowest unemployment rate
    highest_and_lowest_unemployment_rates()
