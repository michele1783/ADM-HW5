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


def dateparse(time_as_a_unix_timestamp):
    
    #input:unix time stamp
    #output: date
    #through this function we pass from the unix timestamp  to a readable date
    return pd.to_datetime(time_as_a_unix_timestamp, unit="s").strftime("%Y-%m-%d %H:%M")


class display(object):
    #it is a class that allows to visualize contemporarely more dataframe 
    #it's just for visualization
    
    """Display HTML representation of multiple objects"""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>"""
    def __init__(self, *args):
        self.args = args
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(a, eval(a)._repr_html_())
                         for a in self.args)
    
    def __repr__(self):
        return '\n\n'.join(a + '\n' + repr(eval(a))
                           for a in self.args)

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
        
    def add_edge_object_list(self, edges):
        #through this function instead we add a list of edge object, already created
        #so we do not use the class EDGE, and we can add more edges together
        #in the dictionary we add this edge object to its starting node and to its end node
        for edge in edges:
            self.nodes[edge.from_n].append(edge)
            self.nodes[edge.to_n].append(edge)
            
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
                
         #check the key of end node      
        for edge in self.nodes[to_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                self.nodes[to_n].remove(edge)
                
    def delete_all_edge_of_node(self, node):
        
        #through this function given a node we delete all its edges
        #in the dictionary to its key will not correspond any value
        for edge in self.nodes[node]:
    
            if(edge.to_n != node):
                self.nodes[edge.to_n].remove(edge)
                
             
            else:
                self.nodes[edge.from_n].remove(edge)
        
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
    bin_2 = list(range(20, 101))
    
    #histogram
    plt.hist(degree_1, bins = bin_2, color = "salmon")
    plt.title("Density Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of users with x degree")
    
    #disposition of the subplot
    plt.subplot(223)
    
    #bins in the third subplot
    bin_3 = list(range(100, 501))
    
    #histogram
    plt.hist(degree_1, bins = bin_3, color = "darkgreen")
    plt.title("Density Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of users with x degree")
    
    
    plt.subplot(224)
    
    #bins in the fourth subplot
    bin_4 = list(range(500, max(degree_1)))
    
    #histogram
    plt.hist(degree_1, bins = bin_4, color = "red")
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
    
def make_graph(data):
    nodes = {el:NODE(el) for el in pd.concat([data["user_a"], data["user_b"]], axis = 0).drop_duplicates().array}
    
    g = GRAPH()
    with Pool(multiprocessing.cpu_count()) as pool:

        with tqdm(total = len(data)) as pbar:
            for el in pool.imap_unordered(lambda row: EDGE(nodes[row[1]["user_a"]],nodes[row[1]["user_b"]],row[1]["time"],row[1]["weights"]), data.iterrows()):
                g.add_edge_object(el)
                pbar.update()
                
    #save_object(g_a2q, "data/g_a2q.pkl")
    return g


def dijkstra(n, g, print_g = False, size=(7,7), style = "random"):
    
    #visited list is empty     
    g.clear_graph_path()
    
    new_G = GRAPH()
    
    #dictionary where each node is initialized as infinite
    #keys are nodes
    #values are distances from the starting node
    dist = defaultdict(float, {k.value:float('inf') for k in g.nodes})
    
    #the starting node has distance zero from itself
    dist[n] = 0 
    
    #sigma is the dictionary that has as values the number of shortest path that go through that node
    #keys are the nodes
    #it is useful for functionality 2
    sigma = dict.fromkeys([k.value for k in g.nodes], 0)
    
    #we initialize the first node with 1
    sigma[n] = 1
    #new_G.add_node(n)
    
    
    for i in range(len(g)):  
        
        #if the node is not already visited we compute the minimum distance among the nodes. We take the minimum distance
        #but we are interested to the corresponding node so we take the key. 
        current_node = min([(dist[el.value], el) for el in g.nodes if not g.is_visited(el)], key=lambda e: e[0])[1]
        
        #current node is visited
        g.visited.append(current_node)
        
        #if the minimum distance is infinite we go out from the cycle
        if(dist[current_node.value] == float("inf")):
            break
        
        #precedent nodes: edges that not starts from the current node, but are edges that are values of our node
        prec = [el.from_n for el in new_G.nodes[current_node] if el.from_n != current_node]
        
        #just for the first node that has not precedent nodes
        if(len(prec) != 0):
            
            #we assign to actual node the value of the previous 
            #because shortest path are at least the number of the previous
            sigma[current_node.value] += sigma[prec[0].value]
        
        #between edges of the current node there is one that start from current node we look end nodes of these edges 
        for neighbour in [el.to_n for el in g.nodes[current_node] if el.from_n == current_node]:
            
            #we sum the distance of the current node and the distance of the new edge belong to neighbours
            alt = dist[current_node.value] + g.get_edge(current_node, neighbour).w
            
            #if the new distance computed is less than distance of neighbour 
            #that are not visited we update this distance
            if(alt < dist[neighbour.value] and not neighbour in g.visited):
                
                #we update the distance
                dist[neighbour.value] = alt
                
                #initialize the number of shortest path of node to zero
                sigma[neighbour.value] = 0
                
                try:
                    
                    #we remove edges because we do not know if we have found the minimum distance
                    new_G.delete_all_edge_of_node(neighbour)
                    
                except:
                    pass
                #we add the edge between the current node, the neighbour. The weight is alt 
                new_G.add_edge(current_node, neighbour, g.get_edge(current_node,neighbour).time, alt)
                
            elif(alt == dist[neighbour.value]):
                sigma[neighbour.value] += sigma[current_node.value]
           
                
    g.clear_graph_path()
    
    #print graph
    if(print_g):
        new_G.print_graph(size=size, pos=style)
    
    #we return the new graph, the dictionary with distances and dictionary with shortest paths
    return new_G, dist, sigma

def shortest_ordered_route(p, p_start, p_end, g):
    
    #add to the starting and the final node to ordered list of p
    p.append(p_end)
    p.insert(0, p_start)
    
    #list of the edges of the shortest ordered route
    final_path = []
    for i in range(0, len(p)-1):
        
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



def func_3(data, p, p_start, p_end, time_start, time_end):
    
    #we filter the dataset with a given interval of time
    data = data[data.time.between(time_start,time_end)]
    
    #from dataframe to graph
    g = make_graph(data)
    
    #compute the shortest ordered route
    #return the out_graph for the visualization
    #lunghezza is the length of the final path
    #final path is a list of edges of the route
    return shortest_ordered_route(p, p_start, p_end, g)
