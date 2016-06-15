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
        
        self.buyPointsBase = 27
        self.buyPointsRem = 27
        
        self.strm = int(floor((self.str - 10)/2))
        self.dexm = int(floor((self.dex - 10)/2))
        self.conm = int(floor((self.con - 10)/2))
        self.intm = int(floor((self.int - 10)/2))
        self.wism = int(floor((self.wis - 10)/2))
        self.cham = int(floor((self.cha - 10)/2))
        
    def assignStats(self,vstr,vdex,vcon,vint,vwis,vcha):
        stats = [vstr,vdex,vcon,vint,vwis,vcha]
        cost = 0
        
        # check to make sure that you input the right number of stats
#        if len(stats) != 6:
#            raise RuntimeError("You must input 6 stats to assignStats")
        for stat in stats:
#            if stat > 15:
#                raise RuntimeError("You cannot assign a stat to higher than 15")
#            elif stat > 13:
#                cost = cost + 2*(stat-13) + 5
#            else:
#                cost = cost + stat - 8
            if stat > 13:
                cost = cost + 2*(stat-13) + 5
                if stat > 15:
                    print 'var too high'
            else:
                cost = cost + stat - 8
            
        if (self.buyPointsBase - cost) < 0:
            raise RuntimeError("You don't have enough base buy points to make this stats change")
        else: #assign the stats
            self.str = stats[0]
            self.dex = stats[1]
            self.con = stats[2]
            self.int = stats[3]
            self.wis = stats[4]
            self.cha = stats[5]
            
            # Calculate modifiers
            self.strm = int(floor((self.str - 10)/2))
            self.dexm = int(floor((self.dex - 10)/2))
            self.conm = int(floor((self.con - 10)/2))
            self.intm = int(floor((self.int - 10)/2))
            self.wism = int(floor((self.wis - 10)/2))
            self.cham = int(floor((self.cha - 10)/2))
            
            # Calculate remaining points
            self.buyPointsRem = self.buyPointsBase - cost
            
        print 'Your stats:'
        print 'Strength:     {:2d} ({:+2d})'.format(self.str,self.strm)
        print 'Dexterity:    {:2d} ({:+2d})'.format(self.dex,self.dexm)
        print 'Constitution: {:2d} ({:+2d})'.format(self.con,self.conm)
        print 'Intelligence: {:2d} ({:+2d})'.format(self.int,self.intm)
        print 'Wisdom:       {:2d} ({:+2d})'.format(self.wis,self.wism)
        print 'Charisma:     {:2d} ({:+2d})'.format(self.cha,self.cham)
        print 'Remaining buy points: {:3d}'.format(self.buyPointsRem)
        
        
        
cTest = character()
print cTest.xp
print("Ideals: ",cTest.ideals)