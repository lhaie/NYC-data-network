import gzip
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing
#import getData
import route as r
#import node
from datetime import date, time, datetime
import time


#Creation of the map

longimax = -73.5
longimin = -74.5
latimax = 41.5
latimin = 40.5
intervalle_longitude = [longimin, longimax]
intervalle_latitude = [latimin, latimax]

EW = abs(intervalle_longitude[0]-intervalle_longitude[1])
# 0.443 degree from east to west
# 1 degree at 40 degree latitude equals to 85.26 km
# So we have 37.8 km from east to west
NS = abs(intervalle_latitude[0]-intervalle_latitude [1])
# 0.307 degree from north to south
# 1 degree equals 111.2 km
# so we have 34.2 km from north to south

#Let's say we want to make that one node represents an area of 100 m²

EW_axis = []
NS_axis = []
EW_nb = int(85.3/0.1)
NS_nb = int(111.2/0.1)

for j in range(EW_nb):
    EW_axis += [longimin + j*(EW/EW_nb)]

for i in range(NS_nb):
    NS_axis += [latimin + i*(NS/NS_nb)]

#Generating the nodes
G = nx.Graph()
DG = nx.DiGraph()
#nodes = []
k = 0
for long in EW_axis :
    for lat in NS_axis :
        #nodes += [(long,lat)]
        G.add_node(k, longitude = long, latitude = lat)
        DG.add_node(k, longitude = long, latitude = lat)
        k += 1

#Generatig the edges
names_line = True
u = 0
t0 = time.time()
with gzip.open("yellow_tripdata_2015-01-06.csv.gz","rb") as f :
    for line in f :
        if names_line:
            #names = list_of_string(line.decode(), ',')
            names = line.decode().split()
            names = names[0].split(",")
            print(type(names))
            print(names)
            names_line = False
 #           for l in names :
#                print(l)
        else :
            u += 1
            #line = list_of_string(line.decode(), ',')
            line = line.decode().split(",")
            line[-1] = line[-1].split()[0]
            #type(line)
            #print(line)
            print(u)
            trip = dict()
            for i in range(len(names)):
                trip[names[i]] = line[i]


            indiv = r.Route(trip)
            
            pick_long = 0
            drop_long = 0
    
            if EW_axis[len(EW_axis)-1] <= indiv.pickup_longitude:
                pick_long = len(EW_axis)-1
            if EW_axis[len(EW_axis)-1] <= indiv.dropoff_longitude:
                drop_long = len(EW_axis)-1
    
            if pick_long == 0 or drop_long == 0 :
                for i in range(len(EW_axis)-1):
                    if (EW_axis[i] <= indiv.pickup_longitude and indiv.pickup_longitude < EW_axis[i+1]):
                        pick_long = i
                    if (EW_axis[i] <= indiv.dropoff_longitude and indiv.dropoff_longitude < EW_axis[i+1]):
                        drop_long = i

           
            pick_lat = 0
            drop_lat = 0
    
            if NS_axis[len(NS_axis)-1] <= indiv.pickup_latitude:
                pick_lat = len(NS_axis)-1
            if NS_axis[len(NS_axis)-1] <= indiv.dropoff_latitude:
                drop_lat = len(NS_axis)-1
    
            if pick_lat == 0 or drop_lat == 0 :
                for i in range(len(NS_axis)-1):
                    if (NS_axis[i] <= indiv.pickup_latitude and indiv.pickup_latitude < NS_axis[i+1]):
                        pick_lat = i
                    if (NS_axis[i] <= indiv.dropoff_latitude and indiv.dropoff_latitude < NS_axis[i+1]):
                        drop_lat = i
    
            pickup_node = pick_long * NS_nb + pick_lat
            dropoff_node = drop_long * NS_nb + drop_lat
    
    #Undirected Graph
            if (pickup_node,dropoff_node) in G.edges :
                G.edges[(pickup_node, dropoff_node)]['trips'] += 1
                G.edges[(pickup_node, dropoff_node)]['passengers'] += indiv.passenger_count
                G.edges[(pickup_node, dropoff_node)]['total_amount'] += indiv.total_amount
                G.edges[(pickup_node, dropoff_node)]['distance'] += indiv.trip_distance
    
            else :
                G.add_edge(pickup_node, dropoff_node, trips = 1, 
                           passengers = indiv.passenger_count, 
                           total_amount = indiv.total_amount,
                           distance = indiv.trip_distance)
    
    #Directed Graph
            if (pickup_node,dropoff_node) in DG.edges :
                DG.edges[(pickup_node, dropoff_node)]['trips'] += 1
                DG.edges[(pickup_node, dropoff_node)]['passengers'] += indiv.passenger_count
                DG.edges[(pickup_node, dropoff_node)]['total_amount'] += indiv.total_amount
                DG.edges[(pickup_node, dropoff_node)]['distance'] += indiv.trip_distance
    
            else :
                DG.add_edge(pickup_node, dropoff_node, trips = 1, 
                            passengers = indiv.passenger_count, 
                            total_amount = indiv.total_amount,
                            distance = indiv.trip_distance)

