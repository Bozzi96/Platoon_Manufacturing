# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:05:57 2023

@author: bozzi
"""

import numpy as np
from scipy.spatial.distance import cdist


class AGV:
    def __init__(self, who, x, y, vehicle_id, v_x, v_y, heading, battery, vehicle_type, state, product, destination_node, destination_entity, pos_platoon):
        self.who = who
        self.x = x
        self.y = y
        self.vehicle_id = vehicle_id
        self.v_x = v_x
        self.v_y = v_y
        self.heading = heading
        self.battery = battery
        self.vehicle_type = vehicle_type
        self.state = state
        self.product = product
        self.destination_node = destination_node
        self.destination_entity = destination_entity
        self.pos_platoon = pos_platoon
    
    ### GETTERS        
    def get_who(self):
        return self.who
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_pos(self):
        return self.x, self.y

    def get_vehicle_id(self):
        return self.vehicle_id
        
    def get_v_x(self):
        return self.v_x
    
    def get_v_y(self):
        return self.v_y
    
    def get_battery(self):
        return self.battery
    
    def get_vehicletype(self):
        return self.vehicle_type
	
    def get_state(self):
        return self.state
	
    def get_product(self):
        return self.product
	
    def get_destination_node(self):
        return self.destination_node
	
    def get_destination_entity(self):
        return self.destination_entity
	
    def get_pos_platoon(self):
        return self.pos_platoon
	
	
    ### SETTERS
    def set_x(self,x):
        self.x = x
        
    def set_y(self,y):
        self.y = y
        
    def set_pos(self,x,y):
        self.x = x
        self.y = y
    
    def set_v_x(self,v_x):
        self.v_x = v_x
    
    def set_v_y(self,v_y):
        self.v_y = v_y
                
    def set_battery(self,battery):
        self.battery = battery
		
    def set_state(self,state):
        self.state = state
    
    def set_product(self,product):
        self.product = product
    
    def set_destination_node(self,destination_node):
        self.destination_node = destination_node
		
    def set_destination_entity(self,destination_entity):
        self.destination_entity = destination_entity
		
    def set_pos_platoon(self,pos_platoon):
        self.pos_platoon = pos_platoon
    
def distance_between_agvs(agv1: AGV, agv2: AGV) -> float:
    """
    Calculate the Euclidean distance between two AGVs (Automated Guided Vehicles).

    Args:
        agv1 (AGV): The first AGV object.
        agv2 (AGV): The second AGV object.

    Returns:
        float: The Euclidean distance between the positions of the two AGVs.

    Example:
        agv1 = AGV()
        agv1.set_pos(1, 2, 3)
        agv2 = AGV()
        agv2.set_pos(4, 5, 6)
        distance = distance_between_agvs(agv1, agv2)
        # distance is approximately 5.1962
    """
    return np.linalg.norm(agv1.get_pos() - agv2.get_pos())

HIGH_CHARGE = 80
LOW_CHARGE = 20
def recharge_decision(self, rech_free, rech_tot, AGV_waiting, AGV_tot):
	"""
	Function to decide whether it is convenient or not to go to a recharging station

	Parameters
	----------
	rech_free : Integer
		Number of free recharging station
	rech_tot : Integer
		Number of total recharging station
	AGV_waiting : Integer
		Number of AGVs waiting in the queue
	AGV_tot : Integer
		Number of total AGVs in the system

	Returns
	-------
	Boolean
		True: go to recharging station
		False: don't go to recharging station

	"""
	if self.battery > HIGH_CHARGE:
		return False
	if self.battery < LOW_CHARGE:
		return True
	Kr = 0.25 # gain for importance of number of free recharging station
	Ka = 0.25 # gain for importance of number of agv waiting in the queue
	Kb = 0.5 # gain for importance of current state of charge of battery
	decision = Kr*rech_free/rech_tot + Ka*AGV_waiting/AGV_tot + (Kb/self.vehicle_type)*(100-self.battery)/100
	if decision > 0.5:
		return True # Go to recharging station
	else:
		return False  # Don't go to recharging station
	
def compute_agvs_distances(agvs):
    """
    Compute pairwise distances between AGVs.

    Args:
        agvs (list): List of AGVs

    Returns:
        np.ndarray: 2D array containing pairwise distances between AGVs.
            distances[i, j] contains the distance between agvs[i] and agvs[j].
    """

    # Extract the (x, y) coordinates from AGV objects
    points = np.array([(float(agv.x), float(agv.y)) for agv in agvs], dtype=[('x', float), ('y', float)])

    # Compute pairwise distances
    distances = cdist(points, points)
	 # TODO: verify if it it sufficient or if it is needed to add identifiers of AGVs
    return distances


def update_AGVs(AGVs, agvs_info):
	for info in agvs_info:
		vehicle_id= info[2]
		# Find the AGV object with the corresponding index
		agv = next((agv for agv in AGVs if agv.vehicle_id == vehicle_id), None)
    
	# Update the x and y coordinates of the AGV object
	if agv is not None:
		agv.x = info[0]
		agv.y = info[1]
		agv.battery = info[5]
		agv.state = info[6]
		agv.product = info[7]
		agv.destination_node = info[8]
		agv.destination_entity = info[9]