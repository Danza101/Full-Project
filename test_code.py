import random
import pandas as pd
import awoc 
import unittest as test
import assessment_code as ac

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

def getting_the_data_from_assessment_code():
    
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
        self.country, self.unemployment, self.continents, self.data = getting_the_data_from_assessment_code()
        
    #calls method to check the data is good 
    def test_data_import(self):
        data_checker = pd.read_csv("Global_Education.csv", encoding='ISO-8859-1')
        self.assertEqual(test_data_function(data , data_checker) , True)
        
    def test_modules_imports(self):
        #This code tests that pandas, matplotlib and numpy has been downloaded properlly
        self.assertEqual(True , checking_modules_installed())

#Requirements 2: Testing that each country has gone to the correct continent
class TestGraphs(test.TestCase):

    def setUp(self):
        # Common setup for each test method in this class
        self.country, self.unemployment, self.continents, self.data = getting_the_data_from_assessment_code()

    def test_correct_continent(self):
        # When testing, suppress plotting
        data_checker = pd.read_csv("Global_Education.csv", encoding='ISO-8859-1')["Countries and areas"]
        self.assertEqual(True , checking_correct_continent(country , continents , data_checker))
        


if __name__ == '__main__':
    #Getting the requires data i need from my assessment code file
    country , unemployment, continents , data = getting_the_data_from_assessment_code()
    
    #Checking the continent
    test.main()
