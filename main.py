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
from Station import Station
model_path = r'Platoon.nlogo'
ncm.netlogo.load_model(model_path)
ncm.netlogo.command('A-Setup')


##### BEGIN: SETUP of static objects and parameters (no. AGVs, machines position, etc...)
N = int(ncm.netlogo.report("count vehicles")) # no. of AGVs
P = int(ncm.netlogo.report("count products")) # no. of products
M = int(ncm.netlogo.report("count machines")) #no. of machines
S = int(ncm.netlogo.report("count recharge-stations")) #no. of recharging stations

# Get machines information and fill the structure to store data
machines_info = ncm.log_mach_initialInfo()
Machines = []
for i in range(0,M):
	Machines.append(Machine(machines_info[i][0],machines_info[i][1],machines_info[i][2],"Normal","MachineIdle",machines_info[i][3],1000000, 0, 0))
# Get recharging stations information and fill the structure to store data
Stations = []
stations_info = ncm.log_station_initialInfo()
for i in range(0,S):
	Stations.append(Station(stations_info[i][0],stations_info[i][1],stations_info[i][2],0,"StationIdle",1000000,0,0))
# Get AGVs information and fill the structure to store data
AGVs = []
agvs_info = ncm.log_veh_info()
for i in range(0,N):
	AGVs.append(AGV(agvs_info[i][0],agvs_info[i][1],agvs_info[i][2],0,0,0,agvs_info[i][3],agvs_info[i][3]/21,0,0,0,0))
	############
	# Problem in retrieving values from netlogo: if I have int and string it is not possible to get them all at once
	# Maybe we need to find a proper structure to store the values? netlogo.report for each attribute would be computationally heavy
	###########
# Get products information and fill the structure to store data
Products = []
products_info = ncm.log_prod_info()
for i in range(0,P):
	#TODO: setup product operations (for the moment is marked as 0)
	Products.append(Product(products_info[i][0],products_info[i][1], products_info[i][2], \
						 products_info[i][3], products_info[i][4], products_info[i][5],0,0,0,0))

##### END: SETUP of static objects and parameters (no. AGVs, machines position, etc...)

### LOOP: Evolution of the system overtime
for tick in range(1,100):
	ncm.netlogo.command('B-Go')
	
print("END OF MAIN")