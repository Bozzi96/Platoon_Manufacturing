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
		#TODO: Handle the case where the destination is a charging station
	   x=250
	   y=60
		
	return x,y

def solve_conflicts(id1, id2, AGVs, Products):
	# Retrieve AGVs involved in the conflict
	agv1 = [agv for agv in AGVs if agv.vehicle_id == id1]
	agv2 = [agv for agv in AGVs if agv.vehicle_id == id2]
	# Retrieve the corresponding product
	prod1 = [prod for prod in Products if agv1[0].product == prod.who]
	prod2 = [prod for prod in Products if agv2[0].product == prod.who]
	if len(prod1) == 0:
		return id1
	if len(prod2) == 0:
		return id2
	if prod1[0].due_date > prod2[0].due_date:
		return id1
	elif prod1[0].due_date < prod2[0].due_date:
		return id2
	else:
		if prod1[0].release_order	 > prod2[0].release_order:
			return id1
		else:
			return id2
		
def find_free_recharging_station(Stations):
	for station in Stations:
		if station.state == const.RECH_IDLE:
			return station.station_id
	return 0