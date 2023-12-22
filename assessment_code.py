#These are all the modules i plan on using in the development
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#First i get the data
data = pd.read_csv("Global_Education.csv" , encoding='ISO-8859-1')

#The data is all about school attendance by student group and district from the last couple years
#The sata comes from Data.gov which suggests to me that the data is reliably sourced because it came from a government based website
#From this data the best thing i will be able to study would be how different levels of education affect the likelyhood of getting
#a job depending on the country

# Assuming 'data' is a pandas DataFrame with the correct columns.
country = data["Countries and areas"]  # This should be a Series or list of country names.
unemployment = data["Unemployment_Rate"].astype(float)  # This should be a Series of floats.

plt.bar(country[:10], unemployment[:10])  # Using a bar chart for categorical x-axis data.
plt.xticks(range(len(country[:10])), country[:10], rotation='vertical')
plt.xticks(range(len(country[:10])), country[:10], rotation='vertical')
plt.show()  # To display the plot.
