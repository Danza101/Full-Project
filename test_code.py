import random
import pandas as pd
import awoc 
import unittest as test
import assessment_code as ac
from assessment_code import getting_the_world_map

def test_average_continents():
    return {'Africa': 4.775, 'Asia': 3.2133333333333334, 'Europe': 7.118, 'North America': 7.166666666666667, 'Oceania': 2.12, 'South America': 3.69}
    
#Checks the dictionary produces the correct ans
def testing_manipulating_data_func_in_ac_file(test_ans , actual_ans):
    if(test_ans == actual_ans):
        return True
    else:
        return False
    
def test_calc(proxy_file_df):
    oos_rate_instance = ac.OOSRate(False)
    countries = proxy_file_df["Country"]
    MaleOOS = proxy_file_df["Male (%)"].str.rstrip('%').astype(float)
    FemaleOOS = proxy_file_df["Female (%)"].str.rstrip('%').astype(float)

    # Create a list to store the continent for each country
    continents = [ac.converting_country_to_continent(country) for country in countries]
    
    # Convert the list to a pandas Series
    continents_series = pd.Series(continents)

    # Now call the manipulate_data method on this instance
    result = oos_rate_instance.manipulate_data(continents_series, MaleOOS, FemaleOOS, "neither")
    
    answer = {'Africa': 51.6375, 'Asia': 65.58166666666666, 'Europe': 56.34400000000001, 'North America': 64.215, 'Oceania': 93.055, 'South America': 54.379999999999995}
    
    return(result == answer)  




#Generating a 2d array mant to act as a proxy file for my testing
def getting_the_proxy_file():
    proxy_data = [
    ["Country", "Male (%)", "Female (%)", "Unemployment_Rate"],
    ["United States", "91.51%", "78.48%", 8.95],
    ["Canada", "53.92%", "29.56%", 5.67],
    ["Brazil", "48.16%", "60.60%", 3.69],
    ["Togo", "57.12%", "10.88%", 2.32],
    ["Germany", "53.14%", "77.27%", 9.46],
    ["France", "92.44%", "85.72%", 3.39],
    ["Italy", "70.18%", "10.28%", 7.73],
    ["Spain", "41.65%", "73.26%", 7.99],
    ["Japan", "27.61%", "61.82%", 2.23],
    ["China", "97.04%", "45.91%", 6.12],
    ["India", "94.91%", "66.20%", 1.29],
    ["Australia", "97.59%", "88.52%", 2.12],
    ["Russia", "29.80%", "29.70%", 7.02],
    ["Mexico", "37.75%", "94.07%", 6.88],
    ["Zimbabwe", "58.30%", "80.25%", 7.23]
]
    return proxy_data
    
def checking_the_continent(country):
    my_world = awoc.AWOC()
    continent_names = ['Europe', 'Africa', 'Oceania', 'North America', 'South America']
    
    # Create a dictionary to hold the countries with their respective continent
    continent_dict = {}
    for name in continent_names:
        countries = my_world.get_countries_list_of(name)
        for c in countries:
            continent_dict[c] = name
    
    # Find the continent for the given country
    return continent_dict.get(country, "Unknown")

def getting_the_data_from_assessment_code_file():
    
    try:
        # Create an instance of the class
        world_map = ac.getting_the_world_map(plot_data=False)

        # Call the instance method and capture its returned data
        country, unemployment, continents , data = ac.getting_the_data()
        
        return country , unemployment , continents , data
    except Exception as e:
        # Return the error message for debugging purposes
        return f"There is an error: {e}"

#This code is used to check if the columns in the dataset are the ones you expect
def test_data_function(data, data_checker):
    try:
        # Check if the data is the same length
        if len(data) != len(data_checker):
            return False

        # If the data is the same length, check all of the indexes match
        for i in range(len(data)):
            if not data.iloc[i].equals(data_checker.iloc[i]):
                return False
        return True
    except Exception as e:
        # Return the error message for debugging purposes
        return f"There is an error: {e}"

#This will be used to import the moduels from assessment code file
#It tries to downloads all the imports from the assessment_code file and if it isnt able it retuens the error
def checking_modules_installed():
    try:
        from assessment_code import pd
        from assessment_code import plt
        from assessment_code import np
        return(True)
    except ImportError:
        return(False)

