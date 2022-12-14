import networkx as nx
import osmnx as ox
from src.model.algo_model import AlgorithmModel
from src.model.path_model import Path
from src.model.observable import Observable

ELEVATION_GAIN = "elevation_gain"
SHORTEST = "Shortest Route"
LENGTH = "length"

class ShortestPathController:
    """
    Initializing shortest_path, start location, end location and Algorithm model
    """
    def __init__(self, G):
        self.G = G
        self.shortest_path = None
        self.shortest_dist = None
        self.start_location = None
        self.end_location = None
        self.model = AlgorithmModel()
    
    """
    Method to compute shortest path using weights on the edges.
    """
    def get_shortest_path(self, start, end):
        self.start_location, _ = ox.get_nearest_node(self.G, point=start, return_dist=True)
        self.end_location, _ = ox.get_nearest_node(self.G, point=end, return_dist=True)
        self.shortest_path = nx.shortest_path(self.G, self.start_location, self.end_location, weight=LENGTH)

        path_model = Path()
        path_model.set_algo(SHORTEST)
        path_model.set_start_location(self.start_location)
        path_model.set_end_location(self.end_location)
        path_model.set_elevation_gain(self.model.get_path_weight(self.G, self.shortest_path, ELEVATION_GAIN))
        path_model.set_drop(0)
        path_model.set_path([[self.G.nodes[node]['x'], self.G.nodes[node]['y']]
                                            for node in self.shortest_path])
        self.shortest_dist = sum(ox.utils_graph.get_route_edge_attributes(self.G,self.shortest_path,LENGTH))
        path_model.set_distance(self.shortest_dist)
        path_model.set_path_flag(1)
        return path_model
