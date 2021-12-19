#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 08:18:59 2021

@author: michele
"""

def dormitory(n, k): 
    #input:
    #n: list of n kids
    #k: list of k tuples
    
    #output:
    #dorm_1: list of kids that sleep in first dormitory
    #dorm_2: list of kids that sleep in second dormitory
    
    dorm_1 = [] #list of kids in first dormitory
    dorm_2 = [] #list of kids in second dormitory
    visited = [] #list of kids already settled
    
    for i in k: 
        
        if i[0] > i[1]: #check if the pairs in k are ordered
            i = list(i) #if not I order them
            t = i[0]
            i[0] = i[1]
            i[1] = t
            i = tuple(i) # now I have a sorted tuple 
        
        #if first kid is not already settled
        if visited.count(i[0]) == 0: 
            
            if dorm_1.count(i[1]) == 0: #if the second kid of the couple is not in dormitory 1
                
                dorm_1.append(i[0]) #I add first kid to first dormitory

            else:
                dorm_2.append(i[0]) #I add first kid to first dormitory
                
            visited.append(i[0]) #I flag this kid as visited
            
         #if second kid is not already settled
        if visited.count(i[1]) == 0: 
            
            if dorm_2.count(i[0]) == 0: #if the first kid of the couple is not in dormitory 2
                
                dorm_2.append(i[1]) #I add second kid to second dormitory
                
            else:
                
                dorm_1.append(i[1]) #I add second kid to first dormitory
                
            visited.append(i[1]) #I flag this kid as visited 

            
    for i in n: 
        
        if (dorm_1.count(i) == 0) & (dorm_2.count(i) == 0): #add all the kids that are not in k tuples
            dorm_1.append(i)
    c = 0 
    
    for i in k: #check if a couple is in the same dormitory
        
        if ((dorm_1.count(i[0]) != 0) & (dorm_1.count(i[1]) != 0)) \
        | ((dorm_2.count(i[0]) != 0) & (dorm_2.count(i[1]) != 0)):
            
            c += 1
            
    if c != 0: #there are not possible combination
        
        print("no combination")
        
    else:
        
        print("In first dormitory there are the following kids: " + str(dorm_1))
        print("In second dormitory there are the following kids: " + str(dorm_2))