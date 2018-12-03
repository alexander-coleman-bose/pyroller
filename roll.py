# -*- coding: utf-8 -*-
"""Helper functions to calculate the probabilities of given die rolls and to simulate die rolls.

Functions:
    roll(numD = 1,typeD = 20,modD = 0,keepLow = 0,keepHigh = 0,rerollD = 0)
        simulates the specified die roll
    info(varargin_clean = "1d20")
        calculates the probabilities of specific results of a given die roll
    win(dic,target = 15)
        returns the summed probability of meeting or exceeding the target value
    lose(dic,target = 15)
        returns the summed probability of not meeting the target value
    crit(dic)
        returns the probabilities of critical hits and misses for rolls that can crit
        
TODO:
    * https://wiki.roll20.net/Dice_Reference
        * exploding dice
    * configuration system for reroll, crit, and exploding behavior
    * function to compare one roll to another
    * BUG: negD on '-2d20k1' doesn't work
    * get keepLow and keepHigh working for any roll fed into info
    * get rerollD to support multiple values in roll and info
    * get rerollD probabilities for info
    * get median values, not just mean
        
Created on Tue Jan 17 10:28:14 2017

@author: lordmailman
"""

from math import floor
from random import randint
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def roll(varargin_clean, infoFlag = False):
    """Simulates the specified die roll
    
    Args:
        varargin_clean(str): A string that describes the die roll. Default:1d20
            In the form of '(numDice)d(numSides)(tag)# + (numDice)d(numSides)(tag)# + ...
            Tags:
                'd' or 'dl': drop # of the lowest dice
                'D' or 'dh': drop # of the highest dice
                'k' or 'kh': keep # of the highest dice
                'kl': keep # of the lowest dice
                'r': reroll any die that hits this value
            Refer to:
                https://wiki.roll20.net/Dice_Reference
                (Not all functionality is working)
        infoFlag(bool): If True, run info on the input instead
        
    Returns:
        float: The summed value of the simulated roll. IFF infoFlag is False.
        dict: The dictionary returned from info. IFF infoFlag is True.
    
    Examples:
        val = roll('2d4') # rolls two four-sided dice
        val = roll('1d20+5') # rolls a twenty-sided die and adds 5
        val = roll('2d20k1') # rolls two twenty-sided dice and keeps the highest
        val = roll('2d20kl1') # rolls two twenty-sided dice and keeps the lowest
        val = roll('2d6r1') # rolls 2d6 and rerolls (once) any '1's
        val = roll('2d20K1+1d8+1) # rolls 2d20 at advantage and adds 1d8 + 5
        
    """
    
    if infoFlag:
        return info(varargin_clean)
    else:
    # delete spaces and replace '-' with a '+-' so that the split works
        varargin_clean = varargin_clean.replace(" ","")
        varargin = varargin_clean.replace("+-","-")
        varargin = varargin.replace("-","+-")
    # split the string into discrete rolls
        splits = varargin.split('+')
        nSplits = len(splits)
        
        numD = [0] * nSplits
        typeD = [0] * nSplits
        modD = [0] * nSplits
        dropLow = [0] * nSplits
        dropHigh = [0] * nSplits
        keepLow = [0] * nSplits
        keepHigh = [0] * nSplits
        rerollD = [0] * nSplits
        negD = [0] * nSplits
        
        # use this variable to sum up the result
        val = 0
        
        for indS in range(len(splits)):
            # parse for numD or modD
            tmp = re.search(r'^(-|)(\d+)d',splits[indS])
            if tmp:
                numD[indS] = int(tmp.group().strip('d'))
            else:
                # if there isn't a 'd', then assume that the only value is modD
                modD[indS] = int(splits[indS])
                
            # parse for typeD and dropLow
            tmp = re.findall(r'(d)(\d+)',splits[indS])
            if len(tmp) > 2:
                raise RuntimeError("You can't use two separate drop low calls in a die slice.")
            elif len(tmp) > 1:
                typeD[indS] = int(tmp[0][1])
                dropLow[indS] = int(tmp[1][1])
            elif len(tmp) > 0:
                typeD[indS] = int(tmp[0][1])
                
            rerollD[indS] = []
            tmp = re.findall(r'(d|D|dl|dh|k|kl|kh|r)(\d+)',splits[indS])
            for indT in range(len(tmp)):
                if tmp[indT][0] in ['dl']:
                    dropLow[indS] = int(tmp[indT][1])
                    
                if tmp[indT][0] in ['D','dh']:
                    dropHigh[indS] = int(tmp[indT][1])
                    
                if tmp[indT][0] in ['k','kh']:
                    keepHigh[indS] = int(tmp[indT][1])
                    
                if tmp[indT][0] in ['kl']:
                    dropHigh[indS] = int(tmp[indT][1])
                    
                if tmp[indT][0] in ['r']:
                    rerollD[indS].append(int(tmp[indT][1]))
    
            if keepLow[indS] and keepHigh[indS]:
                raise RuntimeError("You can keep the lowest or the highest rolls, not both.")
            elif (keepLow[indS] or keepHigh[indS]) and (dropLow[indS] or dropHigh[indS]):
                raise RuntimeError("You can't both drop and keep dice.")
            elif keepLow[indS]<0 or (keepLow[indS]>=numD[indS] and keepLow[indS]):
                raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
            elif keepHigh[indS]<0 or (keepHigh[indS]>=numD[indS] and keepHigh[indS]):
                raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
            elif dropLow[indS]<0 or (dropLow[indS]>=numD[indS] and dropLow[indS]):
                raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
            elif dropHigh[indS]<0 or (dropHigh[indS]>=numD[indS] and dropHigh[indS]):
                raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
