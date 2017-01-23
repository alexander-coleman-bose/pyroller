# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:28:14 2017

@author: lordmailman
"""

from math import floor
from random import randint
import re
import numpy as np

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
    
    for ind in range(numD):
        tmp = randint(1,typeD)
        if tmp == rerollD:
            tmp = randint(1,typeD)
        tmp = tmp
        
        rolls.append(tmp)
    
    if keepLow>0:
        for ind in range(numD-keepLow):
            rolls.pop(rolls.index(max(rolls)))
            
    if keepHigh>0:
        for ind in range(numD-keepHigh):
            rolls.pop(rolls.index(min(rolls)))
            
    return sum(rolls) + modD
    
#def rollInfo(numD = 1,typeD = 20,modD = 0,keepLow = 0,keepHigh = 0,rerollD = 0):
def rollInfo(varargin_clean = "1d20"):
    
    def ss(numD):
        tmp = 0;
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
    
    numD = list()
    typeD = list()
    modD = list()
    keepLow = list()
    keepHigh = list()
    rerollD = list()
    negD = list()
    
    dic = {}
    dic['roll'] = varargin_clean
    dic['min'] = 0
    dic['max'] = 0
    dic['val'] = 0
    dic['results'] = 0
    dic['keys'] = 0
#    dic['results_all'] = 0
    dic['avg'] = 0
    dic['critHit'] = 0
    dic['critMiss'] = 0
    
    results = list()
    keys = list()
#    results_all = list()
    
    for indS in range(len(splits)):
        # parse for numD
        tmp = splits[indS].split('d')
        if len(tmp) > 2:
            raise RuntimeError("You cannot use 'd' twice in the same die split string.")
        elif len(tmp) < 2:
            # if there isn't a 'd', then assume that the only value is modD
            numD.append(0)
            typeD.append(0)
            modD.append(int(tmp[0]))
            keepLow.append(0)
            keepHigh.append(0)
            rerollD.append(0)
        else:
            # if there is a 'd', pop it, then re.search for the other values
            numD.append(int(tmp.pop(0)))
            modD.append(0)
            
            tmp2 = re.search(r'^(\d*)',tmp[0])
            if tmp2:
                typeD.append(int(tmp2.group().strip('d')))
            else:
                typeD.append(0)
            
            tmp2 = re.search(r'k(\d*)',tmp[0])
            if tmp2:
                keepLow.append(int(tmp2.group().strip('k')))
            else:
                keepLow.append(0)
                
            tmp2 = re.search(r'K(\d*)',tmp[0])
            if tmp2:
                keepHigh.append(int(tmp2.group().strip('K')))
            else:
                keepHigh.append(0)
            
            tmp2 = re.search(r'r(\d*)',tmp[0])
            if tmp2:
                rerollD.append(int(tmp2.group().strip('r')))
            else:
                rerollD.append(0)

        if keepLow[indS] and keepHigh[indS]:
            raise RuntimeError("You can keep the lowest or the highest rolls, not both.")
        elif keepLow[indS]<0 or (keepLow[indS]>=numD[indS] and keepLow[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
        elif keepHigh[indS]<0 or (keepHigh[indS]>=numD[indS] and keepHigh[indS]):
            raise RuntimeError("You must keep a positive number of dice, but less than you roll.")
        elif rerollD[indS]<0 or rerollD[indS]>typeD[indS]:
            raise RuntimeError("You cannot reroll numbers higher than the die has.")
    
        if rerollD[indS]>0:
            print('Warning: rerolls are not supported by rollInfo')
            
        if numD[indS]<0:
            negD.append(1)
            numD[indS] = -1*numD[indS]
        else:
            negD.append(0)
        
        #debug
#        print(indS)
#        print(numD)
#        print(typeD)
#        print(keepLow)
#        print(keepHigh)
#        print(modD)
#        print(rerollD)
#        print(negD)
        
    # establish the minimum and maximum values for this roll
        thisMin = ((-1)**negD[indS])*(numD[indS]-keepLow[indS]-keepHigh[indS])*(typeD[indS]**negD[indS]) + modD[indS]
        thisMax = ((-1)**negD[indS])*(numD[indS]-keepLow[indS]-keepHigh[indS])*(typeD[indS]**(1-negD[indS])) + modD[indS]
        
    # generate an actual rolled value for the die roll
        rolls = list()
        tmp = 0
        
        for indN in range(numD[indS]):
            tmp = randint(1,typeD[indS])
            if tmp == rerollD[indS]:
                tmp = randint(1,typeD[indS])
            rolls.append(tmp)
        
        if keepLow[indS]>0:
            for indK in range(numD[indS]-keepLow[indS]):
                rolls.pop(rolls.index(max(rolls)))
                
        if keepHigh[indS]>0:
            for indK in range(numD[indS]-keepHigh[indS]):
                rolls.pop(rolls.index(min(rolls)))
                
        dic['val'] = dic['val'] + sum(rolls) + modD[indS]
        
    # compute the probabilities
#        results_all.append({})
        thisResult = [0] * (thisMax-thisMin+1)
        # if an advantage or disadvantage roll
        if numD[indS] == 2 and typeD[indS] == 20 and (keepHigh[indS] == 1 or keepLow[indS] == 1):
            if keepHigh[indS] == 1:
                for indD in range(typeD[indS]):
                    n = indD+1 # ind is 0 through typeD
                    tmp = (2*n-1)/typeD[indS]**numD[indS]
#                    results_all[indS][n] = tmp
                    thisResult[indD] = tmp
                dic['avg'] = dic['avg'] + (2*ss(typeD[indS])-(1+typeD[indS])*(typeD[indS]/2))/typeD[indS]**numD[indS]

            elif keepLow[indS] == 1:
                for indD in range(typeD[indS]):
                    n = indD+1 # ind is 0 through typeD
                    tmp = (2*(21-n)-1)/typeD[indS]**numD[indS]
#                    results_all[indS][n] = tmp
                    thisResult[indD] = tmp
                dic['avg'] = dic['avg'] + (2*ds(typeD[indS])-(1+typeD[indS])*(typeD[indS]/2))/typeD[indS]**numD[indS]
                
            else:
                raise RuntimeError("Unexpected error: keepHigh or keepLow should = 1.")
                
            if dic['critHit'] == 0:          
#                    dic['critHit'] = results_all[indS][20]
#                    dic['critMiss'] = results_all[indS][1]
                dic['critHit'] = thisResult[thisMax-1]
                dic['critMiss'] = thisResult[thisMin-1]
        elif ~keepLow[indS] and ~keepHigh[indS]:
            dic['avg'] = dic['avg'] + numD[indS]*(1+typeD[indS])/2 + modD[indS]
            
            if typeD[indS] == 20 and dic['critHit'] == 0:
                dic['critHit'] = 1/20
                dic['critMiss'] = 1/20
            
#            for indR in range(thisMin,thisMax+1):
#                results_all[indS][indR] = 0
            
            for indR in range(typeD[indS]**numD[indS]):
                n = indR+1
                result = []
                for indN in range(numD[indS]):
                    result.append(floor((indR/(typeD[indS]**indN))%typeD[indS]+1))
                   
                # debug
#                print(results_all)
#                print(sum(result),thisMin,thisMax)
#                print(thisResult)
#                print(modD[indS])
                # may incur floating point errors
                thisResult[sum(result)-thisMin+modD[indS]] = thisResult[sum(result)-thisMin+modD[indS]] + 1
#                results_all[indS][((-1)**negD[indS])*sum(result)+modD[indS]] = results_all[indS][((-1)**negD[indS])*sum(result)+modD[indS]] + 1/(typeD[indS]**numD[indS])
        
            thisResult = [x/(typeD[indS]**numD[indS]) for x in thisResult]
        
        # if results is empty, this is the first split
#        print(results,indS)
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
    
    dic['keys'] = list(range(dic['min'],dic['max']+1))
    dic['results'] = results.tolist()
#    dic['results_all'] = results_all
            
    return dic

def rollWin(dic,target = 15):
    # gives the probability that a given roll will meet or exceed the target
#    return sum(dic['results_all'][0][k] for k in range(target,max(dic['results_all'][0])+1))
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
        
def rollLose(dic,target = 15):
    # gives the probability that a given roll will fail to meet the target
#    return sum(dic['results_all'][0][k] for k in range(min(dic['results_all'][0]),target))
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
    
def critInfo(dic):
    # gives the probability that a given roll will critically hit or miss
    return (dic['critHit'],dic['critMiss'])

                
                

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