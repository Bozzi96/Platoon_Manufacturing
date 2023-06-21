# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:05:57 2023

@author: bozzi
"""

import numpy as np


class AGV:
    def __init__(self, who, x, y, v_x, v_y, heading, battery, vehicle_type, state, product, destination, pos_platoon):
        self.who = who
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.heading = heading
        self.battery = battery
        self.vehicle_type = vehicle_type
        self.state = state
        self.product = product
        self.destination = destination
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
	
    def get_destination(self):
        return self.destination
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
    
    def set_destination(self,destination):
        self.destination = destination
		
    def set_pos_platoon(self,pos_platoon):
        self.pos_platoon = pos_platoon
    
# Useful methods
def distance_between_agvs(agv1: AGV, agv2: AGV):
    return np.linalg.norm(agv1.get_pos - agv2.get_pos)


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
	Kr = 0.25 # gain for importance of number of free recharging station
	Ka = 0.25 # gain for importance of number of agv waiting in the queue
	Kb = 0.5 # gain for importance of current state of charge of battery
	decision = Kr*rech_free/rech_tot + Ka*AGV_waiting/AGV_tot + (Kb/self.vehicle_type)*(100-self.battery)/100
	if decision > 0.5:
		return True # Go to recharging station
	else:
		return False  # Don't go to recharging station