# This is a function which uses anoother class to get all the countries in each continent   
def checking_correct_continent(country , continents , country_data_checker):
   
   #The first thing i need to do is find the continents which each the country data checker belongs to
    continents_data_checker = country_data_checker.apply(checking_the_continent)

    #Next thing is to check that the country matches the data needed
    try:
        for i in range(len(country)):
            #This checks the country i used in the dowmloaded file is the same as the county data in my coding file
            if(country[i] != country_data_checker[i]):
                print(country[i] + "||" + country_data_checker[i])
                return False
            #This checks if the country in the contines expected
            if (continents[i] != continents_data_checker[i]):
                if (continents_data_checker[i] == ("unknown")):
                    print(continents[i] + "||" + continents_data_checker[i])
                    return False
        return True    
    except Exception as e:
        # Return the error message for debugging purposes
        print("There is an error")
        return f"There is an error: {e}"    
    
# Requirements 1: Testing I have imported the correct imports to this file
class Test_Imports(test.TestCase):
    
    def setUp(self):
        # Common setup for each test method in this class
        self.country, self.unemployment, self.continents, self.data = getting_the_data_from_assessment_code_file()
        
    #calls method to check the data is good 
    def test_data_import(self):
        data_checker = pd.read_csv("Global_Education.csv", encoding='ISO-8859-1')
        self.assertEqual(test_data_function(self.data , data_checker) , True)
        
    def test_modules_imports(self):
        #This code tests that pandas, matplotlib and numpy has been downloaded properlly
        self.assertEqual(True , checking_modules_installed())

#Requirements 2: Testing that each country has gone to the correct continent
class TestGraphs(test.TestCase):

    def setUp(self):
        # Common setup for each test method in this class
        self.country, self.unemployment, self.continents, self.data = getting_the_data_from_assessment_code_file()
        self.proxy_file = getting_the_proxy_file()

    def test_correct_calculations(self):
        proxy_file_df = pd.DataFrame(self.proxy_file[1:], columns=self.proxy_file[0])
        self.assertEqual(True, test_calc(proxy_file_df))


    def test_correct_continent(self):
        proxy_file_df = pd.DataFrame(self.proxy_file[1:], columns=self.proxy_file[0])  # Convert to DataFrame if it's a list
        self.assertEqual(True, test_calc(proxy_file_df))

#Requirements 3: Testing my getting_the_world_map class logic works by using dummy data
class Test_World_Map(test.TestCase):
     
    def test_values_in_map(self):
        
        #Instantiating class
        class_to_access = getting_the_world_map(False)
        
        #This gets the continents. We have already unit tested this method so i can now use it to change the dummy data country to continent
        continents_series = pd.Series([ac.converting_country_to_continent(country[0]) for country in getting_the_proxy_file()[1:]])
        
        #Getting the unemployment rate
        unemployment_rates_series = pd.Series([row[3] for row in getting_the_proxy_file()[1:]])
        
        unemployment_dict = class_to_access.manipulating_the_data(continents_series, unemployment_rates_series)
                            
        #Checking the values are the expected values
        self.assertEqual(unemployment_dict, test_average_continents())

#Requirement 4: Checking the files 
class Test_file(test.TestCase):
    
    def setUp(self):
        # Common setup for each test method in this class
        self.country, self.unemployment, self.continents, self.data = getting_the_data_from_assessment_code_file()
    
    #This checks the data is correct datatype    
    def test_file_type(self):
        self.assertEqual(type(self.data), pd.DataFrame)
        self.assertEqual(type(self.continents), pd.Series)
        self.assertEqual(type(self.unemployment), pd.Series)
        self.assertEqual(type(self.country), pd.Series)

    #This checks that the files opened are the correct one
    def test_correct_folder(self):
        expected_df = pd.read_csv("Global_Education.csv", encoding='ISO-8859-1')

        # Check if both DataFrames have the same columns in the same order
        self.assertListEqual(list(self.data.columns), list(expected_df.columns))

        #Check if the values are the same (and ignore the index)
        self.assertTrue(self.data.equals(expected_df))

        
        
if __name__ == '__main__':
    #Checking the continent
    test.main()
