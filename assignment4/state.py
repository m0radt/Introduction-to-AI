import vertex as v
import copy as cp
import graph as g
import names
from edge import Edge
import itertools


def generate_states(graph: g.Graph):
	states = []
	vertices = graph.get_vertices()
	edges = graph.get_edges()
	blockable_edges = [edge for edge in edges if edge.blocked_in_prob > 0]
	possibilites_for_edges = itertools.product([0, 1, names.U], repeat=len(blockable_edges))
	for possibility in possibilites_for_edges:
		edges_status = dict(zip(blockable_edges, possibility))
		for vertex in vertices:
			states.append(State(vertex, edges_status))
	return filter_bad_states(states, graph)


def get_starting_state(states:list, starting_vertex):
	for state in states:
		if state.current_vertex == starting_vertex and state.all_edges_unknown():
			return state
	exit(1)


def get_state_from_states(states:list, required_current_vertex, required_edges_status):
	for state in states:
		if state.current_vertex == required_current_vertex and state.edges_status == required_edges_status:
			return state
	exit(2)


class State:

	def __init__(self, current_vertex: v.Vertex, edges_status: dict):
		self.current_vertex = current_vertex
		self.edges_status = cp.copy(edges_status)

	def all_edges_unknown(self) -> bool:
		for value in self.edges_status.values():
			if value != names.U:
				return False
		return True

	def same_status(self, other) -> bool:
		return self.edges_status == other.edges_status

	def get_actions_from(self, world: g.Graph) -> list[Edge]:
		return world.expand_just_edges(self.current_vertex)

	def __str__(self):
		s = "STATE\nCurrent vertex: " + str(self.current_vertex) + "\n{"
		for edge in self.edges_status:
			s += edge.name + ": " + str(self.edges_status[edge]) + ", "
		return s + "}\n"

	def edge_blocked_in_state(self, edge:Edge) -> bool:
		for edge_status in self.edges_status.items():
			edge_from_status = edge_status[0]
			status = edge_status[1]
			if status == 1 and edge_from_status == edge:
				return True
		return False

	def goal_state(self):
		return self.current_vertex.target


def state_list_as_string(state_list) -> str:
	s = "STATES:\n"
	for state in state_list:
		s += str(state) + "\n"
	return s


def consistent_states(state1: State, state2: State) -> bool:
	for edge_status in state1.edges_status.items():
		edge = edge_status[0]
		status = edge_status[1]
		if (status == 0 or status == 1) and state2.edges_status[edge] != status:
			return False
	return True


def discovered_edges(state1: State, state2: State) -> list:
	edges = []
	for blockable_edge in state1.edges_status.keys():
		if state1.edges_status[blockable_edge] == names.U:
			if state2.edges_status[blockable_edge] != names.U:
				zero_or_one = state2.edges_status[blockable_edge]
				edges.append((blockable_edge, zero_or_one))
	return edges


def filter_bad_states(states:list[State], graph:g.Graph) -> list[State]:
	filtered_states = []
	for state in states:
		vertex = state.current_vertex
		blockable_edges_from_vertex = graph.get_adjacent_blockable_edges(vertex)
		makes_sense = True
		for blockable_edge in blockable_edges_from_vertex:
			if state.edges_status[blockable_edge] == names.U:
				makes_sense = False
				break
		if makes_sense:
			filtered_states.append(state)
	return filtered_states
