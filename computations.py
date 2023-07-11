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
	   x=250
	   y=60
		
	return x,y