#            elif rerollD[indS]<0 or rerollD[indS]>typeD[indS]:
#                raise RuntimeError("You cannot reroll numbers higher than the die has.")
                        
            if numD[indS]<0:
                negD[indS] = 1
                numD[indS] = -1*numD[indS]
            else:
                negD[indS] = 0
        
        # generate an actual rolled value for the die roll
            rolls = list()
            tmp = 0
            
            for indN in range(numD[indS]):
                tmp = randint(1,typeD[indS])
                if tmp in rerollD[indS]:
                    tmp = randint(1,typeD[indS])
                rolls.append(tmp)
                
            if dropLow[indS]>0:
                for indK in range(dropLow[indS]):
                    rolls.pop(rolls.index(min(rolls)))
                    
            if dropHigh[indS]>0:
                for indK in range(dropHigh[indS]):
                    rolls.pop(rolls.index(max(rolls)))
            
            if keepLow[indS]>0:
                for indK in range(numD[indS]-keepLow[indS]):
                    rolls.pop(rolls.index(max(rolls)))
                    
            if keepHigh[indS]>0:
                for indK in range(numD[indS]-keepHigh[indS]):
                    rolls.pop(rolls.index(min(rolls)))
                    
            val = val + ((-1)**negD[indS])*sum(rolls) + modD[indS]
        # end for every die slice
        
        return val
    
