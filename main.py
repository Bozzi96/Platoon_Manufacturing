# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:18:30 2023

@author: bozzi

Main file, needed to make Netlogo interact with Python and to:
	- plan trajectories
	- schedule AGVs recharging
	- form platoons to achieve energy efficient movement to shared resources
"""


### IMPORT
import NetlogoCommunicationModule as ncm
import constant as const
import numpy as np
import math
from AGV import AGV, update_AGVs, compute_agvs_distances, recharge_decision
from Product import Product
from Machine import Machine
from Station import Station
from potentialField_controller import potential_field_controller,convert_force_to_speed
from computations import get_target_position, solve_conflicts, find_free_recharging_station


### SETUP Netlogo
model_path = r'Platoon.nlogo'
ncm.netlogo.load_model(model_path)
ncm.netlogo.command('A-Setup')
ncm.netlogo.repeat_command('B-go', 10) # Make the simulation evolve a bit to retrive reliable data
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
	# product, destination_node, destination_entity, platoon_type, platoon_position
	AGVs.append(AGV(agvs_info[i][0],agvs_info[i][1],agvs_info[i][2],agvs_info[i][3],0,0,0, \
				 100,agvs_info[i][4],0,0,0,0,0,0))
# Get products information and fill the structure to store data
Products = []
products_info = ncm.log_prod_initialInfo()
for i in range(0,P):
	# Product attributes who, x, y, prod_id, release_order, weight,due_date,op_seq, curr_op, next_op, prod_type, prod_vehicle, prod_machine
	Products.append(Product(products_info[i][0],products_info[i][1], products_info[i][2], \
						 products_info[i][3], products_info[i][4], products_info[i][5], \
						 products_info[i][6],[],0,0,products_info[i][7],0,0))

##### END: SETUP of static objects and parameters (no. AGVs, machines position, etc...)
obstacles = [] # Store position of machines and recharging stations to be used in the potential field controller
obstacles = ncm.log_mach_allpos()
obstacles = [obstacles, ncm.log_stations_allpos()]
obstacles = np.concatenate((obstacles[0], obstacles[1]), axis=0)
### LOOP: Evolution of the system overtime
safety_distance = 5
count = 0
for tick in range(1,2000):
	ncm.netlogo.repeat_command('B-Go', 10) # Apply the control each 10 iterations (= 0.5 seconds)
	# Retrieve values from netlogo and update the structures that store data
	agvs_info = ncm.log_veh_info()
	update_AGVs(AGVs,agvs_info)
	rech_free = ncm.count_free_station()
	agvs_waiting = ncm.count_AGV_waiting()
	## 0. Retrieve position and destination of each vehicle
###### BEGIN: Control algorithm
	# Consider only the AGVs that are currently moving within the shopfloor
	moving_agvs = [agv for agv in AGVs if agv.state == const.MOVING]
	for agv in moving_agvs:
		if agv.destination_entity == const.DEST_MACHINE:
			### BEGIN: Potential field control
			target_pos = get_target_position(agv.destination_entity, agv.destination_node, Machines)
			static_obstacles = obstacles[~np.all(obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
			moving_obstacles = [[vehicle.x, vehicle.y] for vehicle in moving_agvs if vehicle.vehicle_id != agv.vehicle_id] # Retrieve position of other AGVs moving within the shopfloor
			potential_force = potential_field_controller(target_pos, [agv.x, agv.y], static_obstacles, moving_obstacles)
			potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
			ncm.command_speed(agv.vehicle_id, potential_speed[0], potential_speed[1], agv.product)
			### END: Potential field control
			### BEGIN: Recharging decision after passing through the unloading unit
		if agv.destination_entity == const.DEST_EXITINGVEHICLE:
			recharging = recharge_decision(agv, rech_free, S, agvs_waiting, M) # TODO: verify if M is the correct choice, or if it is better to take the number of AGV currently in the shopfloor
			if recharging:
				agv.destination_entity = const.DEST_CHARGINGSTATION
				recharge_dest = find_free_recharging_station(Stations)
				agv.destination_node = recharge_dest
				ncm.command_destination(agv.vehicle_id, const.DEST_CHARGINGSTATION, recharge_dest) # Maybe a +/- 11 is needed to "fix" the offset between rech_id and destination node
			### END: Recharging decision
			### BEGIN: Handle AGVs who have different destinations (charging stations, unloading unit)
		if agv.destination_entity == const.DEST_CHARGINGSTATION:
			target_pos = get_target_position(agv.destination_entity, agv.destination_node, Stations)
			static_obstacles = obstacles[~np.all(obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
			moving_obstacles = [[vehicle.x, vehicle.y] for vehicle in moving_agvs if vehicle.vehicle_id != agv.vehicle_id] # Retrieve position of other AGVs moving within the shopfloor
			potential_force = potential_field_controller(target_pos, [agv.x, agv.y], static_obstacles, moving_obstacles)
			potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
			ncm.command_speed(agv.vehicle_id, potential_speed[0], potential_speed[1], agv.product)
			agv.platoon_type = const.PLATOON_CHARGING # add agv to platoon 
		if agv.destination_entity == const.DEST_GETTINGIN: # After recharging AGVs need to go back to the queue
 			#TODO: handle two cases: 1) the gettingIn of AGVs directly after the unloading unit (they don't need control, should be handled by Netlogo) 
										# 2) the AGVs going to the queue after recharging (they need control, implemented in the following 4-5 lines)
 			target_pos = (34.0, 15.0)
 			static_obstacles = obstacles[~np.all(obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
 			moving_obstacles = [[vehicle.x, vehicle.y] for vehicle in moving_agvs if vehicle.vehicle_id != agv.vehicle_id] # Retrieve position of other AGVs moving within the shopfloor
 			potential_force = potential_field_controller(target_pos, [agv.x, agv.y], static_obstacles, moving_obstacles)
 			potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
 			ncm.command_speed(agv.vehicle_id, potential_speed[0], potential_speed[1], agv.product)
		if agv.destination_entity == const.DEST_UNLOADINGSTATION:
			agv.platoon_type = const.PLATOON_UNLOADING # add agv to platoon 
			### END: Handle AGVs who have different destinations (charging stations, unloading unit)
		### BEGIN: Platoon control for AGVs who share destination
	#platoon_charging = [agv for agv in AGVs if agv.platoon_type == const.PLATOON_CHARGING]
	platoon_unloading = [agv for agv in AGVs if agv.platoon_type == const.PLATOON_UNLOADING]
	if platoon_unloading:
		target_pos = (34.0, 50.0)
		distance_from_unloading = [np.sqrt((agv.x - target_pos[0])**2 + (agv.y - target_pos[1])**2) for agv in platoon_unloading] 	# Calculate distance of each AGV from the fixed point
		sorted_indices = np.argsort(distance_from_unloading) # Sort the AGVs based on their distances
		# Assign the position attribute in increasing order based on the sorted indices
		for position, index in enumerate(sorted_indices):
			   platoon_unloading[index].platoon_position = position + 1
		platoon_unloading.sort(key=lambda agv: agv.platoon_position) # Sort platoon based on platoon_position
	   # Compute ideal speed for each element of the platoon
		unloading_processing = 500 # Unloading processing time, to be put at the beginning of the main
		static_obstacles = obstacles[~np.all(obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
		moving_obstacles = [[vehicle.x, vehicle.y] for vehicle in moving_agvs if vehicle.vehicle_id != platoon_unloading[0].vehicle_id] # Retrieve position of other AGVs moving within the shopfloor
		potential_force = potential_field_controller(target_pos, [platoon_unloading[0].x, platoon_unloading[0].y], static_obstacles, moving_obstacles)
		potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
		ncm.command_speed(platoon_unloading[0].vehicle_id, potential_speed[0], potential_speed[1], platoon_unloading[0].product)
		expected_arrival_time = distance_from_unloading[0]/ (math.sqrt(potential_speed[0]**2 + potential_speed[1]**2)) # compute the expected arrival time of the first element of the platoon
		for index, (agv, distance) in enumerate(zip(platoon_unloading[1:], distance_from_unloading[:-1])): # loop over each agv starting from the second, and for each distance except the last one
			# Compute angle and speed_x and speed_y for each agv
			time_from_unloading = expected_arrival_time + unloading_processing # compute the time for the unloading machine to be available
			speed_tot = distance_from_unloading[index]/ time_from_unloading # compute the average speed (assumed constant) needed to arrive at the destination at the precise time
			speed_angle = np.arctan2(agv.y - target_pos[1], agv.x - target_pos[0]) # compute the angle with respect to the unloading machine
			ncm.command_speed(agv.vehicle_id, -speed_tot*np.cos(speed_angle), -speed_tot*np.sin(speed_angle) , agv.product)
			expected_arrival_time = time_from_unloading # update the expected arrival time for the following element of the platoon
			### END: Platoon control for AGVs who share destination
	### BEGIN: Emergency control
	distances = compute_agvs_distances(moving_agvs)
	# Find AGV conflicts based on distances
	conflicts = []
	for agv_ids, distance in distances.items():
	    agv_id1, agv_id2 = agv_ids
	    if distance < safety_distance and agv_id1 != agv_id2:
	        conflicts.append(agv_ids)
	# Solve conflicts
	# TODO: solve conflicts in a smart way, avoiding collision in all possible scenarios
	for conflict in conflicts:
		   agv_id1, agv_id2 = conflict
		   agv_to_stop, agv_to_prioritize = solve_conflicts(agv_id1, agv_id2, AGVs, Products)
		   AGV_stop = next((agv for agv in AGVs if agv.vehicle_id == agv_to_stop), None)
		   AGV_priority = next((agv for agv in AGVs if agv.vehicle_id == agv_to_prioritize), None)
		   ncm.command_speed(agv_to_stop, 0.0001, 0.0001, agv.product) # Stop vehicle; speed = 0 gives error, so put a very low number
		   ## Recompute the potential field controller for the other vehicle
# 		   target_pos = get_target_position(agv.destination_entity, agv.destination_node, Machines)
# 		   static_obstacles = obstacles[~np.all(obstacles == target_pos, axis=1)] # Remove the target from the list of obstacles
# 		   potential_force = potential_field_controller(target_pos, [AGV_stop.x, AGV_stop.y], static_obstacles, [[AGV_priority.x, AGV_priority.y]] )
# 		   potential_speed = convert_force_to_speed(potential_force, mass=5, time_interval=1)
# 		   ncm.command_speed(agv_to_prioritize, potential_speed[0], potential_speed[1], agv.product)
	### END: Emergency control
###### END: Control algorithm

#TODO: Find a way to end the simulation and store results (performance index)
	
