from state import State, get_state_from_states
from graph import Graph
import copy


def find_target(graph:Graph, blockable_edges_status: dict, policies: dict, states: list, starting_state: State):
	current_state = starting_state
	while not current_state.goal_state():
		optimal_edge = policies[current_state][1]
		print(optimal_edge)
		copied_edges_status = copy.copy(current_state.edges_status)
		destination_vertex = optimal_edge.get_destination_vertex(current_state.current_vertex)
		blockable_edges_from_destination = graph.get_adjacent_blockable_edges(destination_vertex)
		for blockable_edge in blockable_edges_from_destination:
			if blockable_edges_status[blockable_edge] == True:
				copied_edges_status[blockable_edge] = 1
			else:
				copied_edges_status[blockable_edge] = 0
		current_state = get_state_from_states(states, destination_vertex, copied_edges_status)
