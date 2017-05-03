# -*- coding: utf-8 -*-
"""
An example script showing how to use the functions in roll.py

Created on Mon Jan 23 12:07:01 2017

@author: lordmailman
"""

from roll import roll,info,win,lose,crit,compare,attack
import matplotlib
import matplotlib.pyplot as plt
#from roll import *

#%%
printMM = False
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

if printMM:
    print('Firing '+str(N)+' magic missiles, they do...')
    print('\ta minimum of '+str(mmInfo['min'])+' damage.')
    print('\ta maximum of '+str(mmInfo['max'])+' damage.')
    print('\ta mean of '+str(mmInfo['mean'])+' damage.')

#%% roll an attack roll with advantage and 1d6 Bardic Inspiration (2d20K1 + 1d6 + 5)
printAtt = False
atInfo = info('2d20k1 + 1d6 + 5')
target = 18

if printAtt:
    print('\nFor an attack roll with advantage, a +5 modifier, and 1d6 of Bardic Inspiration...')
    print('\tyou will get a minimum result of '+str(atInfo['min'])+'.')
    print('\tyou will get a maximum result of '+str(atInfo['max'])+'.')
    print('\tyou will get a mean result of '+str(atInfo['mean'])+'.')
    print('\tyou have a '+str(atInfo['critHit']*100)+'% chance of critically hitting.')
    print('\tyou have a '+str(atInfo['critMiss']*100)+'% chance of critically missing.')
    print('\tyou have a '+str(win(atInfo,target)*100)+'% chance of hitting an AC of '+str(target)+'.')

#%% compare 1-5 level fighter, rogue, wizard, and monk
# fighter
#level = [1,2,3,4,5]
#prof = [2,2,2,2,3]
#mod = [3,3,3,4,4]
#
#fighter = {}
#fighter['attacks'] = [0]*len(level)
#fighter['damage_die'] = '1d12'
#
#for ind in range(len(level)):
#    fighter['attacks'][ind] = [attack('1d20+'+str(mod[ind]),fighter['damage_die'],str(prof[ind]+mod[ind]))]
#    if level[ind] >= 5:
#        fighter['attacks'][ind].append(attack('1d20+'+str(mod[ind]),fighter['damage_die'],str(prof[ind]+mod[ind])))
#        
#print(fighter)

#%% compare counterspell chances
printCS = False
castingMod = 3 # Faen has +3 Intelligence modifier
dic = info('1d20+'+str(castingMod))
dicA = info('2d20k1+'+str(castingMod))

SL = list(range(1,10))
listDC = list(range(11,20))
listProb = [0]*len(listDC)
listProbA = [0]*len(listDC)
for ind in range(len(listDC)):
    if ind < 3:
        listProb[ind] = 1
        listProbA[ind] = 1
    else:
        listProb[ind] = win(dic,listDC[ind])
        listProbA[ind] = win(dicA,listDC[ind])

if printCS:
    plt.plot(SL,listProb,SL,listProbA)
    plt.axis([1,9,0,1])
    plt.show()
    
#%% Compare Expertise to advantage
printEx = False
abilityMod = 3
profMod = 2

dic = info('1d20+'+str(abilityMod+profMod))
dicE = info('1d20+'+str(abilityMod+2*profMod))
dicA = info('2d20k1+'+str(abilityMod+profMod))
dicB = info('2d20k1+'+str(abilityMod+2*profMod))

listDC = list(range(1,31))
listProb = [0]*len(listDC)
listProbE = [0]*len(listDC)
listProbA = [0]*len(listDC)
listProbB = [0]*len(listDC)

for ind in range(len(listDC)):
    listProb[ind] = win(dic,listDC[ind])
    listProbE[ind] = win(dicE,listDC[ind])
    listProbA[ind] = win(dicA,listDC[ind])
    listProbB[ind] = win(dicB,listDC[ind])

if printEx:
    plt.plot(listDC,listProb,listDC,listProbE,listDC,listProbA,listDC,listProbB)
    plt.axis([1,30,0,1])
    plt.show()
    
#%% compare save chances
printSav = True
#castMod = 3 # Faen has an Intelligence modifier of 3
#profMod = 3 # Faen has a proficiency bonus of 3
##DC = 8+castMod+profMod
#DC = 16
#attackMod = 4
#attackBonus = attackMod+profMod

