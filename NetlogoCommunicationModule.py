# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:43:40 2023

@author: bozzi
"""

### SETUP of Netlogo
import pyNetLogo
import constant as const
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
	 return netlogo.report("[(list who xcor ycor MachineID)] of machines ")
#	 return netlogo.report("[MachineValues] of machines")
def log_station_initialInfo():
	return netlogo.report("[(list who xcor ycor Rech.StationID)] of recharge-stations")
def log_mach_allpos():
	return netlogo.report("[(list xcor ycor)] of machines")
def log_stations_allpos():
	return netlogo.report("[(list xcor ycor)] of recharge-stations")
	
# All info on vehicles
def log_veh_initialInfo():
	info = netlogo.report("[(list who xcor ycor VehicleID VehicleType)] of vehicles")
	return info

def log_prod_initialInfo():
	productInfo = "[(list who xcor ycor ProductID ProductReleaseOrder ProductWeight ProductDueDate ProductType)] of products"
	info = netlogo.report(productInfo)
	return info

# Position of all vehicles
def log_veh_everyPos():
	return netlogo.report("[(list VehicleId xcor ycor)] of vehicles")
# Position of all products
def log_prod_everyPos():
	return netlogo.report("[(list xcor ycor who)] of products")

### Periodic communication
# Periodic info on vehicles
def log_veh_info():
	instruction = "[(list xcor ycor VehicleId VehicleSpeed-X VehicleSpeed-Y " \
					    "VehicleBatteryCharge VehicleState VehicleWithProduct " \
							"VehicleDestinationNode VehicleDestinationEntity)] of vehicles"
	return netlogo.report(instruction)

# Periodic info on products
def log_prod_info():
	instruction = "[(list ProductId xcor ycor)] of products"
	return netlogo.report(instruction)

# Periodic info on machines
def log_mach_info():
	instruction = "[(list MachineId MachineState MachineWithVehicle " \
		"MachineProcessingProduct )] of machines"
	return netlogo.report(instruction)

#Periodic info on recharging stations
def log_rech_info():
	instruction = "[(list Rech.StationId Rech.State Rech.NextCompletion " \
		"Rech.WithVehicle Rech.ReservedForVehicle )] of recharge-stations"
	return netlogo.report(instruction)

def command_speed(vehicle_id, speed_x, speed_y):
	netlogo.command("ask vehicles with [vehicleid = " + str(vehicle_id) + "] [set vehiclespeed-x " +  str(speed_x) + " set vehiclespeed-y " + str(speed_y) + "]")
		
def count_free_station():
	return netlogo.report("count Recharge-stations with [Rech.state = " + str(const.RECH_IDLE) + "]")
	
def count_AGV_waiting():
	return netlogo.report("count Vehicles with [VehicleState = " + str(const.WAITING_OUTSIDE) + "]")

def command_destination(vehicle_id, destination, node):
	netlogo.command("ask vehicles with [vehicleid = " + str(vehicle_id) + "] [ set VehicleDestinationEntity " + str(destination) + " set VehicleDestinationNode " + str(node) + "]")
	
