# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 09:53:38 2017

@author: finalfrog
"""

#from random import randrange
from roll import roll
from math import floor

heightUnits = 'inches'
weightUnits = 'lbs'

#params = [
#    ("Race",                "Base Height",  "Base Weight",  "Height Modifier",  "Weight Modifier"   ),
#    ("Human",               "4`8``",        110,            "2d10",             "2d4"               ),
#    ("Dwarf (Hill)",        "3`8``",        115,            "2d4",              "2d6"               ),
#    ("Dwarf (Mountain)",    "4`0``",        130,            "2d4",              "2d6"               ),
#    ("Elf (High)",          "4`6``",        90,             "2d10",             "1d4"               ),
#    ("Elf (Wood)",          "4`6``",        100,            "2d10",             "1d4"               ),
#    ("Elf (Drow)",          "4`5``",        75,             "2d6",              "1d6"               ),
#    ("Halfling",            "2`7``",        35,             "2d4",              "1"                 ),
#    ("Dragonborn",          "5`6``",        175,            "2d8",              "2d6"               ),
#    ("Gnome",               "2`11``",       35,             "2d4",              "1"                 ),
#    ("Half-Elf",            "4`9``",        110,            "2d8",              "2d4"               ),
#    ("Half-Orc",            "4`10``",       140,            "2d10",             "2d6"               ),
#    ("Tiefling",            "4`9``",        110,            "2d8",              "2d4"               ),
#    ("Asaimar",             "4`8``",        110,            "2d10",             "2d4"               ),
#    ("Bugbear",             "6`0``",        200,            "2d12",             "2d6"               ),
#    ("Firbolg",             "6`2``",        175,            "2d4",              "2d6"               ),
#    ("Goblin",              "3`5``",        35,             "2d10",             "1"                 ),
#    ("Hobgoblin",           "4`8``",        200,            "2d10",             "2d6"               ),
#    ("Kenku",               "4`4``",        50,             "2d8",              "2d4"               ),
#    ("Kobold",              "2`1``",        25,             "2d4",              "1"                 ),
#    ("Lizardfolk",          "4`9``",        120,            "2d10",             "2d6"               ),
#    ("Orc",                 "5`4``",        175,            "2d8",              "2d6"               ),
#    ("Tabaxi",              "4`10``",       90,             "2d10",             "2d4"               ),
#    ("Triton",              "4`6``",        90,             "2d10",             "2d4"               ),
#    ("Yuan-ti",             "4`8``",        110,            "2d10",             "2d4"               )
#    ]

params = [
    ("Race",                "Base Height",  "Base Weight",  "Height Modifier",  "Weight Modifier"   ),
    ("Human",               56,             110,            "2d10",             "2d4"               ),
    ("Dwarf (Hill)",        44,             115,            "2d4",              "2d6"               ),
    ("Dwarf (Mountain)",    48,             130,            "2d4",              "2d6"               ),
    ("Elf (High)",          54,             90,             "2d10",             "1d4"               ),
    ("Elf (Wood)",          54,             100,            "2d10",             "1d4"               ),
    ("Elf (Drow)",          53,             75,             "2d6",              "1d6"               ),
    ("Halfling",            31,             35,             "2d4",              "1"                 ),
    ("Dragonborn",          66,             175,            "2d8",              "2d6"               ),
    ("Gnome",               35,             35,             "2d4",              "1"                 ),
    ("Half-Elf",            57,             110,            "2d8",              "2d4"               ),
    ("Half-Orc",            58,             140,            "2d10",             "2d6"               ),
    ("Tiefling",            57,             110,            "2d8",              "2d4"               ),
    ("Aasaimar",            56,             110,            "2d10",             "2d4"               ),
    ("Bugbear",             72,             200,            "2d12",             "2d6"               ),
    ("Firbolg",             74,             175,            "2d4",              "2d6"               ),
    ("Goblin",              41,             35,             "2d10",             "1"                 ),
    ("Hobgoblin",           56,             200,            "2d10",             "2d6"               ),
    ("Kenku",               52,             50,             "2d8",              "2d4"               ),
    ("Kobold",              25,             25,             "2d4",              "1"                 ),
    ("Lizardfolk",          57,             120,            "2d10",             "2d6"               ),
    ("Orc",                 64,             175,            "2d8",              "2d6"               ),
    ("Tabaxi",              58,             90,             "2d10",             "2d4"               ),
    ("Triton",              54,             90,             "2d10",             "2d4"               ),
    ("Yuan-ti",             56,             110,            "2d10",             "2d4"               )
    ]

def stature(baseHeight = 56,baseWeight = 110,hMod = '2d10',wMod = '2d4'):
    hRoll = roll(hMod)
    wRoll = roll(wMod)
    
    return [baseHeight+hRoll,baseWeight+(hRoll*wRoll)]

print('Height)
## Parse height
## Example: 6`11``
#def parseHeight(height):
#    # Strip inches
#    height = height.split("``")[0]
#     
#    # Split on feet
#    height = height.split("`")
#    
#    feet = int(height[0])
#    inches = int(height[1])
#    
#    return (feet * 12) + inches
#
#def inchesToHeightString(inches):
#    feet = inches / 12
#    inches = inches % 12
#    return str(feet)+"\'"+str(inches)+"\""
#
## Parse dice roll
## Example: 1d20+4
#def parseRoll(roll):
#    # Check for dice roll
#    if ( roll.find('d') != -1 ):
#        # Parse number of dice
#        roll = roll.split('d')
#        dieCount = int(roll[0])
#        
#        roll = roll[1]
#        dieSize = 0
#        modifier = 0
#
#        # Parse modifiers
#        if (roll.find('+') != -1):
#            roll = roll.split('+')
#            dieSize = int(roll[0])
#            modifer = int(roll[1])
#        elif (roll.find('-') != -1):
#            roll = roll.split('-')
#            dieSize = int(roll[0])
#            modifer = -1 * int(roll[1])
#        else:
#            dieSize = int(roll)
#
#        # Roll and sum dice results
#        rollResult=0
#        while (dieCount > 0):
#            dieRoll = randrange(1,dieSize+1)
#            print "Rolling 1d"+str(dieSize)+" ... "+str(dieRoll)
#            rollResult = rollResult + dieRoll
#            dieCount = dieCount - 1
#
#        # Return roll result
#        return rollResult + modifier
#            
#    # No dice roll, just constant
#    else:
#        return int(roll)
#        
#
#while (True):
#    print "Choose a race from the following:"
#    for i in range(1,len(params)):
#        print str(i) + ") "+params[i][0]
#
#    try:
#        race=int(raw_input('\nSelection: '))
#    except ValueError:
#        print "Not a number"
#        exit
#
#    if (race < 1 or race >= len(params)):
#        print "Invalid race selection: "+str(race)
#        exit
#
#    raceParams = params[race]
#    raceName = raceParams[0]
#    baseHeight = parseHeight(raceParams[1])
#    print "Base height (inches): "+str(baseHeight)
#    baseWeight = raceParams[2]
#    print "Base weight (lb): "+str(baseWeight)
#    modifier = parseRoll(raceParams[3])
#    print "Rolling modifier ("+raceParams[3]+"): "+str(modifier)
#    weightMultiplier = parseRoll(raceParams[4])
#    print "Rolling weight multiplier ("+raceParams[4]+"): "+str(weightMultiplier)
#
#    heightInches = int(baseHeight) + modifier
#    outputHeight = inchesToHeightString(heightInches)
#    
#    outputWeight = baseWeight + ( modifier * weightMultiplier )
#
#    print "\n"+raceName+" Stats:"
#
#    print "Height: "+outputHeight
#    print "Weight: "+str(outputWeight)+" lb."
#    raw_input('\nAgain?')
#    print "\n"
    