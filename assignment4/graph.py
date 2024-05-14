import vertex as v
import sys
from edge import Edge
import copy


class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.graph_dict.keys())

    def get_adjacent_blockable_edges(self,vertex):
        blockable_edges = []
        for neighbor_tup in self.expand(vertex):
            if neighbor_tup[2].blocked_in_prob > 0:
                blockable_edges.append(neighbor_tup[2])
        return blockable_edges

    def get_edges(self):
        edges = set()
        for vertex in self.graph_dict:
            for neighbor_tuple in self.graph_dict[vertex]:
                edges.add(neighbor_tuple[2])
        return list(edges)

    def get_blockable_edges(self) -> list[Edge]:
        edges = self.get_edges()
        return [edge for edge in edges if edge.blocked_in_prob > 0]

    def get_vertex(self, location):
        vertex_to_ret = None
        for vertex in self.get_vertices():
            if vertex.location == location:
                vertex_to_ret = vertex
        return vertex_to_ret

    def vertices_location(self):
        list = []
        for vertex in self.get_vertices():
            list.append(vertex.location)
        return list

    def expand(self, vertex):
        return self.graph_dict[vertex]

    def expand_just_vertices(self, vertex):
        return list(map(lambda neighbor_tup: neighbor_tup[0], self.expand(vertex)))

    def expand_just_edges(self, vertex):
        return list(map(lambda neighbor_tup: neighbor_tup[2], self.expand(vertex)))

    def get_edge_weight(self, vertex1, vertex2):
        neighbors = self.expand(vertex1)
        for neighbor in neighbors:
            if neighbor[0].location == vertex2.location:
                return neighbor[1]

    def vertex_exists(self, vertex):
        return vertex.location in self.vertices_location()

    def edge_exists(self, vertex1, vertex2):
        neighbor_list = self.expand(vertex1)
        for neighbor_tup in neighbor_list:
            if vertex2 == neighbor_tup[0]:
                return True
        return False

    def get_edge(self, vertex1: v.Vertex, vertex2: v.Vertex) -> Edge:
        neighbor_list = self.expand(vertex1)
        for neighbor_tup in neighbor_list:
            if vertex2 == neighbor_tup[0]:
                return neighbor_tup[2]
        return None

    def add_vertex(self, vertex):
        if not self.vertex_exists(vertex):
            self.graph_dict[vertex] = []

    def add_edge(self, vertex1, vertex2, weight, edge_name, probability=0):
        edge = Edge(edge_name, weight, vertex1, vertex2, probability)
        if vertex2 not in self.expand_just_vertices(vertex1) and vertex1 not in self.expand_just_vertices(vertex2):
            self.graph_dict[vertex1].append((vertex2, weight, edge))
            self.graph_dict[vertex2].append((vertex1, weight, edge))

    def generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbor_tuple in self.graph_dict[vertex]:
                edges.append((vertex, neighbor_tuple[0], neighbor_tuple[1]))
        return edges

    def __str__(self):
        s = ""
        for edge in self.get_edges():
            s += str(edge) + "\n"
        s += "\n"
        return s

    def copy_graph(self):
        new_graph = Graph()
        for vertex in self.get_vertices():
            new_graph.graph_dict[vertex] = list(self.expand(vertex))
        return new_graph



