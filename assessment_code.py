#These are all the modules i plan on using in the development
import pandas as pd
import matplotlib as plt
import numpy as np

#First i get the data
data = pd.read_csv("School_Attendance_by_Student_Group_and_District__2021-2022.csv")

#The data is all about school attendance by student group and district from the last couple years
#The sata comes from Data.gov which suggests to me that the data is reliably sourced because it came from a government based website
#The first idea which comes to me is seeing if i could group the data some way depending on the school
