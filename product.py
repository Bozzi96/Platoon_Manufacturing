# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:49:13 2023

@author: bozzi
"""

import itertools

class Product:
    def init(self,mass,op_seq,due_date, ptype):
        self.id = itertools.count().next
        self.mass = mass
        self.op_seq = op_seq
        self.due_date = due_date
        self.ptype = ptype
    
    ### GETTERS
    def get_id(self):
        return self.id
    
    def get_mass(self):
        return self.mass
    
    def get_op_seq(self):
        return self.op_seq
    
    def get_due_date(self):
        return self.due_date
    
    def get_ptype(self):
        return self.ptype
    
    ### SETTERS
    def set_mass(self, mass):
        self.mass = mass
    
    def set_op_seq(self, op_seq):
        self.op_seq = op_seq
        
    def set_due_date(self, due_date):
        self.due_date = due_date
    
    def set_ptype(self,ptype):
        self.ptype = ptype
        