def info(varargin_clean = "1d20"):
    """Calculates the probabilities of and simulates the given die roll
    
    Args:
        varargin_clean(str): A string that describes the die roll. Default:1d20
            In the form of '(numDice)d(numSides)(tag)# + (numDice)d(numSides)(tag)# + ...
            Tags:
                'd' or 'dl': drop # of the lowest dice
                'D' or 'dh': drop # of the highest dice
                'k' or 'kh': keep # of the highest dice
                'kl': keep # of the lowest dice
                'r': reroll any die that hits this value
            Refer to:
                https://wiki.roll20.net/Dice_Reference
                (Not all functionality is working)
        
    Returns:
        dic(dict): A dictionary with the following fields:
            'roll':(str) The roll string, stripped of white-space
            'min':(float) The minimum roll result
            'max':(float) The maximum roll result
            'val':(float) The value of one simulated roll using the given dice
            'results':(list) A list of the probabilities of each result, from
                dic['min'] to dic['max']. 'd','dl','D','dh','k','kl','kh'
                    (keepLow/High and dropLow/High) only work for 2d20 rolls
            'keys':(list) A list of the values of each result, keyed to 'results'
            'mean':(float) The average value of the roll. 'd','dl','D','dh','k',
                'kl','kh' (keepLow/High and dropLow/High) only work for 2d20 rolls
            'critHit':(float) The probability that the given roll will
                critically hit
            'critMiss':(float) The probability that the given roll will
                critically miss
    
    Examples:
        dic = info('2d4') # rolls two four-sided dice
        dic = info('1d20+5') # rolls a twenty-sided die and adds 5
        dic = info('2d20k1') # rolls two twenty-sided dice and keeps the highest
        dic = info('2d20kl1') # rolls two twenty-sided dice and keeps the lowest
        dic = info('2d6r1') # rolls 2d6 and rerolls (once) any '1's
        dic = info('2d20K1+1d8+1) # rolls 2d20 at advantage and adds 1d8 + 5
        
    """
    
    def ss(numD):
        tmp = 0
        for ind in range(numD):
            tmp = tmp + (ind+1)**2
        return tmp
        
    def ds(numD):
        tmp = 0
        for ind in range(numD):
            tmp = tmp + (ind+1)*(20-ind)
        return tmp
    
    # delete spaces and replace '-' with a '+-' so that the split works
    varargin_clean = varargin_clean.replace(" ","")
    varargin = varargin_clean.replace("+-","-")
    varargin = varargin.replace("-","+-")
    # split the string into discrete rolls
    splits = varargin.split('+')
    nSplits = len(splits)
    
    numD = [0] * nSplits
    typeD = [0] * nSplits
    modD = [0] * nSplits
    dropLow = [0] * nSplits
    dropHigh = [0] * nSplits
    keepLow = [0] * nSplits
    keepHigh = [0] * nSplits
    rerollD = [0] * nSplits
    negD = [0] * nSplits
    
    dic = {}
    dic['roll'] = varargin_clean
    dic['min'] = 0
    dic['max'] = 0
    dic['val'] = 0
    dic['results'] = 0
    dic['keys'] = 0
    dic['mean'] = 0
    dic['critHit'] = 0
    dic['critMiss'] = 0
    
    results = list()
#    keys = list()
    
    if not splits[0]: splits.pop(0)
    
    for indS in range(len(splits)):
        # parse for numD or modD
        tmp = re.search(r'^(-|)(\d+)d',splits[indS])
        if tmp:
            numD[indS] = int(tmp.group().strip('d'))
        else:
            # if there isn't a 'd', then assume that the only value is modD
            modD[indS] = int(splits[indS])
            
        # parse for typeD and dropLow
        tmp = re.findall(r'(d)(\d+)',splits[indS])
        if len(tmp) > 2:
            raise RuntimeError("You can't use two separate drop low calls in a die slice.")
        elif len(tmp) > 1:
            typeD[indS] = int(tmp[0][1])
            dropLow[indS] = int(tmp[1][1])
        elif len(tmp) > 0:
            typeD[indS] = int(tmp[0][1])
            
        rerollD[indS] = []
        tmp = re.findall(r'(D|dl|dh|k|kl|kh|r)(\d+)',splits[indS])
        for indT in range(len(tmp)):
            if tmp[indT][0] in ['dl']:
                dropLow[indS] = int(tmp[indT][1])
                
            if tmp[indT][0] in ['D','dh']:
                dropHigh[indS] = int(tmp[indT][1])
                
            if tmp[indT][0] in ['k','kh']:
                keepHigh[indS] = int(tmp[indT][1])
                
            if tmp[indT][0] in ['kl']:
                dropHigh[indS] = int(tmp[indT][1])
                
            if tmp[indT][0] in ['r']:
                rerollD[indS].append(int(tmp[indT][1]))
                
        #debug
