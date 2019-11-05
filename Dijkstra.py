# 6.0002 Problem Set 2
# Graph Optimization
# Name: Deniz Sert
# Collaborators: Karen Gao, Luke, Office Hours TAs
# Time: 4 hrs

#
# Finding shortest paths to drive from home to work on a road network
#


import unittest
from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER:
# Nodes: The places in MIT
# Edges: The paths between each place at MIT.
# Times: The weight of each of travel time.


# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by tabs:
            From To TotalTime  RoadType
        e.g.
            N0	N1	15	interstate
        This entry would become an edge from 'N0' to 'N1' on an interstate highway with 
        a weight of 15. There should also be another edge from 'N1' to 'N0' on an interstate
        using the same weight.

    Returns:
        a directed road map representing the inputted map
    """
    #initialize a RoadMap
    road_map = RoadMap()
    #with loop will automatically close file
    with open(map_filename) as f:
        read_data = f.readlines()
    for line in read_data:
        n_1, n_2, time, road_type = tuple(line.split())
        
        n_start = Node(n_1)
        n_end = Node(n_2)
        #adds nodes to Map
        if not road_map.has_node(n_start):
            road_map.add_node(n_start)
        if not road_map.has_node(n_end):
            road_map.add_node(n_end)
        
        #creates Roads
        r1 = DirectedRoad(Node(n_1), Node(n_2), int(time), road_type)
        r2 = DirectedRoad(Node(n_2), Node(n_1), int(time), road_type)
        
        #adds roads to road map
        
        road_map.add_road(r1)
        road_map.add_road(r2)
    return road_map

# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out


# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PROBLEM 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER:

# PROBLEM 3b: Implement get_neighbors
def get_neighbors(roadmap, node, restricted_roads):
    """
    Finds the neighbors of a node in a given roadmap, without
    considering roads of type in restricted_roads.

    
    Parameter:
        roadmap: RoadMap
            The graph on which to carry out the search
        node: Node
            node whose neighbors to retrieve
        restricted_roads: list[strings]
            Road Types not under consideration

    Returns:
        list of neighbor nodes
    """
    neighbors = []
    #loops through roads starting with the passed node
    for road in roadmap.get_roads_for_node(node):
        #set variable "node" to eq the dest. of the passed node
        node = road.get_destination()
        #if node is in 
        if road.get_type() not in restricted_roads:
            neighbors.append(node)
    return neighbors

#FROM LECTURE NOTES
def Dijkstra(graph, start, end, toPrint = False):
    """
    graph: an unweighted (all edges have weight 1) digraph
    start: a node in  graph
    end: a node in graph
    returns a list representing shortest path from start to end,
       and None if no path exists"""
    #Easily modified to deal with non-negative weighted edges

    # Mark all nodes unvisited and store them.
    # Set the distance to zero for our initial node 
    # and to infinity for other nodes.
    unvisited = graph.getAllNodes()
    distanceTo = {node: float('inf') for node in graph.getAllNodes()}
    distanceTo[start] = 0
    # Mark all nodes as not having found a predecessor node on path
    #from start
    predecessor = {node: None for node in graph.getAllNodes()}

    while unvisited:
        # Select the unvisited node with the smallest distance from 
        # start, it's current node now.
        current = min(unvisited, key=lambda node: distanceTo[node])
        if toPrint: #for pedagocical purposes
            print('\nValue of current:', current)
            print('Value of distanceTo:')
            for k in distanceTo:
                print('  ' + k + ':', distanceTo[k])
            print('Value of predecessor:')
            for k in predecessor:
                print('  ' + k + ':', predecessor[k])

        # Stop, if the smallest distance 
        # among the unvisited nodes is infinity.
        if distanceTo[current] == float('inf'):
            break

        # Find unvisited neighbors for the current node 
        # and calculate their distances from start through the
        # current node.
        for neighbour in graph.childrenOf(current):
            alternativePathDist = distanceTo[current] + 1 #hops as distance

            # Compare the newly calculated distance to the assigned. 
            # Save the smaller distance and update predecssor.
            if alternativePathDist < distanceTo[neighbour]:
                distanceTo[neighbour] = alternativePathDist
                predecessor[neighbour] = current

        # Remove the current node from the unvisited set.
        unvisited.remove(current)
            
    #Attempt to be build a path working backwards from end
    path = []
    current = end
    while predecessor[current] != None:
        path.insert(0, current)
        current = predecessor[current]
    if path != []:
        path.insert(0, current)
    else:
        return None
    return path
# PROBLEM 3c: Implement get_best_path
def get_best_path(roadmap, start, end, restricted_roads, to_neighbor = False):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
        roadmap: RoadMap
            The graph on which to carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
        restricted_roads: list[strings]
            Road Types not allowed on path
        to_neighbor: boolean
            flag to indicate whether to get shortest path to end or
            shortest path to some neighbor of end 

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of nodes (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """

    # Write Dijkstra implementation here
    unvisited = list(roadmap.get_all_nodes())
    distanceTo = {node: float('inf') for node in unvisited}
    distanceTo[start] = 0
    # Mark all nodes as not having found a predecessor node on path
    #from start
    predecessor = {node: None for node in roadmap.get_all_nodes()}
    
