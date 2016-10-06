# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 12:00:15 2016

@author: lordmailman
"""

from math import floor
from random import randint

class character:
    def __init__(self):
        self.name = []
        self.portrait = []

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
        self.statRacialBonus = {'str':0,'dex':0,'con':0,'int':0,'wis':0,'cha':0}
        self.stat = self.statBase
        self.statMod = {'str':-1,'dex':-1,'con':-1,'int':-1,'wis':-1,'cha':-1}

        self.pointBuy = True
        self.buyPointsBase = 27
        self.buyPointsRem = 27
        
        self.features = []
        self.attacks = []
        self.spells = []
        
        self.equipment = []
        self.weapons = []
        self.armor = []
        
        self.coins = []

#        self.strm = int(floor((self.str - 10)/2))
#        self.dexm = int(floor((self.dex - 10)/2))
#        self.conm = int(floor((self.con - 10)/2))
#        self.intm = int(floor((self.int - 10)/2))
#        self.wism = int(floor((self.wis - 10)/2))
#        self.cham = int(floor((self.cha - 10)/2))

#        self.dic = {}

        
    def rollStats(self,nDice=4,nDrop=1):
        if nDice<3:
            raise RuntimeError("You must roll at least 3d6.")
        elif nDrop<0 or nDrop>=nDice:
            raise RuntimeError("You must drop a positive number of dice, but no more than you roll.")
        
        self.pointBuy = False
        
        for stat in self.statBase:
            rolls = list()
        
            for ind in range(nDice):
                rolls.append(randint(1,6))
            
            for ind in range(nDrop):
                rolls.pop(rolls.index(min(rolls)))
        
            self.abilityScore(stat,sum(rolls))
        

    def abilityScore(self,ability,newScore = None):
        acceptedNames = ['str','dex','con','int','wis','cha']
        ability = str.lower(ability)
        
        # interpret full names to stat names
        if ability == 'strength':
            ability = 'str'
        elif ability == 'dexterity':
            ability = 'dex'
        elif ability == 'constitution':
            ability = 'con'
        elif ability == 'intelligence':
            ability = 'int'
        elif ability == 'wisdom':
            ability = 'wis'
        elif ability == 'charisma':
            ability = 'cha'
        elif ability not in acceptedNames:
            raise RuntimeError("abilityScore must be called with an ability (str,dex,con,int,wis,cha)")
        
        # if no score is given, get the stat instead
        if newScore == None:
            return self.stat[ability]
        elif self.pointBuy:
            adjScore = floor(newScore) - self.statRacialBonus[ability]
            cost = 0
            
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
        self.statMod[ability] = floor( (self.stat[ability]-10)/2 )
                
        print('Your stats:')
        print('Strength:'.ljust(14),
              repr(self.stat['str']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Dexterity:'.ljust(14),
              repr(self.stat['dex']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Constitution:'.ljust(14),
              repr(self.stat['con']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Intelligence:'.ljust(14),
              repr(self.stat['int']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Wisdom:'.ljust(14),
              repr(self.stat['wis']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Charisma:'.ljust(14),
              repr(self.stat['cha']).rjust(3),
              '({:+d})'.format(self.strm()),sep='')
        print('Remaining buy points:',repr(self.buyPointsRem).rjust(3))
        
        
    def strength(self,newScore = None):
        if newScore == None:
            return self.abilityScore('str')
        else:
            self.abilityScore('str',newScore)
            
    def dexterity(self,newScore = None):
        if newScore == None:
            return self.abilityScore('dex')
        else:
            self.abilityScore('dex',newScore)
        
    def constitution(self,newScore = None):
        if newScore == None:
            return self.abilityScore('con')
        else:
            self.abilityScore('con',newScore)
        
    def intelligence(self,newScore = None):
        if newScore == None:
            return self.abilityScore('int')
        else:
            self.abilityScore('int',newScore)
        
    def wisdom(self,newScore = None):
        if newScore == None:
            return self.abilityScore('wis')
        else:
            self.abilityScore('wis',newScore)
        
    def charisma(self,newScore = None):
        if newScore == None:
            return self.abilityScore('cha')
        else:
            self.abilityScore('cha',newScore)
        
    def strm(self):
        return self.statMod['str']
        
    def dexm(self):
        return self.statMod['dex']
        
    def conm(self):
        return self.statMod['con']
        
    def intm(self):
        return self.statMod['int']
        
    def wism(self):
        return self.statMod['wis']
        
    def cham(self):
        return self.statMod['cha']


#cTest = character()
#print cTest.xp
#print("Ideals: ",cTest.ideals)
