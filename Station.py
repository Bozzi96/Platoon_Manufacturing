# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:41:32 2023

@author: bozzi
"""

class Station:
	def __init__(self,who,x,y,station_id,state, completion, curr_vehicle,reserved_vehicle):
		self.who = who
		self.x = x
		self.y = y
		self.station_id = station_id
		self.state = state
		self.completion = completion
		self.curr_vehicle = curr_vehicle
		self.reserved_vehicle = reserved_vehicle
	
	### GETTERS	
	def get_who(self):
		return self.who
	
	def get_x(self):
		return self.x
	
	def get_y(self):
	   return self.y

	def get_pos(self):
		return self.x, self.y
	   
	def get_station_id(self):
		return self.station_id

	def get_state(self):
		return self.state

	def get_completion(self):
		return self.completion

	def get_curr_vehicle(self):
		return self.curr_vehicle
	
	def get_reserved_vehicle(self):
		return self.reserved_vehicle
	
	### SETTERS 
	def set_state(self, state):
		self.state = state
	
	def set_completion(self, completion):
		self.completion = completion
	
	def set_curr_vehicle(self, curr_vehicle):
		self.curr_vehicle = curr_vehicle

	def set_reserved_vehicle(self, reserved_vehicle):
		self.reserved_vehicle= reserved_vehicle
		