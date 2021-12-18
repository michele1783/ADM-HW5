#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 15:58:21 2021

@author: michele
"""
import pandas as pd
import numpy as np
from datetime import *
import networkx as nx
import networkx.drawing
from collections import *
from tqdm.notebook import tqdm
from multiprocessing.dummy import Pool
import multiprocessing
import matplotlib.pyplot as plt
import pickle
from general_functions import *
from graphs_functions import *
from test_data import *



def shortest_ordered_route(p, p_start, p_end, g):
    
    #add to the starting and the final node to ordered list of p
    p.append(p_end)
    p.insert(0, p_start)
    
    #list of the edges of the shortest ordered route
    final_path = []
    for i in tqdm(range(0, len(p)-1)):
        
        #compute dijkstra from the i-th node
        new_g, dist, _ = dijkstra(p[i], g)
        
        #retrieve the node p[i] and p[i+1] from the new graph computed by dijkstra
        node_new = new_g.get_node(p[i])
        next_node_new = new_g.get_node(p[i+1])
        
        
        #check if they are connected directly the two consecutive nodes
        if(new_g.is_linked_from(node_new, next_node_new)):
            
            #if yes we append the edge to the final path
            final_path.append(g.get_edge(node_new, next_node_new))
            
        else:
            temp = []
            
            #we make a try because is possible that graph is disconnected 
            try:
                #from edges of new node we look ones that not starts from our new next node
                prec = [el for el in new_g.nodes[next_node_new] if el.from_n != next_node_new][0]
            except IndexError:
                return ("Not possible")
                break
            
            #we append the edge in a temporary list  
            temp.append(g.get_edge(prec.from_n, prec.to_n))
            
            #we have started from the end, we continue until we arrive at the current edge
            while(not prec.from_n == node_new):
                
                #edge that points to the previous node
                punt = [el for el in new_g.nodes[prec.from_n] if el.from_n != prec.from_n][0]

                prec = punt
                
                #we append the edge from the last node to the previous one
                temp.append(g.get_edge(punt.from_n, punt.to_n))

            #we reverse the list because we have started from the end
            temp.reverse()
            
            #we extend our list 
            final_path.extend(temp)
            
    #create the graph for visualization
    out_graph = GRAPH()
    
    #add edges to the graph
    for edge in final_path:
        out_graph.add_edge_object(edge)
    
    #compute the length of the path summing all the weigth of edges of the path
    lunghezza = sum([edge.w for edge in final_path])
    
    return out_graph, final_path, lunghezza



def func_3():
    
    
    p = list(map(int,input("Insert list of user: ").split()))
    
    p_start = int(input("Insert the starting user: "))
    
    p_end = int(input("Insert the final user: "))
    
    #we filter the dataset with a given interval of time
    #data = data[data.time.between(time_start,time_end)]
    
    #from dataframe to graph
    #g = make_graph(totDataframe_2y)
    
    #compute the shortest ordered route
    #return the out_graph for the visualization
    #lunghezza is the length of the final path
    #final path is a list of edges of the route
    return shortest_ordered_route(p, p_start, p_end, totDataframe_2y_g)