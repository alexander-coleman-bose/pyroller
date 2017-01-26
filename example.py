# -*- coding: utf-8 -*-
"""
An example script showing how to use the functions in roll.py

Created on Mon Jan 23 12:07:01 2017

@author: lordmailman
"""

from roll import roll,info,win,lose,crit,compare,attack
#from roll import *

# roll magic missile damage N*(1d4+1)
N = 3
# using roll
magic_missile = list()
for ind in range(N): magic_missile.append(roll('1d4+1'))

# using rollInfo to just simulate the roll
magic_missile = list()
for ind in range(N): magic_missile.append(info('1d4+1')['val'])

# using rollInfo to provide the full statistics
#mmInfo = rollInfo('3d4+3')
mmInfo = info(str(N)+'d4+'+str(N))

print('Firing '+str(N)+' magic missiles, they do...')
print('\ta minimum of '+str(mmInfo['min'])+' damage.')
print('\ta maximum of '+str(mmInfo['max'])+' damage.')
print('\ta mean of '+str(mmInfo['mean'])+' damage.')

# roll an attack roll with advantage and 1d6 Bardic Inspiration (2d20K1 + 1d6 + 5)
atInfo = info('2d20k1 + 1d6 + 5')
target = 18
print('\nFor an attack roll with advantage, a +5 modifier, and 1d6 of Bardic Inspiration...')
print('\tyou will get a minimum result of '+str(atInfo['min'])+'.')
print('\tyou will get a maximum result of '+str(atInfo['max'])+'.')
print('\tyou will get a mean result of '+str(atInfo['mean'])+'.')
print('\tyou have a '+str(atInfo['critHit']*100)+'% chance of critically hitting.')
print('\tyou have a '+str(atInfo['critMiss']*100)+'% chance of critically missing.')
print('\tyou have a '+str(win(atInfo,target)*100)+'% chance of hitting an AC of '+str(target)+'.')

##compare 1-5 level fighter, rogue, wizard, and monk
# fighter
level = [1,2,3,4,5]
prof = [2,2,2,2,3]
mod = [3,3,3,4,4]

fighter = {}
fighter['attacks'] = [0]*len(level)
fighter['damage_die'] = '1d12'

for ind in range(len(level)):
    fighter['attacks'][ind] = [attack('1d20+'+str(mod[ind]),fighter['damage_die'],str(prof[ind]+mod[ind]))]
    if level[ind] >= 5:
        fighter['attacks'][ind].append(attack('1d20+'+str(mod[ind]),fighter['damage_die'],str(prof[ind]+mod[ind])))
        
print(fighter)