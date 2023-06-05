# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:43:40 2023

@author: bozzi
"""

### SETUP of Netlogo
import pyNetLogo
global netlogo
netlogo = pyNetLogo.NetLogoLink(gui=True) #Show NetLogo GUI


### VEHICLE attributes
def log_veh_x(who):
	return netlogo.report("[xcor] of vehicle " + str(who))
	
def log_veh_y(who):
	return netlogo.report("[ycor] of vehicle " + str(who))

def log_veh_pos(who):
	return netlogo.report("[(list xcor ycor)] of vehicle " + str(who))
	
def log_veh_type(who):
	return netlogo.report("[vehicletype] of vehicle " + str(who))

def log_veh_state(who):
	return netlogo.report("[vehiclestate] of vehicle " + str(who))

def log_veh_prod(who):
	#returns the number of the product, or "None" if no product on top
	return netlogo.report("[vehiclewithproduct] of vehicle " + str(who))

def log_battery(who):
	#Type of battery: T1=21, T2=42, T3=63
	return netlogo.report("[vehiclebattery] of vehicle " + str(who))

def log_veh_destinationnode(who):
	return netlogo.report("[vehicledestinationnode] of vehicle " + str(who))

def log_veh_destinationentity(who):
	return netlogo.report("[vehicledestinationentity] of vehicle " + str(who))

def log_veh_speedx(who):
	return netlogo.report("[vehiclespeed-x] of vehicle " + str(who))

def log_veh_speedy(who):
	return netlogo.report("[vehiclespeed-y] of vehicle " + str(who))

def log_veh_speedtot(who):
	return netlogo.report("[vehiclespeed-total] of vehicle " + str(who))

def log_batterycharge(who):
	#Charge of battery (State of Charge, SoC)
	return netlogo.report("[vehiclebatterycharge] of vehicle " + str(who))



### PRODUCT attributes
def log_prod_x(who):
	return netlogo.report("[xcor] of product " + str(who))

def log_prod_y(who):
	return netlogo.report("[ycor] of product " + str(who))

def log_prod_pos(who):
	return netlogo.report("[(list xcor ycor)] of product " + str(who))

def log_prod_type(who):
	return netlogo.report("[producttype] of product " + str(who))

def log_weight(who):
	return netlogo.report("[productweight] of product " + str(who))

def log_prod_state(who):
	return netlogo.report("[productstate] of product " + str(who))

def log_prod_operations(who):
	return netlogo.report("[productoperations] of product " + str(who))

def log_prod_releaseorder(who):
	return netlogo.report("[productreleaseorder] of product " + str(who))

def log_prod_duedate(who):
	return netlogo.report("[productduedate] of product " + str(who))

def log_prod_currentop(who):
	return netlogo.report("[productcurrentoperation] of product " + str(who))

def log_prod_nextop(who):
	return netlogo.report("[productnextoperation] of product " + str(who))

def log_prod_startop(who):
	return netlogo.report("[productstartoperation] of product " + str(who))

def log_prod_completionop(who):
	return netlogo.report("[productcompletionoperation] of product " + str(who))

def log_prod_in_veh(who):
	return netlogo.report("[productinvehicle] of product " + str(who))

def log_prod_in_mach(who):
	return netlogo.report("[productinmachine] of product " + str(who))



### MACHINES interaction
def log_mach_pos(who):
	return netlogo.report("[(list xcor ycor)] of machine " + str(who))
def log_mach_initialInfo():
	 return netlogo.report("[(list who xcor ycor item 0 machineoperprocessingtime)] of machines ")
def log_station_initialInfo():
	return netlogo.report("[(list who xcor ycor)] of recharge-stations")
	

# All info on vehicles
def log_veh_info():
	info = netlogo.report("[(list who xcor ycor vehiclebattery)] of vehicles")
	#who, xcor, ycor, battery = info[:,0], info[:,1], info[:,2], info[:,3]
	#return who, xcor, ycor, battery
	return info
def log_prod_info():
	#TODO: Find a way to store also product operations, cannot be done separately because the order is not the same
	# for the moment, cannot be done at the same time because there is no way to handle at the same time integers 
	# and array of strings that are returned from "netlogo.report"
	info = netlogo.report("[(list who xcor ycor productreleaseorder productweight productduedate)] of products")
	#info2 = netlogo.report("[productoperations] of products")
	return info#, info2

# Position of all vehicles
def log_veh_everyPos():
	return netlogo.report("[(list xcor ycor who)] of vehicles")
# Position of all products
def log_prod_everyPos():
	return netlogo.report("[(list xcor ycor who)] of products")