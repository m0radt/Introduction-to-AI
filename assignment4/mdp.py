import operator
from functools import reduce
import copy
from state import State
from graph import Graph
from state import consistent_states, discovered_edges
import names


def transition(s1: State, s2: State, world: Graph) -> float:
	source_vertex = s1.current_vertex
	destination_vertex = s2.current_vertex
	blockable_edges_from_dest = world.get_adjacent_blockable_edges(destination_vertex)
	if s1.same_status(s2):
		for blockable_edge in blockable_edges_from_dest:
			if s2.edges_status[blockable_edge] == names.U:
				return 0
		return 1
	if not consistent_states(s1, s2):
		return 0
	for blockable_edge in s1.edges_status.keys():
		if s1.edges_status[blockable_edge] == names.U and s2.edges_status[blockable_edge] != names.U:
			if blockable_edge not in blockable_edges_from_dest:
				return 0
		elif s1.edges_status[blockable_edge] == names.U and s2.edges_status[blockable_edge] == names.U:
			if blockable_edge in blockable_edges_from_dest:
				return 0
	new_edges = discovered_edges(s1, s2)
	prob = 1
	for edge_tup in new_edges:
		if edge_tup[1] == 1:
			prob *= edge_tup[0].blocked_in_prob
		else:
			prob *= (1 - edge_tup[0].blocked_in_prob)
	return round(prob, 2)


def initialize_policies(policies: dict, states: list[State]):
	for state in states:
		if state.current_vertex.target:
			policies[state] = (0, names.finish)
		else:
			policies[state] = (names.default_value, None)


def value_iteration(states: list[State], world: Graph) -> dict:
	policies_prev = dict()
	policies_next = dict()
	initialize_policies(policies_prev, states)
	initialize_policies(policies_next, states)
	change = True
	while change:
		change = False
		for state in [s for s in states if not s.current_vertex.target]:
			source_vertex = state.current_vertex
			max_expectancy = names.default_value
			best_action = None
			for action in state.get_actions_from(world):
				if state.edge_blocked_in_state(action):
					continue
				expectency_for_edge = 0
				for state_tag in states:
					destination_vertex = state_tag.current_vertex
					if action.is_edge_of(source_vertex, destination_vertex):
						prob = transition(state, state_tag, world)
						expectency_for_edge += prob*(-action.weight + policies_prev[state_tag][0])
				if expectency_for_edge > max_expectancy:
					max_expectancy = expectency_for_edge
					best_action = action
			if max_expectancy > policies_prev[state][0]:
				change = True
				policies_next[state] = round(max_expectancy, 2), best_action
		policies_prev = copy.copy(policies_next)
	return policies_next


def print_policies(policies:dict):
	for policy_item in policies.items():
		state = policy_item[0]
		utility = policy_item[1][0]
		action = policy_item[1][1]
		print(state, "UTILITY:", utility, "ACTION: ", action)






