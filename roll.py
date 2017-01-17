# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:28:14 2017

@author: lordmailman
"""

from math import floor
from random import randint

#def roll(varargin)
def roll(numD = 1,typeD = 20,modD = 0,keepLow = 0,keepHigh = 0,rerollD = 0):
    if numD<0:
        raise RuntimeError("You must roll a positive number of dice.")
    elif keepLow>0 and keepHigh>0:
        raise RuntimeError("You can keep the lowest or the highest rolls, not both.")
    elif keepLow<0 or keepLow>=numD:
        raise RuntimeError("You must keep a positive number of dice, but no more than you roll.")
    elif keepHigh<0 or keepHigh>=numD:
        raise RuntimeError("You must keep a positive number of dice, but no more than you roll.")
    elif rerollD<0 or rerollD>typeD:
        raise RuntimeError("You cannot reroll numbers higher than the die has.")
        
    rolls = list()
    
    for ind in range(nDice):
        tmp = randint(1,typeD)
        if tmp == rerollD:
            tmp = randint(1,typeD)
        tmp = tmp + modD
        
        rolls.append(tmp)
    
    if keepLow>0:
        for ind in range(numD-keepLow):
            rolls.pop(rolls.index(max(rolls)))
            
    if keepHigh>0:
        for ind in range(numD-keepHigh):
            rolls.pop(rolls.index(min(rolls)))
            
    return sum(rolls)
    