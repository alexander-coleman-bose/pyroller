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

        self.race = []
        self.subrace = []
        self.background = []

        self.faction = []
        self.factionRank = 0
        self.factionRenown = 0

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

#        self.bStr = 8
#        self.bDex = 8
#        self.bCon = 8
#        self.bInt = 8
#        self.bWis = 8
#        self.bCha = 8

#        self.str = self.bStr
#        self.dex = self.bDex
#        self.con = self.bCon
#        self.int = self.bInt
#        self.wis = self.bWis
#        self.cha = self.bCha

        self.statBase = {'str':8,'dex':8,'con':8,'int':8,'wis':8,'cha':8}
        self.statRolled = self.statBase
        self.statRacialBonus = {'str':0,'dex':0,'con':0,'int':0,'wis':0,'cha':0}
        self.stat = self.statBase
        self.statMod = {'str':-1,'dex':-1,'con':-1,'int':-1,'wis':-1,'cha':-1}

        self.buyPointsBase = 27
        self.buyPointsRem = 27

#        self.strm = int(floor((self.str - 10)/2))
#        self.dexm = int(floor((self.dex - 10)/2))
#        self.conm = int(floor((self.con - 10)/2))
#        self.intm = int(floor((self.int - 10)/2))
#        self.wism = int(floor((self.wis - 10)/2))
#        self.cham = int(floor((self.cha - 10)/2))

#        self.dic = {}
        

    def abilityScore(self,ability,newScore = None):
        if newScore == None:
            return self.stat[ability]
        else:
            adjScore = newScore - self.statRacialBonus[ability]
            cost = 0
            
            # if rolled or point buy...
            
            if adjScore < 8:
                raise RuntimeError("Stat cannot be lowered any further than 8 plus racial bonus.")
            elif adjScore > 15:
                raise RuntimeError("Stat cannot be raised any higher than 15 plus racial bonus.")
            elif adjScore > 13:
                cost = cost + 2*(adjScore-13) + 5
            else:
                cost = cost + adjScore - 8
                
            if (self.buyPointsRem - cost) < 0:
                raise RuntimeError("You don't have enough ability score buy points to make this stats change")
            else:
                self.buyPointsRem = self.buyPointsRem - cost
                
            self.stat[ability] = newScore
            self.statMod[ability] = int(floor( (self.stat[ability]-10)/2 ))
                
        print 'Your stats:'
        print 'Strength:     {:2d} ({:+2d})'.format(self.str,self.strm)
        print 'Dexterity:    {:2d} ({:+2d})'.format(self.dex,self.dexm)
        print 'Constitution: {:2d} ({:+2d})'.format(self.con,self.conm)
        print 'Intelligence: {:2d} ({:+2d})'.format(self.int,self.intm)
        print 'Wisdom:       {:2d} ({:+2d})'.format(self.wis,self.wism)
        print 'Charisma:     {:2d} ({:+2d})'.format(self.cha,self.cham)
        print 'Remaining buy points: {:3d}'.format(self.buyPointsRem)


#cTest = character()
#print cTest.xp
#print("Ideals: ",cTest.ideals)
