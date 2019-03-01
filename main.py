import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing
import getData
import route as r
from datetime import date, time, datetime
import numpy as np

data = getData.get_data_taxis()


#defining the spatial area we will work with
longitudes = []
latitudes = []

for D in data :
    indiv = r.Route_sample(D)
    if indiv.dropoff_longitude != 0 :
        longitudes += [indiv.dropoff_longitude]
    if indiv.pickup_longitude != 0 :
        longitudes += [indiv.pickup_longitude]
    if indiv.dropoff_latitude != 0 :
        latitudes += [indiv.dropoff_latitude]
    if indiv.pickup_latitude != 0 :
        latitudes += [indiv.pickup_latitude]

longimax = max(longitudes)
longimin = min(longitudes)
latimax = max(latitudes)    
latimin = min(latitudes)

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
EW_nb = int(37.8/0.1)
NS_nb = int(34.2/0.1)

for j in range(EW_nb):
    EW_axis += [longimin + j*(EW/EW_nb)]

for i in range(NS_nb):
    NS_axis += [latimin + i*(NS/NS_nb)]

 
#Generating the nodes
H = nx.Graph()
DH = nx.DiGraph()
nodes = []
k = 0

for long in EW_axis :
    for lat in NS_axis :
        nodes += [(long,lat)]
        #nod = (long,lat)
        H.add_node(k, longitude = long, latitude = lat)
        DH.add_node(k, longitude = long, latitude = lat)
        k += 1

#Creating the edges
for D in data :
    indiv = r.Route_sample(D)
    
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
    if (pickup_node,dropoff_node) in H.edges :
        H.edges[(pickup_node, dropoff_node)]['trips'] += 1
        H.edges[(pickup_node, dropoff_node)]['passengers'] += indiv.passenger_count
        H.edges[(pickup_node, dropoff_node)]['total_amount'] += indiv.total_amount
        H.edges[(pickup_node, dropoff_node)]['distance'] += indiv.trip_distance
    
    else :
        H.add_edge(pickup_node, dropoff_node, trips = 1, 
                   passengers = indiv.passenger_count, 
                   total_amount = indiv.total_amount,
                   distance = indiv.trip_distance)
    
    #Directed Graph
    if (pickup_node,dropoff_node) in DH.edges :
        DH.edges[(pickup_node, dropoff_node)]['trips'] += 1
        DH.edges[(pickup_node, dropoff_node)]['passengers'] += indiv.passenger_count
        DH.edges[(pickup_node, dropoff_node)]['total_amount'] += indiv.total_amount
        DH.edges[(pickup_node, dropoff_node)]['distance'] += indiv.trip_distance
    
    else :
        DH.add_edge(pickup_node, dropoff_node, trips = 1, 
                   passengers = indiv.passenger_count, 
                   total_amount = indiv.total_amount,
                   distance = indiv.trip_distance)



n = H.number_of_nodes()
p = H.number_of_edges()


#Removing unused nodes
for node in range(n) :
    if H.degree(node) == 0:
        H.remove_node(node)
    if DH.degree(node) == 0:
        DH.remove_node(node)

n = H.number_of_nodes()
p = H.number_of_edges()
dn = DH.number_of_nodes()
dp = DH.number_of_edges()

Hdegrees = list(d for n,d in H.degree())
HDdegrees = list(d for n,d in DH.degree())

Hindegrees = list(d for n,d in DH.in_degree())
Houtdegrees = list(d for n,d in DH.out_degree())
DH.in_edges()

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
for node in H.nodes :
    positions[node] = location(H,node)

#nx.draw_networkx(G, pos = positions, with_labels = True, ax = True, node_size = 100, node_color = "y", cmap = True, edge_color = "b", edge_cmap = True)

nx.draw_networkx(H, pos = positions, with_labels = False, node_size = 30, node_color = "r", cmap = False, edge_color = "y", edge_cmap = True)


""" Degree centrality """
plt.hist(Hdegrees)

Hdegree_centrality = []
for node in H.nodes:
    Hdegree_centrality += [nx.degree_centrality(H)[node]]
plt.hist(Hdegree_centrality)


""" Connected components """
Hconnected_comp_lengths = [len(c) for c in sorted(nx.connected_components(H), key=len, reverse=True)]
Hconnected_comp = sorted(nx.connected_component_subgraphs(H), key=len, reverse=True)
plt.hist(Hconnected_comp_lengths)

Hconnected_comp_lengths_2 = []
m = min(Hconnected_comp_lengths)    
for k in Hconnected_comp_lengths:
    if k > 5 :
        Hconnected_comp_lengths_2 += [k]
plt.hist(Hconnected_comp_lengths_2)

nx.average_clustering(H, weight = 'trips')

nx.clustering(H)

""" 2D degrees repartition """

DegH = np.zeros((len(NS_axis),len(EW_axis)))
k = 0
for j in range(len(EW_axis)) :
    for i in range(len(NS_axis)) :
        k += 1
        if k in H.nodes :
            DegH[i][j] = H.degree(k)

plt.imshow(DegH)

DegH2 = DegH[120:300]
plt.matshow(DegH2)