#    print(unvisited)
#    print(end)
    if end not in unvisited:
        return None
    if start not in unvisited:
        return None
    while unvisited:
#        print(unvisited[0].get_name())
        # Select the unvisited node with the smallest distance from 
        # start, it's current node now.
        current = min(unvisited, key = lambda node: distanceTo[node])
#        if toPrint: #for pedagocical purposes
#            print('\nValue of current:', current)
#            print('Value of distanceTo:')
#            for k in distanceTo:
#                print('  ' + k + ':', distanceTo[k])
#            print('Value of predecessor:')
#            for k in predecessor:
#                print('  ' + k + ':', predecessor[k])

        # Stop, if the smallest distance 
        # among the unvisited nodes is infinity.
        if distanceTo[current] == float('inf'):
            break
        
    # Find unvisited neighbors for the current node 
        # and calculate their distances from start through the
        # current node.
        for road in roadmap.get_roads_for_node(current):
        
     #   get_neighbors(roadmap, current, restricted_roads):
            
            
#            for road in roadmap.get_roads_for_node(neighbour):
#                
#                the_road = road
#                if neighbour == road.get_destination():
#                    the_road = road
#                
                
                alternativePathDist = int(distanceTo[current]) + int(road.get_total_time())
            # Compare the newly calculated distance to the assigned. 
            # Save the smaller distance and update predecssor.
                if alternativePathDist < distanceTo[road.get_destination()] and road.get_type() not in restricted_roads:
                    distanceTo[road.get_destination()] = alternativePathDist
                    predecessor[road.get_destination()] = current
                
        # Remove the current node from the unvisited set.
        unvisited.remove(current)
        
    #Attempt to be build a path working backwards from end
    
    
    
    path = []
    if not to_neighbor:
        current = end
    else: 
        end_neighbors = get_neighbors(roadmap, end, restricted_roads)
        closest_neighbor = min(end_neighbors, key = lambda node: distanceTo[node])
        
        end = closest_neighbor
        current = end
        
        
    if start == end:
        return [], 0
    while predecessor[current] != None:
        path.insert(0, current)
        current = predecessor[current]
    if path != []:
        path.insert(0, current)
    else:
        return None
    travel_time = distanceTo[end]
    

        
    return path, travel_time
    
    # PROBLEM 4c: Handle the to_neighbor = True case here

    


# PROBLEM 4a: Implement best_path_ideal_traffic
def best_path_ideal_traffic(filename, start, end):
    """Finds the shortest path from start to end during ideal traffic conditions.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end in normal traffic,
            represented by a list of nodes (Nodes).

        If there exists no path, then return None.
    """
    #load map
    roadmap = load_map(filename)
    #no restricted paths
    best_path = get_best_path(roadmap, start, end, [])
    #check if there is no best path
    if best_path != None:
        return best_path[0]
    else:
        return None


# PROBLEM 4b: Implement best_path_restricted
def best_path_restricted(filename, start, end):
    """Finds the shortest path from start to end when local roads cannot be used.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end given the aforementioned conditions,
            represented by a list of nodes (Nodes).

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """
    #load map
    roadmap = load_map(filename)
    #can't take local roads
    best_path = get_best_path(roadmap, start, end, 'local')
    if best_path != None:
        return best_path[0]
    else:
        return None

# PROBLEM 4c: Implement best_path_to_neighbor_restricted
def best_path_to_neighbor_restricted(filename, start, end):
    """Finds the shortest path from start to some neighbor of end
    when local roads cannot be used.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end; you may assume that start != end
    Returns:
        The shortest path from start to some neighbor of end given the
            aforementioned conditions, represented by a list of nodes (Nodes).

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """
    roadmap = load_map(filename)
    #can't take local roads
    best_path = get_best_path(roadmap, start, end, 'local')
    if best_path != None:
        return best_path[0]
    else:
        return None

# UNCOMMENT THE FOLLOWING LINES TO DEBUG
#
#rmap = load_map('road_map.txt')
#my_test = load_map('test_load_map.txt')
#print(my_test)
##
#start = Node('N0')
#end = Node('N9')
#restricted_roads = ['']

#print(get_best_path(rmap, start, end, restricted_roads))

#MY TESTS
#roadmap = load_map('road_map.txt')
#start = None
#end = None
#for node in roadmap.get_all_nodes():
#    if node.get_name() == 'N0':
#        start = node
#for node in roadmap.get_all_nodes():
#    if node.get_name() == 'N9':
#        end = node
##print(best_path_ideal_traffic('road_map.txt', start, end))
#print(best_path_to_neighbor_restricted('road_map.txt', start, end))
