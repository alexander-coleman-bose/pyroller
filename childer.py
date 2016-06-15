# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 12:00:15 2016

@author: lordmailman
"""

from math import *

class character:
    def __init__(self):
        self.name = []
        
        self.xp = 0
        self.level = []
#        self.barbarian = 0
#        self.bard = 0;
#        self.cleric = 0;
#        self.druid = 0;
#        self.fighter = 0;
#        self.monk = 0;
#        self.paladin = 0;
#        self.ranger = 0;
#        self.rogue = 0;
#        self.sorcerer = 0;
#        self.warlock = 0;
#        self.wizard = 0;
        self.race = []
        self.background = []
        
        self.faction = []
        self.factionRank = 0
        
        self.alignment = [] # LG,NG,CG,LN,TN,CN,LE,NE,CE
        self.age = [] # in years
        
        self.height = [] # in inches
        self.weight = [] # in lbs.
        
        self.eyes = []
        self.skin = []
        self.hair = []
        self.appearance = []
        self.personality = []
        self.ideals = []
        self.bonds = []
        self.flaws = []
        self.backstory = []
        
        self.bStr = 8
        self.bDex = 8
        self.bCon = 8
        self.bInt = 8
        self.bWis = 8
        self.bCha = 8
        
        self.str = self.bStr
        self.dex = self.bDex
        self.con = self.bCon
        self.int = self.bInt
        self.wis = self.bWis
        self.cha = self.bCha
        
        self.abPoints = 27
        
        self.strm = math.floor((self.str - 10)/2)
        self.dexm = math.floor((self.dex - 10)/2)
        self.conm = math.floor((self.con - 10)/2)
        self.intm = math.floor((self.int - 10)/2)
        self.wism = math.floor((self.wis - 10)/2)
        self.cham = math.floor((self.cha - 10)/2)
        
cTest = character()
print cTest.xp
print("Ideals: ",cTest.ideals)