Arcloth = {}
Arcloth['name'] = 'Arcanaloth'
Arcloth['AC'] = 17
Arcloth['DC'] = 17
Arcloth['att'] = 7
Arcloth['dam'] = '2d4+3'
Arcloth['saveStr'] = 3
Arcloth['saveDex'] = 5
Arcloth['saveCon'] = 2
Arcloth['saveInt'] = 9
Arcloth['saveWis'] = 7
Arcloth['saveCha'] = 7
       
Strahd = {}
Strahd['name'] = 'Strahd'
Strahd['AC'] = 16
Strahd['DC'] = 18
Strahd['att'] = 9
Strahd['dam'] = '1d8+4d6+4'
Strahd['saveStr'] = 4
Strahd['saveDex'] = 9
Strahd['saveCon'] = 4
Strahd['saveInt'] = 5
Strahd['saveWis'] = 7
Strahd['saveCha'] = 9
       
Faen = {}
Faen['name'] = 'Faen Liadon'
Faen['AC'] = 20
Faen['DC'] = 16
Faen['att'] = 9
Faen['dam'] = '1d8+1d8+2d8+3d6'
Faen['damM'] = '5'
Faen['saveStr'] = 0
Faen['saveDex'] = 7
Faen['saveCon'] = 1
Faen['saveInt'] = 8
Faen['saveWis'] = 6
Faen['saveCha'] = -1
    
you = Faen
target = Strahd
      
dicAtt = info('1d20+'+str(you['att']))
dicAttA = info('2d20k1+'+str(you['att']))
dicAttD = info('2d20kl1+'+str(you['att']))
dicDam = info(you['dam'])

dicStr = info('1d20+'+str(target['saveStr']))
dicStrA = info('2d20k1+'+str(target['saveStr']))
dicStrD = info('2d20kl1+'+str(target['saveStr']))
dicDex = info('1d20+'+str(target['saveDex']))
dicDexA = info('2d20k1+'+str(target['saveDex']))
dicDexD = info('2d20kl1+'+str(target['saveDex']))
dicCon = info('1d20+'+str(target['saveCon']))
dicConA = info('2d20k1+'+str(target['saveCon']))
dicConD = info('2d20kl1+'+str(target['saveCon']))
dicInt = info('1d20+'+str(target['saveInt']))
dicIntA = info('2d20k1+'+str(target['saveInt']))
dicIntD = info('2d20kl1+'+str(target['saveInt']))
dicWis = info('1d20+'+str(target['saveWis']))
dicWisA = info('2d20k1+'+str(target['saveWis']))
dicWisD = info('2d20kl1+'+str(target['saveWis']))
dicCha = info('1d20+'+str(target['saveCha']))
dicChaA = info('2d20k1+'+str(target['saveCha']))
dicChaD = info('2d20kl1+'+str(target['saveCha']))

if printSav:
    print('Attack Modifier: '+str(you['att']))
    print('{:>35}'.format('Chance to hit an AC of '+str(target['AC'])+':')+'{: 7.2%}'.format(win(dicAtt,target['AC'])))
    print('{:>35}'.format('For average damage of:')+'{: 7.2f}'.format(attack('1d20+'+str(you['att']),you['dam'],you['damM'],target['AC'])['avg']))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(win(dicAttA,target['AC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(win(dicAttD,target['AC'])))
    print()
    print('Spellcasting DC: '+str(you['DC']))
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Str save:')+'{: 7.2%}'.format(lose(dicStr,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicStrA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicStrD,you['DC'])))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Dex save:')+'{: 7.2%}'.format(lose(dicDex,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicDexA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicDexD,you['DC'])))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Con save:')+'{: 7.2%}'.format(lose(dicCon,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicConA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicConD,you['DC'])))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Int save:')+'{: 7.2%}'.format(lose(dicInt,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicIntA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicIntD,you['DC'])))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Wis save:')+'{: 7.2%}'.format(lose(dicWis,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicWisA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicWisD,you['DC'])))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(you['DC'])+' Cha save:')+'{: 7.2%}'.format(lose(dicCha,you['DC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicChaA,you['DC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicChaD,you['DC'])))
    
