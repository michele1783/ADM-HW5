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


#class
class EDGE:
    
    def __init__(self, from_n, to_n, time, w):
        
        #from_n: starting node
        #to_n: end node
        #time: corresponding time to the edge
        #w: weight of the edge
        
        #we characterize the edge through its start, end, weight and time
        self.from_n = from_n
        self.to_n = to_n
        self.w = w
        self.time = time
        
    def __repr__(self):
        
        #instances of class EDGE return a print that characterize the edge
        return f"{self.from_n} -> {self.to_n} ::::: weight = {self.w} ::::: time: {self.time}"
class GRAPH:
    
    def __init__(self, nodes = [], edges = []):
                #input:
        #nodes: list of nodes
        #edges: list of edges
        self.nodes = defaultdict(list, {k:[] for k in nodes})
        #initialization of dictionary where the keys are the nodes and the values are the edges

        #if in our graph there are edges
        if(len(edges)>0):

        
        #if in our graph there are edges
            for edge in tqdm(edges):
                
                #in the dictionary we add an edge to its starting node and to its end node
                self.nodes[edge.from_n].append(edge)
                self.nodes[edge.to_n].append(edge)
                
        #number of nodes
        self.num_nodes = len(nodes)
        
        #number of edges
        self.num_edges = len(edges)
        self.visited = []
        
    def add_node(self, node):
        #function to add a node in the graph. A new key in the dictionary
        self.nodes[node] = self.nodes.get(node, [])
        
    def get_node(self, value):
        
        out_node = [node for node in self.nodes if node.value == value]
        
        if(len(out_node)>0):
            return out_node[0]
        else:
            return None
        
    def add_edge(self, from_n, to_n, time, w):
        
        #function to add an edge in the graph.
        #using the class EDGE we provide a new edge
        e = EDGE(from_n, to_n, time, w)
        
        self.nodes[from_n].append(e)
        self.nodes[to_n].append(e)
        
    def add_edge_object(self, edge):
                
        #through this function instead we add an edge object, already created
        #so we do not use the class EDGE
        #in the dictionary we add this edge object to its starting node and to its end node
        self.nodes[edge.from_n].append(edge)
        self.nodes[edge.to_n].append(edge)
        self.num_edges += 1
        
        
        
        
        
    def add_edge_object_list(self, edges):
        #through this function instead we add a list of edge object, already created
        #so we do not use the class EDGE, and we can add more edges together
        #in the dictionary we add this edge object to its starting node and to its end node
        for edge in edges:
            self.nodes[edge.from_n].append(edge)
            self.nodes[edge.to_n].append(edge)
            self.num_edges += 1
            
    def get_edge(self, from_n, to_n):
        #through this function given a starting node in input and in output
        #we can retrieve the edge that links the given nodes if it exists
        out_edge = None
        for edge in self.nodes[from_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                out_edge = edge
        return out_edge
    
    def delete_edge(self, from_n, to_n):
        
        #through this function given a starting node in input and in output
        #we can remove the edge that links the given nodes if it exists
        #we have to remove from the dictionary that edge so we have to check
        #two keys, the one of the starting node and the one of the end node 
        
        #check the key of starting node
        for edge in self.nodes[from_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                self.nodes[from_n].remove(edge)
                self.num_edges -= 1
                
         #check the key of end node      
        for edge in self.nodes[to_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                self.nodes[to_n].remove(edge)
                self.num_edges -= 1
                
    def delete_all_edge_of_node(self, node):
        
        #through this function given a node we delete all its edges
        #in the dictionary to its key will not correspond any value
        for edge in self.nodes[node]:
    
            if(edge.to_n != node):
                self.nodes[edge.to_n].remove(edge)
                self.num_edges -= 1
                
             
            else:
                self.nodes[edge.from_n].remove(edge)
                self.num_edges -= 1
        
        self.nodes[node] = []
             
                
            
            
    def is_linked_from(self, node_a, node_b):
        #through this function given two nodes we can retrieve if first node
        #is linked from node b
        return node_a in [n.from_n for n in self.nodes[node_b]]
    
    def is_linked_to(self, node_a, node_b):
        #through this function given two nodes we can retrieve if first node
        #is linked to node b
        return node_a in [n.to_n for n in self.nodes[node_b]]
    
    def is_visited(self, node):
        #check if a node has been visited
        return node in self.visited
            
    def clear_graph_path(self):
        self.visited = []
        
    def print_graph(self, size = (7,7), pos = "random"):
        #through this function we can visualize our graph
        #we have used networkx but for visualization is allowed
        G = nx.DiGraph()
        
        #for each node we add all its edges
        for k in tqdm(self.nodes):
            G.add_weighted_edges_from([(el.from_n.value, el.to_n.value, el.w) for el in self.nodes[k]])
            
        plt.figure(figsize=size)
        
        pos = eval(graph_layout(pos))
        nx.draw(G, pos, with_labels=True, font_weight='bold')
        
        #the label of an edge is its weight
        labels = nx.get_edge_attributes(G, name="weight")
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels);
        plt.savefig("data/test.pdf")
        plt.show()
        return G
        
    
    def __repr__(self):
        return f"{self.nodes}"
    
    def __len__(self):
        return len(self.nodes)


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
        
    if scelta == "c2a":
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
    plt.title("Denisty distribution", fontsize = 20)
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
    
