# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:18:30 2023

@author: bozzi

Main file, needed to make Netlogo interact with Python and perform the necessary step to plan trajectories, schedule AGVs and 
"""



### SETUP Netlogo
import NetlogoCommunicationModule as ncm
from AGV import AGV,distance_between_agvs, update_AGVs
from Product import Product
from Machine import Machine
from Station import Station
model_path = r'Platoon.nlogo'
ncm.netlogo.load_model(model_path)
ncm.netlogo.command('A-Setup')
ncm.netlogo.repeat_command('B-go', 100)

INF= 100000
##### BEGIN: SETUP of static objects and parameters (no. AGVs, machines position, etc...)
N = int(ncm.netlogo.report("count vehicles")) # no. of AGVs
P = int(ncm.netlogo.report("count products")) # no. of products
M = int(ncm.netlogo.report("count machines")) #no. of machines
S = int(ncm.netlogo.report("count recharge-stations")) #no. of recharging stations

# Get machines information and fill the structure to store data
machines_info = ncm.log_mach_initialInfo()
Machines = []
for i in range(0,M):
	# Machine attributes: who, x, y, machine_id, state, curr_vehicle, curr_prod 
	Machines.append(Machine(machines_info[i][0],machines_info[i][1],machines_info[i][2],machines_info[i][3],0,0,0))
# Get recharging stations information and fill the structure to store data
Stations = []
stations_info = ncm.log_station_initialInfo()
for i in range(0,S):
	# Station attributes: who, x, y, station_id, state, completion, curr_vehicle, reserved_vehicle 
	Stations.append(Station(stations_info[i][0],stations_info[i][1],stations_info[i][2],stations_info[i][3],0,INF,0,0))
# Get AGVs information and fill the structure to store data
AGVs = []
agvs_info = ncm.log_veh_initialInfo()
for i in range(0,N):
	# AGV attributes: who, x, y, vehicle_id,  v_x, v_y, heading, battery, vehicle_type, state, \
	# product, destination_node, destination_entity, pos_platoon
	AGVs.append(AGV(agvs_info[i][0],agvs_info[i][1],agvs_info[i][2],agvs_info[i][3],0,0,0, \
				 100,agvs_info[i][4],0,0,0,0,0))
# Get products information and fill the structure to store data
Products = []
products_info = ncm.log_prod_initialInfo()
for i in range(0,P):
	# Product attributes who, x, y, prod_id, release_order, weight,due_date,op_seq, curr_op, next_op, prod_type, prod_vehicle, prod_machine
	Products.append(Product(products_info[i][0],products_info[i][1], products_info[i][2], \
						 products_info[i][3], products_info[i][4], products_info[i][5], \
						 products_info[i][6],[],0,0,products_info[i][7],0,0))

##### END: SETUP of static objects and parameters (no. AGVs, machines position, etc...)

### LOOP: Evolution of the system overtime
for tick in range(1,100):
	ncm.netlogo.repeat_command('B-Go', 10) # Apply the control each 10 iterations (= 0.5 seconds)
	# Retrieve values from netlogo and update the structures that store data
	agvs_info = ncm.log_veh_info()
	update_AGVs(AGVs,agvs_info)
	# The following is just a test to check if I am able to modify vehicles speed --> OK
	ncm.netlogo.command("ask vehicles with [vehicleid = 1] [ set vehiclespeed-x 0.1 set vehiclespeed-y 1 ]")
	## 0. Retrieve position and destination of each vehicle
	### BEGIN: Control algorithm
	## a) For each AGV that is going to machines:
	## 1a. compute the significant neighborhood (i.e. vehicles under the attraction radius)
	## 2a. Verify if one neighbors is within the safety radius --> if yes perform emergency maneuver
	## 3a. Apply the potential field controller with the given velocity
	## b) For each vehicle that is going to the queue
	## 1b. Verify if it is convenient to go to recharging stations
	## 2b. If it is convenient, change its destination to recharging stations
	## c) For each AGV that is going to recharging stations/unloading unit:
	## 1c. Group them into a platoon
	## 2c. Control them as a platoon
	### END: Control algorithm
	

