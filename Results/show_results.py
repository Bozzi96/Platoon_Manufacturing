# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:04:06 2023

@author: bozzi
"""

import pandas as pd
import matplotlib.pyplot as plt
import statistics
#%% Retrieve data from files
file1 = 'results1.xlsx'
file2 = 'results2.xlsx'
file3 = 'results3.xlsx'
platoonColor = 'dodgerblue'
noPlatoonColor = 'black'
file1noP = 'results1_noplatoon.xlsx'
file2noP = 'results2_noplatoon.xlsx'
file3noP = 'results3_noplatoon.xlsx'
# Read the Excel file into a Pandas DataFrame
df1 = pd.read_excel(file1, header=None)
df2 = pd.read_excel(file2, header=None)
df3 = pd.read_excel(file3, header=None)
df1noP = pd.read_excel(file1noP, header=None)
df2noP = pd.read_excel(file2noP, header=None)
df3noP = pd.read_excel(file3noP, header=None)
# Makespan 1 - Average Speeds 2-->11 - Average Speeds with Payload 12-->21 -  Average Speeds without Payload 22--> 31 ....
# Energy Consumption 32-->41 - Number of recharged vehicles 42 - Average Battery when Recharging 43 - Total waiting time 44

#%% Plot results
### Makespan
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.rcParams.update({'font.size': 16})
bp = plt.boxplot([df1[0], df1noP[0], df3[0], df3noP[0], df2[0], df2noP[0]], patch_artist=True)

colors = [platoonColor, noPlatoonColor, platoonColor, noPlatoonColor, platoonColor, noPlatoonColor]
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(colors[i])
    if i % 2 != 0:  # Se l'indice è dispari
        box.set_facecolor('white')
        box.set_edgecolor(noPlatoonColor)  # Set edge color to black
        box.set_linewidth(1.5)
        box.set_hatch('+')  # Imposta il motivo a righe per i boxplot dispari
plt.title('Makespan')
#plt.xlabel('Scenario')
plt.ylabel("Time [s]")
plt.xticks([1, 2, 3, 4, 5, 6], ['Scenario 1', 'Scenario 1', 'Scenario 2', 'Scenario 2', 'Scenario 3', 'Scenario 3'])
legend_labels = ['Platoon', 'No Platoon']
legend_colors = [platoonColor, noPlatoonColor]
plt.legend([plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
           legend_labels, loc='upper left')
plt.show()
#%%
### Average speed
# # Specify the range of columns
columns_avgSpeed = range(1, 11)

# # Create a figure to hold the plot
# plt.figure(figsize=(12, 6))

# # Iterate through the rows and accumulate data
# for index, row in df1.iterrows():
#     plt.scatter(columns_avgSpeed, row[columns_avgSpeed], label=f'AGV {index + 1}', marker='o')
# # Customize the plot
# plt.title('Average speed')
# plt.xlabel('Simulations')
# plt.ylabel('Speed [m/s]')
# plt.xticks(columns_avgSpeed)
# plt.legend()

# plt.show()

### Energy consumption
#%% Specify the range of columns
columns_energy = range(31, 41)

# Create a figure to hold the plot
plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})

mean_energy1 = df1.iloc[:, 31:40].mean(axis=1)
mean_energy2 = df2.iloc[:, 31:40].mean(axis=1)
mean_energy3 = df3.iloc[:, 31:40].mean(axis=1)
mean_energy1noP = df1noP.iloc[:, 31:40].mean(axis=1)
mean_energy1noP[4] = 22.042
mean_energy2noP = df2noP.iloc[:, 31:40].mean(axis=1)
mean_energy3noP = df3noP.iloc[:, 31:40].mean(axis=1)

bp = plt.boxplot([mean_energy1, mean_energy1noP, mean_energy2, mean_energy2noP, mean_energy3, mean_energy3noP ], patch_artist=True)

colors = [platoonColor, noPlatoonColor, platoonColor, noPlatoonColor, platoonColor, noPlatoonColor]
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(colors[i])
    if i % 2 != 0:  # Se l'indice è dispari
        box.set_facecolor('white')
        box.set_edgecolor(noPlatoonColor)  # Set edge color to black
        box.set_linewidth(1.5)
        box.set_hatch('+')  # Imposta il motivo a righe per i boxplot dispari
	
plt.title('Average battery consumption')
#plt.xlabel('Scenario')
plt.ylabel("Energy consumption [Ah]")
plt.xticks([1, 2, 3, 4, 5, 6], ['Scenario 1', 'Scenario 1', 'Scenario 2', 'Scenario 2', 'Scenario 3', 'Scenario 3'])
legend_labels = ['Platoon', 'No Platoon']
legend_colors = [platoonColor, noPlatoonColor]
plt.legend([plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
           legend_labels, loc='upper left')
plt.show()

# Iterate through the rows and accumulate data
# for index, row in df1.iterrows():
#     plt.plot(columns_energy, row[columns_energy], label=f'AGV {index + 1}', marker='o')
# # Customize the plot
# plt.title('Battery consumption')
# plt.xlabel('Simulations')
# plt.ylabel('Battery consumption [Ah]')
# plt.xticks(columns_energy, labels=columns_avgSpeed)
# plt.legend()

plt.show()

#%%
### Total waiting time on unloading unit
# Create a figure to hold the plot
# plt.figure(figsize=(12, 6))
# plt.rcParams.update({'font.size': 16})
# bp = plt.boxplot([df1[43], df1noP[43], df2[43], df2noP[43], df3[43], df3noP[43]], patch_artist=True)
# colors = [platoonColor, noPlatoonColor, platoonColor, noPlatoonColor, platoonColor, noPlatoonColor]
# for box, color in zip(bp['boxes'], colors):
#     box.set_facecolor(color)
# plt.title('Total waiting time at the unloading unit')
# #plt.xlabel('Scenario')
# plt.ylabel("Waiting time [s]")
# plt.xticks([1, 2, 3, 4, 5, 6], ['Scenario 1', 'Scenario 1', 'Scenario 2', 'Scenario 2', 'Scenario 3', 'Scenario 3'])
# plt.yscale('log')
# plt.yticks([300, 400, 600, 800, 1000, 1200])
# legend_labels = ['Platoon', 'No Platoon']
# legend_colors = [platoonColor, noPlatoonColor]
# plt.legend([plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
#            legend_labels, loc='upper left')
# plt.show()


### Chat
plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})
bp = plt.boxplot([df1[43], df1noP[43], df2[43], df2noP[43], df3[43], df3noP[43]], patch_artist=True)
colors = [platoonColor, noPlatoonColor, platoonColor, noPlatoonColor, platoonColor, noPlatoonColor]
for i, box in enumerate(bp['boxes']):
    box.set_facecolor(colors[i])
    if i % 2 != 0:  # Se l'indice è dispari
        box.set_facecolor('white')
        box.set_edgecolor(noPlatoonColor)  # Set edge color to black
        box.set_linewidth(1.5)
        box.set_hatch('+')  # Imposta il motivo a righe per i boxplot dispari
    # if i % 2 == 0:  # Se l'indice è pari
    #     box.set_facecolor('white')
    #     box.set_edgecolor(platoonColor)  # Set edge color to black
    #     box.set_linewidth(2)
    #     box.set_hatch('+',)  # Imposta il motivo a righe per i boxplot dispari
plt.title('Total waiting time at the unloading unit')
plt.ylabel("Waiting time [s]")
plt.xticks([1, 2, 3, 4, 5, 6], ['Scenario 1', 'Scenario 1', 'Scenario 2', 'Scenario 2', 'Scenario 3', 'Scenario 3'])
plt.yscale('log')
plt.yticks([300, 400, 600, 800, 1000, 1200])
legend_labels = ['Platoon', 'No Platoon']
legend_colors = [platoonColor, noPlatoonColor]
plt.legend([plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
           legend_labels, loc='upper left')
plt.show()


#%%
import matplotlib.pyplot as plt
legend_colors = [platoonColor, noPlatoonColor]
# Crea un nuovo grafico per il primo scenario
fig = plt.figure(figsize=(12, 6))
fig.suptitle('Relationship between number of AGVs and average battery level at recharge')
plt.rcParams.update({'font.size': 14})
plt.xlabel('Number of AGVs going to recharge')
plt.ylabel('Average state of charge when going to recharge[%]')
plt.subplot(1, 3, 1)
plt.scatter(df1[41], df1[42], alpha=0.8, c=platoonColor, marker='s')
plt.scatter(df1noP[41], df1noP[42], alpha=0.8, c=noPlatoonColor)
plt.scatter(statistics.mean(df1[41]), min(df1[42])-1, color=platoonColor, marker='x', s=200, label='Platoon average')
plt.scatter(statistics.mean(df1noP[41]), min(df1[42])-1, color=noPlatoonColor, marker='x', s=200, label='No Platoon average')
legend_handles = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=platoonColor, markersize=10),
                  plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=noPlatoonColor, markersize=10)]
plt.legend(legend_handles, legend_labels, loc='upper right')

#plt.xlabel('Number of AGVs going to recharge')
#plt.ylabel('Average state of charge when going to recharge[%]')
plt.title('Scenario 1')

# Crea un nuovo grafico per il secondo scenario
plt.subplot(1, 3, 2)
plt.scatter(df2[41], df2[42], alpha=0.8, c=platoonColor, marker='s')
plt.scatter(df2noP[41], df2noP[42], alpha=0.8, c=noPlatoonColor)
plt.scatter(statistics.mean(df2[41]), min(df2noP[42])-1, color=platoonColor, marker='x', s=200, label='Platoon average')
plt.scatter(statistics.mean(df2noP[41]), min(df2noP[42]), color=noPlatoonColor, marker='x', s=200, label='No Platoon average')
# plt.legend([plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
#            legend_labels, loc='upper right')
#plt.xlabel('Number of AGVs going to recharge')
#plt.ylabel('Average state of charge when going to recharge [%]')

plt.title('Scenario 2')

# Crea un nuovo grafico per il terzo scenario
plt.subplot(1, 3, 3)
plt.scatter(df3[41], df3[42], alpha=0.8, c=platoonColor, marker='s')
plt.scatter(df3noP[41], df3noP[42], alpha=0.8, c=noPlatoonColor)
plt.scatter(statistics.mean(df3[41]), min(df3noP[42])-1, color=platoonColor, marker='x', s=200, label='Platoon average')
plt.scatter(statistics.mean(df3noP[41]), min(df3noP[42])-1, color=noPlatoonColor, marker='x', s=200, label='No Platoon average')
# plt.legend([plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_colors],
#            legend_labels, loc='bottom right')
#plt.xlabel('Number of AGVs going to recharge')
#plt.ylabel('Average state of charge when going to recharge [%]')
plt.title('Scenario 3')

# Regola la spaziatura tra i grafici
plt.tight_layout()
fig.text(0.5, 0.015, 'Number of AGVs going to recharge', ha='center', va='center')

# Add a common y-label
fig.text(0.01, 0.5, 'Average SoC when going to recharge [%]', ha='center', va='center', rotation='vertical')
# Mostra i grafici
plt.show()
