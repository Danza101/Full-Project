import random 
import unittest as test
from assessment_code import *

def test_data_function(data, data_checker):
    for _ in range(20):
        random_index = random.randrange(1, 25)
        if not data.iloc[random_index].equals(data_checker.iloc[random_index]):
            return False
    return True

    
#This will be used to import the moduels from assessment code file
#It tries to downloads all the imports from the assessment_code file and if it isnt able it retuens the error
def modulesInstalled():
    try:
        from assessment_code import pd
        from assessment_code import plt
        from assessment_code import np
        return(True)
    except ImportError:
        return(False)
    
    
# Requirements 1: Testing I have imported the correct imports to this file
class Test_Imports(test.TestCase):
    
    def test_data_import(self):
        data_checker = pd.read_csv("Global_Education.csv", encoding='ISO-8859-1')
        self.assertEqual(test_data_function(data , data_checker) , True)
        
    def test_modules_imports(self):
        #This code tests that pandas, matplotlib and numpy has been downloaded properlly
        self.assertEqual(True , modulesInstalled())

if __name__ == '__main__':
    test.main()