tf = time.time()
duree = tf-t0
print('duree : ', duree, ' secondes')



n = G.number_of_nodes()
p = G.number_of_edges()


#Removing unused nodes
for node in range(n) :
    if G.degree(node) == 0:
        G.remove_node(node)
    if DG.degree(node) == 0:
        DG.remove_node(node)

n = G.number_of_nodes()
p = G.number_of_edges()
dn = DG.number_of_nodes()
dp = DG.number_of_edges()

degrees = list(d for n,d in G.degree())
Ddegrees = list(d for n,d in DG.degree())

indegrees = list(d for n,d in DG.in_degree())
outdegrees = list(d for n,d in DG.out_degree())
DG.in_edges()

#Loaction of node n in longitude and latitude coordinates
def location(G,node):
    if node in G.nodes :
        long = G.nodes[node]['longitude']
        lat = G.nodes[node]['latitude']
    else:
        long = 0
        lat = 0
    return(long,lat)


positions = dict()
for node in G.nodes :
    positions[node] = location(G,node)

#nx.draw_networkx(G, pos = positions, with_labels = True, ax = True, node_size = 100, node_color = "y", cmap = True, edge_color = "b", edge_cmap = True)

nx.draw_networkx(G, pos = positions, with_labels = False, node_size = 30, node_color = "r", cmap = False, edge_color = "y", edge_cmap = True)


""" Degree centrality """
plt.hist(degrees)

degree_centrality = []
for node in G.nodes:
    degree_centrality += [nx.degree_centrality(G)[node]]
plt.hist(degree_centrality)


""" Connected components """
connected_comp_lengths = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
connected_comp = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
plt.hist(connected_comp_lengths)

connected_comp_lengths_2 = []
m = min(connected_comp_lengths)    
for k in connected_comp_lengths:
    if k > 5 :
        connected_comp_lengths_2 += [k]
plt.hist(connected_comp_lengths_2)

nx.average_clustering(G, weight = 'trips')

nx.clustering(G)


""" 2D degrees repartition """

Deg = np.zeros((len(NS_axis),len(EW_axis)))
k = 0
for j in range(len(EW_axis)) :
    for i in range(len(NS_axis)) :
        k += 1
        if k in G.nodes :
            Deg[i][j] = G.degree(k)

N_limit = 0
N_found = False
S_limit = len(NS_axis)
S_found = False
E_limit = len(EW_axis)
E_found = False
W_limit = 0
W_found = False

for i in range(10,len(NS_axis)-1):
    for j in range(10,len(EW_axis)-1):
        if not(N_found):
            if Deg[i][j] != 0 :
                N_limit = i
                N_found = True
        if not(S_found):
            if Deg[len(NS_axis)-1-i][j] != 0 :
                S_limit = len(NS_axis)-1-i
                S_found = True

for j in range(10,len(EW_axis)-1):
    for i in range(10,len(NS_axis)-1):
        if not(W_found):
            if Deg[i][j] != 0 :
                W_limit = j
                W_found = True
        if not(E_found):
            if Deg[i][len(EW_axis)-1-j] != 0 :
                E_limit = len(EW_axis)-1-j
                E_found = True


plt.imshow(Deg)
Degree_matrix = Deg[N_limit:S_limit+1][W_limit:E_limit+1]
plt.imshow(Degree_matrix)

Degree_mat = Degree_matrix[150:600][150:600]
plt.imshow(Degree_mat)

matrice_deg = Deg[150:400]
plt.imshow(matrice_deg)
matrice_deg2 = np.transpose(np.transpose(matrice_deg)[400:550])
plt.imshow(matrice_deg2)
plt.matshow(matrice_deg2)





