from graphs_functions import *




def closenessCentrality(n, g, option = 1):
    
    if(option==1):
        new_G, dist, _ = dijkstra(n, g)

        dist.pop(n)

        return sum((len(new_G)-1)/np.array([el for el in dist.values()]))
    
    elif(option==2):
        new_G, dist, _ = dijkstra(n, g)

        dist.pop(n)

        dist = {key:val for key, val in dist.items() if val != float("inf")}

        return (len(dist))/sum(np.array([el for el in dist.values()]))
    
    else:
        print("This option does not exist!")
        return None
    
    
    
def degreeCentrality(n, g):
    
    in_degree = 0
    out_degree = 0
    
    for edge in g.nodes[n]:
        if(edge.from_n == n):
            out_degree += 1
        if(edge.to_n == n):
            in_degree += 1
            
    return out_degree, in_degree
   
    
    
    
def betweeness(n, G):
    
    betweeness = 0
    
    for s in G.nodes:

        new_G, _, sigma = dijkstra(s, G)
        
        if(s != n and sum(sigma.values()) - 1 != 0):
            betweeness += sigma[n]/(sum(sigma.values()) - 1)
        
    return betweeness

