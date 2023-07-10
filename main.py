# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:18:30 2023

@author: bozzi

Main file, needed to make Netlogo interact with Python and perform the necessary step to plan trajectories, schedule AGVs and 
"""



### SETUP Netlogo
import NetlogoCommunicationModule as ncm
import constant as const
import numpy as np
from AGV import AGV,distance_between_agvs, update_AGVs, compute_agvs_distances, recharge_decision
from Product import Product
from Machine import Machine
from Station import Station
from potentialField_controller import potential_field_controller,convert_force_to_speed
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
agvs_info = ncm.log_veh_initialInfo() # DATA: [xcor ycor VehicleId VehicleSpeed-X VehicleSpeed-Y ...
												#			VehicleBatteryCharge VehicleState VehicleWithProduct
												#			VehicleDestinationNode VehicleDestinationEntity ]
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
all_obstacles = []
all_obstacles = ncm.log_mach_allpos()
all_obstacles = [all_obstacles, ncm.log_stations_allpos()]
all_obstacles = np.concatenate((all_obstacles[0], all_obstacles[1]), axis=0)
### LOOP: Evolution of the system overtime
safety_radius = 2
count = 0
for tick in range(1,1000):
	ncm.netlogo.repeat_command('B-Go', 10) # Apply the control each 10 iterations (= 0.5 seconds)
	# Retrieve values from netlogo and update the structures that store data
	agvs_info = ncm.log_veh_info()
	update_AGVs(AGVs,agvs_info)
	rech_free = ncm.count_free_station()
	agvs_waiting = ncm.count_AGV_waiting()
	## 0. Retrieve position and destination of each vehicle
	### BEGIN: Control algorithm
	# Consider only the AGVs that are currently moving within the shopfloor
	moving_agvs = [agv for agv in AGVs if agv.state == const.MOVING]
	for agv in moving_agvs:
		if agv.destination_entity == const.DEST_MACHINE:
			#TODO: compute the potential field and the correspondent speed
			target_pos = [104.5, 105.5]
			obstacles = all_obstacles[~np.all(all_obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
			moving_obstacles = [vehicle for vehicle in moving_agvs if vehicle.vehicle_id != agv.vehicle_id]
			potential_force = potential_field_controller(target_pos, [agv.x, agv.y], obstacles, moving_obstacles)
			potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
			ncm.command_speed(agv.vehicle_id, potential_speed[0], potential_speed[1])
			#TODO: compute the safety maneuver if needed
# 			distances = compute_agvs_distances(AGVs)
# 			 # Find indices where distances are less than the threshold
# 			indices = np.where(distances < safety_radius)
# 			if len(indices[0]) == 0:
# 				 conflicts = []
# 			else:	
# 				 # Create a list of tuples representing the indices
# 				conflicts = list(zip(indices[0], indices[1]))
# 				#TODO: Solve conflicts by prioritizing vehicle with closer due date
# 				
		if agv.destination_entity == const.DEST_UNLOADINGSTATION:
			#TODO: plan the recharge decision
			recharging = agv.recharge_decision(rech_free, S, agvs_waiting, M) # TODO: verify if M is the correct choice, or if it is better to take the number of AGV currently in the shopfloor
			if recharging:
				agv.command_destination(agv.id, const.DEST_CHARGINGSTATION) # TODO: add which recharging station is the destination amongst the 5 possible options
		# TODO: if SAME DESTINATION then merge into platoon
		#### PLATOON CONTROL: to be chosen and implemented
	
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
	

