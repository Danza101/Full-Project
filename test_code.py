import unittest as test
from assessment_code import *

# This method will be used to check if I have the correct table
def check_value(value):
    column_names = ['District code', 'District name', 'Category', 'Student group', '2021-2022 student count - year to date', '2021-2022 attendance rate - year to date', '2020-2021 student count', '2020-2021 attendance rate', '2019-2020 student count', '2019-2020 attendance rate', 'Reporting period', 'Date update']
    return column_names

#This will be used to import the moduels from assessment code file
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
        # This checks that the data I am importing in the coding file is the same as the data I am using in this file
        self.assertEqual(data.columns.tolist(), check_value(0))  
    
    def test_modules_imports(self):
        #This code tests that pandas, matplotlib and numpy has been downloaded properlly
        self.assertEqual(True , modulesInstalled())

if __name__ == '__main__':
    test.main()
