# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:18:30 2023

@author: bozzi

Main file, needed to make Netlogo interact with Python and perform the necessary step to plan trajectories, schedule AGVs and 
"""



### SETUP Netlogo
import config
import NetlogoCommunicationModule as ncm
from AGV import AGV,distance_between_agvs
from Product import Product
model_path = r'Platoon.nlogo'
config.netlogo.load_model(model_path)
config.netlogo.command('A-Setup')


### SETUP of static objects and parameters (no. AGVs, machines position, etc...)
N = int(config.netlogo.report("count vehicles")) # no. of AGVs
P = int(config.netlogo.report("count products")) # no. of products
M = int(config.netlogo.report("count machines")) #no. of machines

# Get machines position
machines = []
for i in range(0,M):
	machines.append(ncm.log_mach_pos(i+1))

### LOOP: Evolution of the system overtime
for i in range(1,100):
	config.netlogo.command('B-Go')