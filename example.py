# -*- coding: utf-8 -*-
"""
An example script showing how to use the functions in roll.py

Created on Mon Jan 23 12:07:01 2017

@author: lordmailman
"""

from roll import roll,rollInfo,rollWin,rollLose,critInfo
#from roll import *

# roll magic missile damage N*(1d4+1)
N = 3
# using roll
magic_missile = list()
for ind in range(N): magic_missile.append(roll(1,4,1))

# using rollInfo to just simulate the roll
magic_missile = list()
for ind in range(N): magic_missile.append(rollInfo('1d4+1')['val'])

# using rollInfo to provide the full statistics
#mmInfo = rollInfo('3d4+3')
mmInfo = rollInfo(str(N)+'d4+'+str(N))

print('Firing '+str(N)+' magic missiles, they do...')
print('\ta minimum of '+str(mmInfo['min'])+' damage.')
print('\ta maximum of '+str(mmInfo['max'])+' damage.')
print('\ta mean of '+str(mmInfo['mean'])+' damage.')

# roll an attack roll with advantage and 1d6 Bardic Inspiration (2d20K1 + 1d6 + 5)
atInfo = rollInfo('2d20k1 + 1d6 + 5')
target = 18
print('\nFor an attack roll with advantage, a +5 modifier, and 1d6 of Bardic Inspiration...')
print('\tyou will get a minimum result of '+str(atInfo['min'])+'.')
print('\tyou will get a maximum result of '+str(atInfo['max'])+'.')
print('\tyou will get a mean result of '+str(atInfo['mean'])+'.')
print('\tyou have a '+str(atInfo['critHit']*100)+'% chance of critically hitting.')
print('\tyou have a '+str(atInfo['critMiss']*100)+'% chance of critically missing.')
print('\tyou have a '+str(rollWin(atInfo,target)*100)+'% chance of hitting an AC of '+str(target)+'.')
