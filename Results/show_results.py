# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:04:06 2023

@author: bozzi
"""

import pandas as pd
import matplotlib.pyplot as plt

#%% Retrieve data from files
file1= 'results_1.xlsx'
file2= 'results_2.xlsx'
file3= 'results_3.xlsx'

# Read the Excel file into a Pandas DataFrame
df1 = pd.read_excel(file1, header=None)
df2 = pd.read_excel(file2, header=None)
df3 = pd.read_excel(file3, header=None)

# Makespan 1 - Average Speeds 2-->11 - Average Speeds with Payload 12-->21 -  Average Speeds without Payload 22--> 31 ....
# Energy Consumption 32-->41 - Rate of Speed 42-->51 - Number of recharged vehicles 52 - Average Battery when Recharging 53

#%% Plot results
### Makespan
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.boxplot([df1[0],df2[0], df3[0]])
plt.title('Makespan')
plt.xlabel('Scenario')
plt.ylabel("Time [s]")
plt.xticks([1,2,3], ['Scenario 1', 'Scenario 2', 'Scenario 3'])
plt.show()

### Average speed
# Specify the range of columns
columns_avgSpeed = range(1, 11)

# Create a figure to hold the plot
plt.figure(figsize=(12, 6))

# Iterate through the rows and accumulate data
for index, row in df1.iterrows():
    plt.scatter(columns_avgSpeed, row[columns_avgSpeed], label=f'AGV {index + 1}', marker='o')
# Customize the plot
plt.title('Average speed')
plt.xlabel('Simulations')
plt.ylabel('Speed [m/s]')
plt.xticks(columns_avgSpeed)
plt.legend()

plt.show()

### Energy consumption
#%% Specify the range of columns
columns_energy = range(31, 41)

# Create a figure to hold the plot
plt.figure(figsize=(12, 6))

# Iterate through the rows and accumulate data
for index, row in df1.iterrows():
    plt.plot(columns_energy, row[columns_energy], label=f'AGV {index + 1}', marker='o')
# Customize the plot
plt.title('Battery consumption')
plt.xlabel('Simulations')
plt.ylabel('Battery consumption [Ah]')
plt.xticks(columns_energy)
plt.legend()

plt.show()


### Average battery when recharging
#%%
plt.figure(figsize=(8, 6))
plt.scatter(df1[51], df1[52], label='Scenario 1')
plt.scatter(df2[51], df2[52], label='Scenario 2')
plt.scatter(df3[51], df3[52], label='Scenario 3')
plt.title('Average battery when recharging')
plt.xlabel('AGVs recharged')
plt.ylabel('Battery when recharging [%]')
plt.xticks([5,6,7,8])
plt.grid(True)
plt.legend()
plt.show()