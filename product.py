# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:49:13 2023

@author: bozzi
"""

import itertools

class Product:
    def init(self,who,mass,op_seq,due_date, prod_type):
        self.who = itertools.count().next
        self.mass = mass
        self.op_seq = op_seq
        self.due_date = due_date
        self.prod_type = prod_type
    
    ### GETTERS
    def get_who(self):
        return self.who
    
    def get_mass(self):
        return self.mass
    
    def get_op_seq(self):
        return self.op_seq
    
    def get_due_date(self):
        return self.due_date
    
    def get_prod_type(self):
        return self.prod_type
    
    ### SETTERS
    def set_mass(self, mass):
        self.mass = mass
    
    def set_op_seq(self, op_seq):
        self.op_seq = op_seq
        
    def set_due_date(self, due_date):
        self.due_date = due_date
    
    def set_prod_type(self,prod_type):
        self.prod_type = prod_type
        