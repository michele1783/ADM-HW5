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


class EDGE:
    
    def __init__(self, from_n, to_n, time, w):
        self.from_n = from_n
        self.to_n = to_n
        self.w = w
        self.time = time
        
    def __repr__(self):
        return f"{self.from_n.value} -> {self.to_n.value} ::::: weight = {self.w} ::::: time: {self.time}"
    
class NODE:
    def __init__(self, value):
        self.value = value
        self.pageRank = 1.0
        

class GRAPH:
    
    def __init__(self, nodes = [], edges = []):
        self.nodes = defaultdict(list, {k:[] for k in nodes})
        
        if(len(edges)>0):
            for edge in tqdm(edges):
                self.nodes[edge.from_n].append(edge)
                self.nodes[edge.to_n].append(edge)
        
        self.num_nodes = len(nodes)
        self.num_edges = len(edges)
        self.visited = []
        
    def add_node(self, node):
        self.nodes[node] = self.nodes.get(node, [])
        
    def get_node(self, value):
        
        out_node = [node for node in self.nodes if node.value == value]
        
        if(len(out_node)>0):
            return out_node[0]
        else:
            return None
        
    def add_edge(self, from_n, to_n, time, w):
        e = EDGE(from_n, to_n, time, w)
        
        self.nodes[from_n].append(e)
        self.nodes[to_n].append(e)
        
    def add_edge_object(self, edge):
        
        self.nodes[edge.from_n].append(edge)
        self.nodes[edge.to_n].append(edge)
        
    def add_edge_object_list(self, edges):
        
        for edge in edges:
            self.nodes[edge.from_n].append(edge)
            self.nodes[edge.to_n].append(edge)
            
    def get_edge(self, from_n, to_n):
        out_edge = None
        for edge in self.nodes[from_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                out_edge = edge
        return out_edge
    
    def delete_edge(self, from_n, to_n):
        for edge in self.nodes[from_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                self.nodes[from_n].remove(edge)
                
        for edge in self.nodes[to_n]:
            if(edge.from_n == from_n and edge.to_n == to_n):
                self.nodes[to_n].remove(edge)
                
    def delete_all_edge_of_node(self, node):
        for edge in self.nodes[node]:
    
            if(edge.to_n != node):
                self.nodes[edge.to_n].remove(edge)
                
             
            else:
                self.nodes[edge.from_n].remove(edge)
        
        self.nodes[node] = []
             
                
            
            
    def is_linked_from(self, node_a, node_b):
        return node_a in [n.from_n for n in self.nodes[node_b]]
    
    def is_linked_to(self, node_a, node_b):
        return node_a in [n.to_n for n in self.nodes[node_b]]
    
    def is_visited(self, node):
        return node in self.visited
            
    def clear_graph_path(self):
        self.visited = []
        
    def print_graph(self, size = (7,7), pos = "random", highlight = False, highlighted_node = None):
        G = nx.DiGraph()
        for k in self.nodes:
            G.add_weighted_edges_from([(el.from_n.value, el.to_n.value, el.w) for el in self.nodes[k]])
        
        
        
        plt.figure(figsize=size) 
        pos = eval(graph_layout(pos)) 
        
        nx.draw(G, pos, with_labels=True, font_weight='bold')
         
        labels = nx.get_edge_attributes(G, name="weight")
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels);
        
        if(highlight):
            nx.draw_networkx_nodes(G, pos, nodelist=[highlighted_node], node_color="red")
        
        plt.savefig("data/test.pdf")
        plt.show()
        return G
        
    
    def __repr__(self):
        return f"{self.nodes}"
    
    def __len__(self):
        return len(self.nodes)

    
    
def make_graph(data):
    nodes = {el:NODE(el) for el in pd.concat([data["user_a"], data["user_b"]], axis = 0).drop_duplicates().array}
    
    g = GRAPH()
    with Pool(multiprocessing.cpu_count()) as pool:

        with tqdm(total = len(data), disable = True) as pbar:
            for el in pool.imap_unordered(lambda row: EDGE(nodes[row[1]["user_a"]],nodes[row[1]["user_b"]],row[1]["time"],row[1]["weights"]), data.iterrows()):
                g.add_edge_object(el)
                pbar.update()
                
    #save_object(g_a2q, "data/g_a2q.pkl")
    return g

def graph_layout(style = "random"):
    
    if(style == "circular"):
        layout = "nx.circular_layout(G)"
    
    elif(style == "planar"):
        layout = "nx.planar_layout(G)"
    
    elif(style == "shell"):
        layout = "nx.shell_layout(G)"
    
    elif(style == "multipartite"):
        layout = "nx.multipartite_layout(G)"
    
    elif(style == "random"):
        layout = "nx.random_layout(G)"
        
    else:
        raise(KeyError("Not valid layout"))
        return None
        
    return layout


def dijkstra(n, g, print_g = False, size=(7,7), style = "random"):
    g.clear_graph_path()
    
    new_G = GRAPH()
    dist = defaultdict(float, {k.value:float('inf') for k in g.nodes})
    dist[n] = 0 
    
    sigma = dict.fromkeys([k.value for k in g.nodes], 0)
    sigma[n] = 1
    #new_G.add_node(n)
    
    for i in range(len(g)):  

        current_node = min([(dist[el.value], el) for el in g.nodes if not g.is_visited(el)], key=lambda e: e[0])[1]
        g.visited.append(current_node)
        
        
        if(dist[current_node.value] == float("inf")):
            break
        
        prec = [el.from_n for el in new_G.nodes[current_node] if el.from_n != current_node]
        
        if(len(prec) != 0):
            sigma[current_node.value] += sigma[prec[0].value]
        
        for neighbour in [el.to_n for el in g.nodes[current_node] if el.from_n == current_node]:

            alt = dist[current_node.value] + g.get_edge(current_node, neighbour).w
            
            if(alt < dist[neighbour.value] and not neighbour in g.visited):
                dist[neighbour.value] = alt
                sigma[neighbour.value] = 0
                
                try:
                    new_G.delete_all_edge_of_node(neighbour)
                except:
                    pass
                
                new_G.add_edge(current_node, neighbour, g.get_edge(current_node,neighbour).time, alt)
                
            elif(alt == dist[neighbour.value]):
                sigma[neighbour.value] += sigma[current_node.value]
                
                
                
                
    g.clear_graph_path()
    
    if(print_g):
        new_G.print_graph(size=size, pos=style)
        
    return new_G, dist, sigma
                
                
                
                
    g.clear_graph_path()
    
    if(print_g):
        new_G.print_graph(size=size, pos=style)
        
    return new_G, dist, sigma