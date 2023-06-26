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
ncm.netlogo.command('B-go')

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
	# There is the need of having ONLY INTEGERS as values taken from Netlogo
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
	ncm.netlogo.repeat_command('B-Go', 10) # Apply the control each 10 iterations (= 0.5 seconds)
	## 0. Retrieve position and destination of each vehicle
	### BEGIN: Control algorithm
	## a) For each AGV that is going to machines:
	## 1a. compute the significant neighborhood (i.e. vehicles under the attraction radius) --> HOW?? Computationally expensive
	## 2a. Verify if one neighbors is within the safety radius --> if yes perform emergency maneuver
	## 3a. Apply the potential field controller with the given velocity
	## b) For each vehicle that is going to the queue
	## 1b. Verify if it is convenient to go to recharging stations
	## 2b. If it is convenient, change its destination to recharging stations
	## c) For each AGV that is going to recharging stations/unloading unit:
	## 1c. Group them into a platoon
	## 2c. Control them as a platoon (how?) --> That will be difficult
	### END: Control algorithm
	
	
print("END OF MAIN")