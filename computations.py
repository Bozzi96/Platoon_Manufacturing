# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:23:02 2023
File to store all functions needed to avoid replication of code
@author: bozzi
"""

import constant as const

def get_target_position(entity,node, machines):
	x=0
	y=0
	if entity == const.DEST_MACHINE:
		target_machine = next((machine for machine in machines if machine.machine_id == node), None)

		# Retrieve the x and y values if the target_machine is found
		if target_machine is not None:
			   x = target_machine.x
			   y = target_machine.y
	elif entity == const.DEST_CHARGINGSTATION:
		target_station = next((station for station in machines if (station.station_id) == node), None)
		x = target_station.x
		y = target_station.y
	else: # Going to unloading station		
		x = 34
		y = 50
	return x,y

def solve_conflicts(id1, id2, AGVs, Products):
	"""
	 Solves conflicts between two AGVs when they get too close each other.

    Parameters:
        id1 (int): The ID of the first AGV involved in the conflict.
        id2 (int): The ID of the second AGV involved in the conflict.
        AGVs (list): A list of AGV objects containing information about each AGV.
        Products (list): A list of Product objects containing information about each product.

    Returns:
        int: The ID of the AGV that should be stopped (agv_to_stop).
        int: The ID of the AGV that should be prioritized (agv_to_prioritize).

    Notes:
        - This function helps to determine which AGV should be prioritized in case of a conflict
          between two AGVs that have conflicting due dates for the products they are carrying.
        - If either of the AGVs is not associated with any product (len(prod1) or len(prod2) is 0),
          it means the AGV is not carrying any product, and in such cases, the AGVs are returned in the order given.
        - The priority is determined based on the due date and release order of the products.
          The AGV carrying the product with an earlier due date or lower release order is prioritized.
        - If both AGVs have the same due date and release order for their respective products,
          the second AGV (id2) is prioritized over the first AGV (id1).
	"""
	# Retrieve AGVs involved in the conflict
	agv1 = [agv for agv in AGVs if agv.vehicle_id == id1]
	agv2 = [agv for agv in AGVs if agv.vehicle_id == id2]
	# Retrieve the corresponding product
	prod1 = [prod for prod in Products if agv1[0].product == prod.who]
	prod2 = [prod for prod in Products if agv2[0].product == prod.who]
	if len(prod1) == 0:
		return id1, id2
	if len(prod2) == 0:
		return id2, id1
	if prod1[0].due_date > prod2[0].due_date:
		return id1, id2
	elif prod1[0].due_date < prod2[0].due_date:
		return id2, id1
	else:
		if prod1[0].release_order	 > prod2[0].release_order:
			return id1, id2
		else:
			return id2, id1
		
import random
def find_free_recharging_station(Stations, vehicles_charged):
	# Choose recharging station with "round robin" policy
	chosen_station = vehicles_charged % len(Stations)
	if chosen_station == 0:
		chosen_station = random.randint(1,5) # Last recharging station
	return chosen_station
# 	for station in Stations:
# 		if station.state == const.RECH_IDLE:
# 			return station.station_id
# 	# No stations is free, find the one that finishes first
# 	first_available = min(Stations, key=lambda station: station.completion)
# 	return first_available