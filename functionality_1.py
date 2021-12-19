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
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import networkx.drawing
from multiprocessing.dummy import Pool
import multiprocessing
import matplotlib.pyplot as plt
import pickle
from test_data import *
from general_functions import *
from graphs_functions import *



def funz_1():
    scelta = input("What file do you want to analyze?: ")
    
    if scelta == "a2q":
        
        number_nodes_1, number_edges_1, directed_1, mean_1, density_1, sparse_1, degree_1, table_1 = functionality_1(a2q_2y, a2q_2y_g)
        print(tabulate(table_1, headers='firstrow', tablefmt='fancy_grid'))
        print("We want to visualize how many users have a certain degree")
        fig(degree_1)
        print("We want to go deeper in the density distribution")
        fig_hist(degree_1)
        print("We want to visualize for each user how many degree it has")
        fig_plot(degree_1)
        
    elif scelta == "c2a":
        number_nodes_2, number_edges_2, directed_2, mean_2, density_2, sparse_2, degree_2, table_2 = functionality_1(c2a_2y, c2a_2y_g)
        print(tabulate(table_1, headers='firstrow', tablefmt='fancy_grid'))
        print("We want to visualize how many users have a certain degree")
        fig(degree_2)
        print("We want to go deeper in the density distribution")
        fig_hist(degree_2)
        print("We want to visualize for each user how many degree it has")
        fig_plot(degree_2)
        
    else:
        number_nodes_2, number_edges_2, directed_2, mean_2, density_2, sparse_2, degree_2, table_2 = functionality_1(c2q_2y, c2q_2y_g)
        print(tabulate(table_1, headers='firstrow', tablefmt='fancy_grid'))
        print("We want to visualize how many users have a certain degree")
        fig(degree_2)
        print("We want to go deeper in the density distribution")
        fig_hist(degree_2)
        print("We want to visualize for each user how many degree it has")
        fig_plot(degree_2)
    
    
def functionality_1(df, df_graph):
    #input: one of three starting dataframe
    #input: one of three starting graph
    
    #output: all the requested values from functionality 1
    
    #Number of users
    num_node = len(df_graph)
    
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
    
    #A graph is sparse if the cardinality of the set of node is much smaller than 
    #the cardinality of the set of edges
    sparse = "dense"
    if D < 0.01:
        sparse = "sparse"
    
    #for each node in the graph(the keys of dictionary) we look how many edges it has(the values of dictionary)
    #we consider so the sum of the out-degree and the in-degree
    degree = []
    for i in df_graph.nodes.keys():
        degree.append(len(df_graph.nodes[i]))
        
    
    #we print a table with all the information 
    table = [['Info requested', 'Answers'], ['File', df.head()],['Directed or Undirected?', direct], ['N. users', num_node], 
         ['Number of answers/comments',num_edge],['Average n. of links per user',round(media,4)],['Density degree', round(D,4)],
        ['Sparse or Dense?', sparse]]

    
    return num_node, num_edge, direct, media, D, sparse, degree, table

def fig(degree_1):
    
    #input: degree
    #output: unique histogram of degree distribution
    
    #dimension
    plt.figure(figsize=(20,10))
    
    #histogram
    plt.hist(degree_1, bins = 300, color = "darkorange")
    plt.yscale("log")
    plt.title("Density distribution", fontsize = 20)
    plt.xlabel("Degree", fontsize = 12)
    plt.ylabel("Number of users with x degree", fontsize = 12)
    plt.show()



def fig_hist(degree_1):
    #input: degree
    #output: four histograms of the degree distribution
    
    
    #dimension
    f = plt.figure(figsize=(20,10))
    
    #disposition of the subplot
    plt.subplot(221)
    
    #bins in the first subplot
    bin_1 = list(range(1, 21))
    
    #histogram
    plt.hist(degree_1, bins = bin_1, color = "orchid")
    plt.title("Density Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of users with x degree")
    plt.xticks(list(range(1, 20 ,2)))
    
    #disposition of the subplot
    plt.subplot(222)
    
    #bins in the second subplot
    bin_2 = list(range(20, 71))
    
    #histogram
    plt.hist(degree_1, bins = bin_2, color = "salmon")
    plt.title("Density Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of users with x degree")
    
    #disposition of the subplot
    plt.subplot(223)
    
    #bins in the third subplot
    bin_3 = list(range(70, 350))
    
    #histogram
    plt.hist(degree_1, bins = bin_3, color = "darkgreen")
    plt.title("Density Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of users with x degree")
    


def fig_plot(degree_1):
    #input: degree
    #output: plot of degree distribution
    
    #dimension
    plt.figure(figsize=(20,10))
    
    #plot
    plt.plot(degree_1, color = "darkblue")
    plt.title("Degree Distribution", fontsize=20)
    plt.xlabel("Users", fontsize=15)
    plt.ylabel("Degree", fontsize=15)
    plt.show()
    
