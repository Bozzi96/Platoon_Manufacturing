# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 14:49:32 2023

@author: bozzi
"""

class Machine:
	def __init__(self, who, x, y, machine_type, state, processing, completion, curr_vehicle, curr_product):
		self.who = who
		self. x = x
		self.y = y
		self.machine_type = machine_type
		self.state = state
		self.processing = processing
		self.completion = completion
		self.curr_vehicle = curr_vehicle
		self.curr_product = curr_product
  ### GETTERS        
	def get_who(self):
		   return self.who
    
	def get_x(self):
			return self.x
    
	def get_y(self):
		return self.y
    
	def get_pos(self):
		return self.x, self.y
	
	def get_type(self):
		return self.machine_type
	
	def get_state(self):
		return self.state
	
	def get_processing(self):
		return self.processing
	def get_completion(self):
		return self.completion
	
	### SETTERS
	def set_state(self, state):
		self.state = state
		
	def set_completion(self, completion):
		self.completion = completion
		
	def set_curr_vehicle(self, curr_vehicle):
		self.curr_vehicle = curr_vehicle
	
	def set_curr_product(self, curr_product):
		self.curr_product = curr_product
