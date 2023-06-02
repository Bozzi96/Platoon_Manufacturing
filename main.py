# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:18:30 2023

@author: bozzi

Main file, needed to make Netlogo interact with Python and perform the necessary step to plan trajectories, schedule AGVs and 
"""



### SETUP Netlogo
import NetlogoCommunicationModule as ncm
from AGV import AGV,distance_between_agvs
from Product import Product
from Machine import Machine
model_path = r'Platoon.nlogo'
ncm.netlogo.load_model(model_path)
ncm.netlogo.command('A-Setup')


### SETUP of static objects and parameters (no. AGVs, machines position, etc...)
N = int(ncm.netlogo.report("count vehicles")) # no. of AGVs
P = int(ncm.netlogo.report("count products")) # no. of products
M = int(ncm.netlogo.report("count machines")) #no. of machines
S = int(ncm.netlogo.report("count recharge-stations")) #no. of recharging stations

# Get machines position
machines_info = ncm.log_mach_initialInfo()
Machines = [] # array that will contain all the Machines object
for i in range(0,M):
	Machines.append(Machine(machines_info[i][0],machines_info[i][1],machines_info[i][2],"Normal","MachineIdle",machines_info[i][3],1000000, 0, 0))

Stations = []
# for i in range(0,S):
# 	Machines.append(Station())
Agvs = []
	############
	# Problem in retrieving values from netlogo: if I have int and string it is not possible to get them all at once
	# Maybe we need to find a proper structure to store the values? netlogo.report for each attribute would be computationally heavy
	###########

#TODO: Get recharging stations position


### LOOP: Evolution of the system overtime
for tick in range(1,100):
	ncm.netlogo.command('B-Go')
	
print("END OF MAIN")