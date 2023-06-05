# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:05:57 2023

@author: bozzi
"""

import numpy as np


class AGV:
    def __init__(self, who, x, y, v_x, v_y, heading, battery, vehicle_type, pos_platoon):
        self.who = who
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.heading = heading
        self.battery = battery
        self.vehicle_type = vehicle_type
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
    
    def set_pos_platoon(self,pos_platoon):
        self.pos_platoon = pos_platoon
    
# Useful methods
def distance_between_agvs(agv1: AGV, agv2: AGV):
    return np.linalg.norm(agv1.get_pos - agv2.get_pos)