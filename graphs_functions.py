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
        return f"{self.from_n.value} -> {self.to_n.value} ::::: weight = {self.w} ::::: time: {self.time}"
    
class NODE:
    def __init__(self, value):
        self.value = value
        self.pageRank = 1.0
        

#class
class GRAPH:
    
    def __init__(self, nodes = [], edges = []):
        #input:
        #nodes: list of nodes
        #edges: list of edges
        
        self.nodes = defaultdict(list, {k:[] for k in nodes})
        #initialization of dictionary where the keys are the nodes and the values are the edges
        
        #if in our graph there are edges
        if(len(edges)>0):
            for edge in tqdm(edges):
                
                #in the dictionary we add an edge to its starting node and to its end node
                self.nodes[edge.from_n].append(edge)
                self.nodes[edge.to_n].append(edge)
        
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
        
        #in the dictionary we add this new edge to its starting node and to its end node
        self.nodes[from_n].append(e)
        self.nodes[to_n].append(e)
        
        self.num_edges += 1
        
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
        
        
    def print_graph(self, size = (7,7), pos = "random", highlight = False, highlighted_node = None):
        
        #through this function we can visualize our graph
        #we have used networkx but for visualization is allowed
        
        G = nx.DiGraph()
        
        #for each node we add all its edges
        for k in self.nodes:
            G.add_weighted_edges_from([(el.from_n.value, el.to_n.value, el.w) for el in self.nodes[k]])
        
        
        
        plt.figure(figsize=size) 
        pos = eval(graph_layout(pos)) 
        
        nx.draw(G, pos, with_labels=True, font_weight='bold')
        
        #the label of an edge is its weight
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
