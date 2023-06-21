# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 14:49:32 2023

@author: bozzi
"""

class Machine:
	def __init__(self, who, x, y, machine_id, state, curr_vehicle, curr_product):
		self.who = who #ID
		self. x = x #x coordinate
		self.y = y #y coordinate
		self.machine_id = machine_id
#		#self.machine_type = machine_type #machine type (only one type atm)
		self.state = state #machine state: MachineBusy, MachineIdle
# 		self.processing = processing #processing time
# 		self.completion = completion #completion time of the next operation
		self.curr_vehicle = curr_vehicle #vehicle inside the machine
		self.curr_product = curr_product #product inside the machine
  ### GETTERS        
	def get_who(self):
		   return self.who
    
	def get_x(self):
			return self.x
    
	def get_y(self):
		return self.y
    
	def get_pos(self):
		return self.x, self.y
	
	def get_machine_id(self):
		return self.machine_id
		
	def get_state(self):
		return self.state
	
# 	def get_processing(self):
# 		return self.processing
# 	def get_completion(self):
# 		return self.completion
	
	### SETTERS
	def set_state(self, state):
		self.state = state
		
# 	def set_completion(self, completion):
# 		self.completion = completion
		
	def set_curr_vehicle(self, curr_vehicle):
		self.curr_vehicle = curr_vehicle
	
	def set_curr_product(self, curr_product):
		self.curr_product = curr_product