#        print(indS)
#        print(keepLow,keepHigh,dropLow,dropHigh)
#        print(numD)
#        print(splits[indS])
            
        if numD[indS]<0:
            negD[indS] = 1
            numD[indS] = -1*numD[indS]
        else:
            negD[indS] = 0

        if keepLow[indS] and keepHigh[indS]:
            raise RuntimeError("You can keep the lowest or the highest rolls, not both.")
        elif (keepLow[indS] or keepHigh[indS]) and (dropLow[indS] or dropHigh[indS]):
            raise RuntimeError("You can't both drop and keep dice.")
        elif keepLow[indS]<0 or (keepLow[indS]>=numD[indS] and keepLow[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
        elif keepHigh[indS]<0 or (keepHigh[indS]>=numD[indS] and keepHigh[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
        elif dropLow[indS]<0 or (dropLow[indS]>=numD[indS] and dropLow[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
        elif dropHigh[indS]<0 or (dropHigh[indS]>=numD[indS] and dropHigh[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
#        elif rerollD[indS]<0 or rerollD[indS]>typeD[indS]:
#            raise RuntimeError("You cannot reroll numbers higher than the die has.")
    
#        if len(rerollD[indS])>0:
#            print('Warning: rerolls are not supported by info')
        
    # establish the minimum and maximum values for this roll
        if keepLow[indS] or keepHigh[indS]:
            thisMin = ((-1)**negD[indS])*(keepLow[indS]+keepHigh[indS])*(typeD[indS]**negD[indS]) + modD[indS]
            thisMax = ((-1)**negD[indS])*(keepLow[indS]+keepHigh[indS])*(typeD[indS]**(1-negD[indS])) + modD[indS]
        else:
            thisMin = ((-1)**negD[indS])*(numD[indS]-dropLow[indS]-dropHigh[indS])*(typeD[indS]**negD[indS]) + modD[indS]
            thisMax = ((-1)**negD[indS])*(numD[indS]-dropLow[indS]-dropHigh[indS])*(typeD[indS]**(1-negD[indS])) + modD[indS]
        
        #debug
#        print(indS,splits)
#        print(numD,typeD,modD,negD,rerollD)
#        print(keepLow,keepHigh,dropLow,dropHigh)
#        print(thisMax,thisMin)
    
    # generate an actual rolled value for the die roll
        rolls = list()
        tmp = 0
        
        for indN in range(numD[indS]):
            tmp = randint(1,typeD[indS])
            if tmp in rerollD[indS]:
                tmp = randint(1,typeD[indS])
            rolls.append(tmp)
            
        if dropLow[indS]>0:
            for indK in range(dropLow[indS]):
                rolls.pop(rolls.index(min(rolls)))
                
        if dropHigh[indS]>0:
            for indK in range(dropHigh[indS]):
                rolls.pop(rolls.index(max(rolls)))
        
        if keepLow[indS]>0:
            for indK in range(numD[indS]-keepLow[indS]):
                rolls.pop(rolls.index(max(rolls)))
                
        if keepHigh[indS]>0:
            for indK in range(numD[indS]-keepHigh[indS]):
                rolls.pop(rolls.index(min(rolls)))
                
        dic['val'] = dic['val'] + ((-1)**negD[indS])*sum(rolls) + modD[indS]
        
    # compute the probabilities
        thisResult = [0] * (thisMax-thisMin+1)
        # if an advantage or disadvantage roll
        if numD[indS] == 2 and typeD[indS] == 20 and (keepHigh[indS] == 1 or keepLow[indS] == 1 or dropLow[indS] == 1 or dropHigh[indS] == 1):
            if keepHigh[indS] or dropLow[indS]:
                for indD in range(typeD[indS]):
                    n = indD+1 # ind is 0 through typeD
                    tmp = (2*n-1)/typeD[indS]**numD[indS]
                    thisResult[indD] = tmp
                dic['mean'] = dic['mean'] + ((-1)**negD[indS])*(2*ss(typeD[indS])-(1+typeD[indS])*(typeD[indS]/2))/typeD[indS]**numD[indS]

            elif keepLow[indS] or dropHigh[indS]:
                for indD in range(typeD[indS]):
                    n = indD+1 # ind is 0 through typeD
                    tmp = (2*(21-n)-1)/typeD[indS]**numD[indS]
                    thisResult[indD] = tmp
                dic['mean'] = dic['mean'] + ((-1)**negD[indS])*(2*ds(typeD[indS])-(1+typeD[indS])*(typeD[indS]/2))/typeD[indS]**numD[indS]
                
            else:
                raise RuntimeError("Unexpected error: keepHigh or keepLow should = 1.")
                
            if dic['critHit'] == 0:
                dic['critHit'] = thisResult[thisMax-1]
                dic['critMiss'] = thisResult[thisMin-1]
                
        elif ~keepLow[indS] and ~keepHigh[indS] and ~dropLow[indS] and ~dropHigh[indS]:            
            if typeD[indS] == 20 and dic['critHit'] == 0:
                dic['critHit'] = 1/20
                dic['critMiss'] = 1/20
            
            result = np.array([0])
            if typeD[indS]:
                resultDie = np.array([1/typeD[indS]]*typeD[indS],dtype=float)
            else:
                resultDie = np.array([1])
            for indD in range(typeD[indS]):
                if indD+1 in rerollD[indS]:
                    resultDie[indD] = len(rerollD[indS])/(typeD[indS]**2)
                else:
                    resultDie[indD] = (len(rerollD[indS])+typeD[indS])/(typeD[indS]**2)
                    
            for indN in range(numD[indS]):
                if indN == 0:
                    result = resultDie
                else:
                    resultArray = result[np.newaxis].T @ resultDie[np.newaxis]
                    tmp = [resultArray[::-1,:].diagonal(i) for i in range(-resultArray.shape[0]+1,resultArray.shape[1])]
                    diags = [sum(resultArray.tolist()) for resultArray in tmp]
                    result = np.array(diags)
            
#                # debug
##                print(results_all)
##                print(sum(result),thisMin,thisMax)
##                print(thisResult)
##                print(modD[indS])

            if typeD[indS]:
                thisResult = result.tolist()
#            elif negD[indS]:
#                thisResult = reversed(result.tolist())
            else:
                thisResult = [1]
                
#            dic['mean'] = dic['mean'] + ((-1)**negD[indS])*numD[indS]*(1+typeD[indS])/2 + modD[indS]
            if negD[indS]:
                dic['mean'] = dic['mean'] + sum(np.array(range(thisMin,thisMax+1))*np.array(list(reversed(thisResult))))
            else:
                dic['mean'] = dic['mean'] + sum(np.array(range(thisMin,thisMax+1))*np.array(thisResult))

        else:
            print('Warning: dropLow/High and keepLow/High are not fully supported by info.')
        
        # if results is empty, this is the first split
        if not any(results):
            if negD[indS]:
                results = np.array(list(reversed(thisResult)),dtype=float)
            else:
                results = np.array(thisResult,dtype=float)
        else:
            if negD[indS]:
                resultsArray = results[np.newaxis].T @ np.array(list(reversed(thisResult)),dtype=float)[np.newaxis]
            else:
                resultsArray = results[np.newaxis].T @ np.array(thisResult,dtype=float)[np.newaxis]
            
            tmp = [resultsArray[::-1,:].diagonal(i) for i in range(-resultsArray.shape[0]+1,resultsArray.shape[1])]
            diags = [sum(resultsArray.tolist()) for resultsArray in tmp]
            results = np.array(diags)
                   
        dic['min'] = dic['min'] + thisMin
        dic['max'] = dic['max'] + thisMax
        # end for every indS loop
    
    dic['avg'] = dic['mean']
    dic['keys'] = list(range(dic['min'],dic['max']+1))
    dic['results'] = results.tolist()
            
    return dic
    
def attack(dicA = '1d20',dicD = '1d8',dicM = '0',target = 15):
    """Returns a dictionary with stats about an attack and damage roll.
    
    Args:
        dicA (dict|str): A dictionary result from a d20 info roll
        dicD (dict|str): A dictionary result from an info roll for damage (no mod)
        dicM (dict|str): A dictionary result from an info roll for damage modifier
        target (int): The target AC against the attack
        
    Returns:
        dic (dict): A dictionary that contains stats on the rolls
            'hit' (float): probability that the attack will hit
            'avg' (float): average damage per attack against target
        
    """
    if type(dicD) in [type(0),type(0.0)]:
        target = dicD
    if type(dicA) is type([]):
        dicM = dicA[2]
        dicD = dicA[1]
        dicA = dicA[0]
    if type(dicA) is type(''):
        dicA = info(dicA)
    if type(dicD) is type(''):
        dicD = info(dicD)
    if type(dicM) is type(''):
        dicM = info(dicM)
    
    # probability that the attack will hit
    hit = win(dicA,target)
    
    # average damage if every attack hit
    avg_raw = dicD['mean'] + dicM['mean']
    avg_crit = 2*dicD['mean'] + dicM['mean'] # crits double the dice used, but not the modifier
    
    # average damage adjusted for hit probability
    avg = (hit-dicA['critHit'])*avg_raw + dicA['critHit']*avg_crit
    
    
#    dic = dicA
    dic = {}
    dic['hit'] = hit
    dic['avg_raw'] = avg_raw
    dic['avg_crit'] = avg_crit
    dic['avg'] = avg
    dic['roll'] = [dicA['roll'],dicD['roll'],dicM['roll']]
    dic['min_attack'] = dicA['min']
    dic['max_attack'] = dicA['max']
    dic['min_damage'] = dicD['min']
    dic['max_damage'] = 2*dicD['max']+dicM['max']
    
    return dic
        
def win(dic = '1d20',target = 15):
    """Returns the probability that the given roll will meet or exceed the target value
    
    Args:
        dic (dict|str): A dictionary result from a info roll
        target (int): The target value
        
    Returns:
        float: The probability that the given roll will meet or exceed the
            target value
            
    """
    # gives the probability that a given roll will meet or exceed the target
#    return sum(dic['results_all'][0][k] for k in range(target,max(dic['results_all'][0])+1))
    if type(dic) is type(''):
        dic = info(dic)
        
    dicLen = len(dic['results'])
    if min(dic['keys'])>=target:
        if dic['critMiss']:
            return 1-dic['critMiss']
        else:
            return 1
    elif target>max(dic['keys']):
        if dic['critHit']:
            return dic['critHit']
        else:
            return 0
    else:
        return sum(dic['results'][k] for k in range(target-dic['min'],dicLen))
        
def lose(dic = '1d20',target = 15):
    """Returns the probability that the given roll will fail to meet the target value
    
    Args:
        dic (dict|str): A dictionary result from a info roll
        target (int): The target value
        
    Returns:
        float: The probability that the given roll will fail to meet the target
            value
            
    """
    # gives the probability that a given roll will fail to meet the target
#    return sum(dic['results_all'][0][k] for k in range(min(dic['results_all'][0]),target))
    if type(dic) is type(''):
        dic = info(dic)
        
    if min(dic['keys'])>=target:
        if dic['critMiss']:
            return dic['critMiss']
        else:
            return 0
    elif target>max(dic['keys']):
        if dic['critHit']:
            return 1-dic['critHit']
        else:
            return 1
    else:
        return sum(dic['results'][k] for k in range(target-dic['min']))
    
def crit(dic = '1d20'):
    """Returns the probability that the given roll will critically miss or hit
        if applicable
    
    Args:
        dic (dict|str): A dictionary result from a info roll of str
        
    Returns:
        dict: {'critHit':dic['critHit'],'critMiss':dic['critMiss']}
            
    """
    if type(dic) is type(''):
        dic = info(dic)
    # gives the probability that a given roll will critically hit or miss
    return {'critHit':dic['critHit'],'critMiss':dic['critMiss']}
    
def compare(dicA,dicB,printFlag = False):
    """Compares two rolls and compares the probability that one will be higher.
    
    Args:
        dicA (dict|str): A dictionary result from a info roll of str.
        dicB (dict|str): A dictionary result from a info roll of str.
        printFlag (bool): A bool to determine whether to print the result.
        
    Returns:
        dic (dict): A dictionary result of A-B
        
    Examples:
        dic = compare(dicA,dicB) # compare rollA to rollB, give dictionary
        compare(dicA,dicB,1) # compare rollA to rollB, print a comparison
        compare('1d20+5','2d20k1') # compare 1d20+5 to 2d20k1, print the dic
        
    """
    if type(dicA) is type(''):
        dicA = info(dicA)
    if type(dicB) is type(''):
        dicB = info(dicB)
        
    if printFlag:
        raise RuntimeError('roll.compare: printFlag not supported yet.')
    else:
        tmp = dicB['roll']
        tmp = tmp.replace('+-','-')
        tmp = tmp.replace('-','+-')
        tmp = tmp.replace('+','-')
        tmp = tmp.replace('--','+')
        if tmp[0] is not '-': tmp = '-'+tmp
        return info(dicA['roll']+tmp)
     
#info('1d20+0')
#info('-2d20k1')
#info('-1d6r1')
#info('2d20dl1')
#attack('1d20+5','1d8','3')

#advantage
#1   1/20*1/20=0.0025
#1   1=1
#2   1/20*1/20+1/20*2/20 = 0.0075
#2   1+2=3
#3   1/20*1/20+1/20*1/20+1/20*3/20
#3   1+1+3=5
#
#(2n-1)/20**2=individual chance
#20*(2*20-1)/20^2 + 19*(2*19-1)/20^2 + ...
#2*20*20-20 + 2*19*19-19 + ...
#2(20^2+19^2+...)-20-19-18-...
#
#average value for 5e advantage
#(2*ss(typeD)-(1+typeD)*(typeD/2))/typeD**2
#
#disadvantage
#20   1/20*1/20=0.0025
#20   1=1
#19   1/20*1/20+1/20*2/20 = 0.0075
#19   1+2=3
#3   1/20*1/20+1/20*1/20+1/20*3/20
#3   1+1+3=5
#
#(2(21-n)-1)/20**2=individual chance
#20*(2*(21-20)-1)/20^2 + 19*(2*(21-19)-1)/20^2 + ...
#2*20*(1)-20 + 2*19*(2)-19 + ...
#2(20^2+19^2+...)-20-19-18-...
#
#average value for 5e disadvantage
#(2*ds(typeD)-(1+typeD)*(typeD/2))/typeD**2
#
#3d4k1   k2  t1
#111 1   11  1
#112 2   12  1
#113 3   13  1
#114 4   14  1
#121 2   12  1
#122 2   22  1
#123 3   23  1
#124 4   24  1
#131 3   13  1
#132 3   23  1
#133 3   33  1
#134 4   34  1
#141 4   14  1
#142 4   24  1
#143 4   34  1
#144 4   44  1
#211 2   12  1
#212 2   22  1
#213 3   23  1
#214 4   24  1
#221 2   22  1
#222 2   22  2
#223 3   23  2
#224 4   24  2
#231 3   23  1
#232 3   23  2
#233 3   33  2
#234 4   34  2
#241 4   24  1
#242 4   24  2
#243 4   34  2
#244 4   44  2
#311 3   13  1
#312 3   23  1
#313 3   33  1
#314 4   34  1
#321 3   23  1
#322 3   23  2
#323 3   33  2
#324 4   34  2
#331 3   33  1
#332 3   33  2
#333 3   33  3
#334 4   34  3
#341 4   34  1
#342 4   34  2
#343 4   34  3
#344 4   44  3
#411 4   14  1
#412 4   24  1
#413 4   34  1
#414 4   44  1
#421 4   24  1
#422 4   24  2
#423 4   34  2
#424 4   44  2
#431 4   34  1
#432 4   34  2
#433 4   34  3
#434 4   44  3
#441 4   44  1
#442 4   44  2
#443 4   44  3
#444 4   44  4
#1   1       37
#2   7       19
#3   19      7
#4   37      1
#11      1
#12      3
#13      3
#14      3
#22      4
#23      9
#24      9
#33      7
#34      15
#44      10
#
#1   1*1*1 = 1
#2   1*2*2 + 1*1*2 + 1*1*1 = 7
#3   1*3*3 + 2*1*3 + 2*2*1 = 19
#4   1*4*4 + 3*1*4 + 3*3*1 = 37
#n**2 + n(n-1) + (n-1)**2
#
#4d4k1
#1   1*1*1*1 = 1
#2   1*2*2*2 + 1*1*2*2 + 1*1*1*2 + 1*1*1*1 = 15
#3   1*3*3*3 + 2*1*3*3 + 2*2*1*3 + 2*2*2*1 = 65
#4   1*4*4*4 + 3*1*4*4 + 3*3*1*4 + 3*3*3*1 = 175
#
#probability for each value of MdNk1
#(n**(M-1) + n**(M-2)*(n-1) + n**(M-3)*(n-1)**2 + ... + (n-1)**(M-1))/N**M
#
#11  1*1*1 = 1
#12  1*1*1 + 1*1*1 + 1*1*1 = 3
#13  1*1*1 + 1*1*1 + 1*1*1 = 3
#14  1*1*1 + 1*1*1 + 1*1*1 = 3
#22  1*1*2 + 1*1*1 + 1*1*1 = 4
#23  1*1*2 + 1*2*1 + 2*1*1 + 1*1*1 + 1*1*1 + 1*1*1 = 9
#24  1*1*2 + 1*2*1 + 2*1*1 + 1*1*1 + 1*1*1 + 1*1*1 = 9
#33  1*1*3 + 1*1*2 + 1*1*2 = 7
#34  1*1*3 + 1*3*1 + 3*1*1 + 1*1*2 + 1*2*1 + 2*1*1 = 15
#44  1*1*4 + 1*1*3 + 1*1*3 = 10
#probability for nm result, of which there are 10 for 3d4k2 = 4+3+2+1 nCr?

## reroll probabilities
#1d6r1 =>
#1 (1/6) =>  1 (1/6)
#            2 (1/6)
#            3 (1/6)
#            4 (1/6)
#            5 (1/6)
#            6 (1/6)
#2 (1/6 + 1/36)
#3 ...
#4 ...
#5 ...
#6 ...
## for one die and one reroll number
#if result == rerollD[indS]:
#    prob = 1/(typeD[indS]**numD[indS])
#else:
#    prob = (typeD[indS] + 1)/(typeD[indS]**numD[indS])
#1d6r1r2
#1 (1/6) =>  1 (1/6)
#            2 (1/6)
#            3 (1/6)
#            4 (1/6)
#            5 (1/6)
#            6 (1/6)
#2 (1/6) =>  1 (1/6)
#            2 (1/6)
#            3 (1/6)
#            4 (1/6)
#            5 (1/6)
#            6 (1/6)
#3 (1/6)
#...
#1 (2/36)
#2 (2/36)
#3 (8/36)
