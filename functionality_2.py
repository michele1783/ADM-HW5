from graphs_functions import *




def closenessCentrality(n, g, option = 1):
    
    n = g.get_node(n)
    
    if(option==1):
        new_G, dist, _ = dijkstra(n.value, g)

        dist.pop(n.value)

        return sum((len(new_G)-1)/np.array([el for el in dist.values()]))
    
    elif(option==2):
        new_G, dist, _ = dijkstra(n.value, g)

        dist.pop(n.value)

        dist = {key:val for key, val in dist.items() if val != float("inf")}

        return (len(dist))/sum(np.array([el for el in dist.values()]))
    
    else:
        print("This option does not exist!")
        return None
    
    
    
def degreeCentrality(n, g):
    
    n = g.get_node(n)
    
    in_degree = 0
    out_degree = 0
    
    for edge in g.nodes[n]:
        if(edge.from_n == n):
            out_degree += 1
        if(edge.to_n == n):
            in_degree += 1
            
    return out_degree, in_degree
   
    
    
    
def betweeness(n, G):
    
    n = G.get_node(n)
    
    betweeness = 0
    
    for s in G.nodes:

        new_G, _, sigma = dijkstra(s.value, G)
        
        if(s != n and sum(sigma.values()) - 1 != 0):
            betweeness += sigma[n.value]/(sum(sigma.values()) - 1)
        
    return betweeness


def PageRank_one_iter(graph, d):
    
    for node in graph.nodes:
        update_pagerank(node, graph, d, len(graph))
        
        

def update_pagerank(node, g, d, n):
    in_neighbors = [edge.from_n for edge in g.nodes[node] if edge.from_n != node.value]
    pagerank_sum = sum((node.pageRank / degreeCentrality(node.value,g)[0]) for node in in_neighbors)
    random_walk = d / n
    node.pageRank = random_walk + (1-d) * pagerank_sum

    
    
def functionality_2(n, start_time, end_time, metric = 1, num_sim = 100):
    
    data = totDataframe[totDataframe.time.between(start_time, end_time)]
    
    data_g = make_graph(data)
    
    if(data_g.get_node(n) != None):

        if(metric == "1"):
            return betweeness(n, data_g)

        elif(metric == "2"):

            for _ in range(num_sim):
                PageRank_one_iter(data_g, 0.85)

            return [el.pageRank for el in data_g.nodes if el.value == n][0]

        elif(metric == "3"):
            return closenessCentrality(n, data_g, option = 1)

        elif(metric == "4"):
            return degreeCentrality(n, data_g)[0]

        else:
            print("No metrics required.")
            return None
    else:
        return "NA"




def functionality_2_visual():
    
    metrics = {1:"Betweeness Centrality", 2:"PageRank", 3:"Closeness Centrality", 4:"Degree Centrality"}
    
    print("FUNCTIONALITY 2:")
    
    start_time = input("Insert start time: ")
    end_time = input("Insert end time: ")
    n = int(input("Insert node: "))
    
    print("Choose the metrix:\n\n1:Betweeness Centrality\n2:PageRank\n3:Closeness Centrality\n4:Degree Centrality")
    metric = input("metric number: ")
    
    
    data = totDataframe[totDataframe.time.between(start_time, end_time)]
    
    data_g = make_graph(data)

    node = data_g.get_node(n)
    
    neighbours = [neighbour for neighbour in data_g.nodes[node]]
    
    out_g = GRAPH(edges=neighbours)
    
    out_g.print_graph(pos="planar", highlight=True, highlighted_node=n, size=(20,20))
    
    
    out = []
    time_intervals = pd.date_range(start_time, end_time, freq="H")
    
    for i in tqdm(range(1,len(time_intervals))):
      
        out.append(functionality_2(n, time_intervals[i-1], time_intervals[i], metric = metric))
        
    
    #Plotting the results
    plt.rcParams['axes.facecolor'] = 'lightgray'
    
    fig, ax = plt.subplots(1,1, figsize=(15,10))
    
    out = [el for el in out if el != "NA"]

    ax.plot(range(0,len(out)), out, linewidth = 4, ls = "--", marker="o", markersize = 15, markerfacecolor = "k", color = "gold")
    ax.set_ylabel(metrics[int(metric)], size = 25)
    ax.set_xlabel("intervals of times where the node exist",size = 25)
    ax.grid(color="w")

    return out