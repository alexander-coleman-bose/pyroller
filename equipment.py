# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 23:33:40 2016

@author: lordmailman
"""

class equipment:
    def __init__(self):
        self.name = []
        self.type = [] # Weapon, 
        self.cost = [] # GP
        self.weight = [] # in lbs
        
        self.attuned = [] # -1, 0, 1 = not attunable, unattuned, attuned
        
        self.action = []
        
    class weapon:
        def __init__(self):
            self.type = 'weapon'
            
            self.melee = [] # bool       
            
            self.ammunition = [] # object
            self.finesse = [] # bool
            self.heavy = [] # bool
            self.light = [] # bool
            self.loading = [] # bool
            self.ranged = [] # range
            self.reach = [] # range
            self.thrown = [] # range
            self.twohanded = [] # bool
            self.versatile = [] # damage die?
            
            self.special = []
            
            
            
        