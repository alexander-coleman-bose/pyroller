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
    
#%% compare save chances
printSav = True
castMod = 3 # Faen has an Intelligence modifier of 3
profMod = 3 # Faen has a proficiency bonus of 3
#DC = 8+castMod+profMod
DC = 16
attackMod = 4
attackBonus = attackMod+profMod

target = {}
target['name'] = 'Arcanaloth'
target['AC'] = 17
target['saveStr'] = 3
target['saveDex'] = 5
target['saveCon'] = 2
target['saveInt'] = 9
target['saveWis'] = 7
target['saveCha'] = 7
      
dicAtt = info('1d20+'+str(attackBonus))
dicAttA = info('2d20k1+'+str(attackBonus))
dicAttD = info('2d20kl1+'+str(attackBonus))

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
    print('Attack Modifier: '+str(attackBonus))
    print('{:>35}'.format('Chance to hit an AC of '+str(target['AC'])+':')+'{: 7.2%}'.format(win(dicAtt,target['AC'])))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(win(dicAttA,target['AC'])))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(win(dicAttD,target['AC'])))
    print()
    print('Spellcasting DC: '+str(DC))
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Str save:')+'{: 7.2%}'.format(lose(dicStr,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicStrA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicStrD,DC)))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Dex save:')+'{: 7.2%}'.format(lose(dicDex,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicDexA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicDexD,DC)))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Con save:')+'{: 7.2%}'.format(lose(dicCon,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicConA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicConD,DC)))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Int save:')+'{: 7.2%}'.format(lose(dicInt,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicIntA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicIntD,DC)))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Wis save:')+'{: 7.2%}'.format(lose(dicWis,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicWisA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicWisD,DC)))
    print()
    print('{:35}'.format('Chance of failing a DC '+str(DC)+' Cha save:')+'{: 7.2%}'.format(lose(dicCha,DC)))
    print('{:>35}'.format('(with advantage):')+'{: 7.2%}'.format(lose(dicChaA,DC)))
    print('{:>35}'.format('(with disadvantage):')+'{: 7.2%}'.format(lose(dicChaD,DC)))
    
