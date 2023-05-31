# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:43:40 2023

@author: bozzi
"""

import config



### VEHICLE attributes
def log_veh_x(who):
	return config.netlogo.report("[xcor] of vehicle " + str(who))
	
def log_veh_y(who):
	return config.netlogo.report("[ycor] of vehicle " + str(who))

def log_veh_pos(who):
	return config.netlogo.report("[(list xcor ycor)] of vehicle " + str(who))
	
def log_veh_type(who):
	return config.netlogo.report("[vehicletype] of vehicle " + str(who))

def log_veh_state(who):
	return config.netlogo.report("[vehiclestate] of vehicle " + str(who))

def log_veh_prod(who):
	#returns the number of the product, or "None" if no product on top
	return config.netlogo.report("[vehiclewithproduct] of vehicle " + str(who))

def log_battery(who):
	#Type of battery: T1=21, T2=42, T3=63
	return config.netlogo.report("[vehiclebattery] of vehicle " + str(who))

def log_veh_destinationnode(who):
	return config.netlogo.report("[vehicledestinationnode] of vehicle " + str(who))

def log_veh_destinationentity(who):
	return config.netlogo.report("[vehicledestinationentity] of vehicle " + str(who))

def log_veh_speedx(who):
	return config.netlogo.report("[vehiclespeed-x] of vehicle " + str(who))

def log_veh_speedy(who):
	return config.netlogo.report("[vehiclespeed-y] of vehicle " + str(who))

def log_veh_speedtot(who):
	return config.netlogo.report("[vehiclespeed-total] of vehicle " + str(who))

def log_batterycharge(who):
	#Charge of battery (State of Charge, SoC)
	return config.netlogo.report("[vehiclebatterycharge] of vehicle " + str(who))



### PRODUCT attributes
def log_prod_x(who):
	return config.netlogo.report("[xcor] of product " + str(who))

def log_prod_y(who):
	return config.netlogo.report("[ycor] of product " + str(who))

def log_prod_pos(who):
	return config.netlogo.report("[(list xcor ycor)] of product " + str(who))

def log_prod_type(who):
	return config.netlogo.report("[producttype] of product " + str(who))

def log_weight(who):
	return config.netlogo.report("[productweight] of product " + str(who))

def log_prod_state(who):
	return config.netlogo.report("[productstate] of product " + str(who))

def log_prod_operations(who):
	return config.netlogo.report("[productoperations] of product " + str(who))

def log_prod_releaseorder(who):
	return config.netlogo.report("[productreleaseorder] of product " + str(who))

def log_prod_duedate(who):
	return config.netlogo.report("[productduedate] of product " + str(who))

def log_prod_currentop(who):
	return config.netlogo.report("[productcurrentoperation] of product " + str(who))

def log_prod_nextop(who):
	return config.netlogo.report("[productnextoperation] of product " + str(who))

def log_prod_startop(who):
	return config.netlogo.report("[productstartoperation] of product " + str(who))

def log_prod_completionop(who):
	return config.netlogo.report("[productcompletionoperation] of product " + str(who))

def log_prod_in_veh(who):
	return config.netlogo.report("[productinvehicle] of product " + str(who))

def log_prod_in_mach(who):
	return config.netlogo.report("[productinmachine] of product " + str(who))



### MACHINES interaction
def log_mach_pos(who):
	return config.netlogo.report("[(list xcor ycor)] of machine " + str(who))