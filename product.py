# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:49:13 2023

@author: bozzi
"""

class Product:
    def __init__(self,who, x, y, prod_id, release_order, weight,due_date,op_seq, curr_op, next_op, prod_type, prod_vehicle, prod_machine):
        self.who = who
        self.x = x
        self.y = y
        self.prod_id = prod_id
        self.release_order = release_order
        self.weight = weight
        self.due_date = due_date
        self.op_seq = op_seq
        self.curr_op = curr_op
        self.next_op = next_op
        self.prod_type = prod_type
        self.prod_vehicle = prod_vehicle
        self.prod_machine = prod_machine
    
    ### GETTERS
    def get_who(self):
        return self.who
	
    def get_x(self):
        return self.x 
	
    def get_y(self):
        return self.y
	
    def get_pos(self):
        return self.x, self.y
	
    def get_prod_id(self):
        return self.prod_id
	
    def get_releaseorder(self):
        return self.release_order
	
    def get_weight(self):
        return self.weight
	
    def get_op_seq(self):
        return self.op_seq
    
    def get_due_date(self):
        return self.due_date
    
    def get_prod_type(self):
        return self.prod_type
	
    def get_prod_vehicle(self):
        return self.prod_vehicle
    
    ### SETTERS
    def set_x(self,x):
        self.x = x
        
    def set_y(self,y):
        self.y = y
        
    def set_pos(self,x,y):
        self.x = x
        self.y = y
		
    def set_weight(self, weight):
        self.weight = weight
    
    def set_op_seq(self, op_seq):
        self.op_seq = op_seq
        
    def set_due_date(self, due_date):
        self.due_date = due_date
    
    def set_prod_type(self,prod_type):
        self.prod_type = prod_type

    def set_prod_vehicle(self,vehicle):
        self.prod_vehicle = prod_vehicle