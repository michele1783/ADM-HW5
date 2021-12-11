#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 19:43:33 2021

@author: michele
"""

import pandas as pd
import numpy as np
from datetime import *
import networkx as nx
from collections import *

class EDGE:
    
    def __init__(self, from_n, to_n, time, w):
        self.from_n = from_n
        self.to_n = to_n
        self.w = w
        self.time = time
        
    def __repr__(self):
        return f"{self.from_n} -> {self.to_n} ::::: weight = {self.w} ::::: time: {self.time}"

class GRAPH:
    
    def __init__(self, nodes = [], edges = []):
        self.nodes = defaultdict(list, {k:[] for k in nodes})
        
        if(len(edges)>0):
            for edge in edges:
                self.nodes[edge.from_n].append(edge)
                self.nodes[edge.to_n].append(edge)
        
        self.num_nodes = len(nodes)
        self.num_edges = len(edges)
        
    def add_edge(self, from_n, to_n, w, time):
        e = EDGE(from_n, to_n, w, time)
        
        self.nodes[from_n].append(e)
        self.nodes[to_n].append(e)

    def __repr__(self):
        return f"{self.nodes}"

def functionality_1(df):
    #input: one of three starting dataframe
    #output: all the requested values from functionality 1
    
    #array of nodes of graph df
    #concatenate two column of user and pick the unique values.
    #it's a pandas array
    nodi_grafo = pd.concat([df["user_a"], df["user_b"]], axis = 0).drop_duplicates().array
    
    #list of edges 
    edge_grafo = []
    
    #read each row of the dataframe
    for i in range(len(df)): 
        
        #exploit the class edge to create them
        edge_grafo.append(EDGE(df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]))
    
    #creation of the graph df
    df_graph = GRAPH(nodi_grafo, edge_grafo)
    
    #Number of users
    num_node = df_graph.num_nodes
    
    #Number of answers
    num_edge = df_graph.num_edges
    
    #in an undirected graph the number of starting nodes is the same of the ending nodes!!
    #If for all couple of nodes edges are like (source node, destination node)
    #and (destination node, source node) that graph is undirected!

    if len(set(list(df["user_a"]))) == len(set(list(df["user_b"]))): 
        direct = "undirected"
    else:
        direct = "directed"
        
    #Average number of links per user
    #the result presents above include in_degree and out_degree of a graph. 
    media = num_edge / num_node
    
    #The degree density of a directed graph is : D = |E| / (|V| * (|V| - 1))
    D = (num_edge) / (num_node * (num_node - 1))
    
    return num_node, num_edge, direct, media, D
