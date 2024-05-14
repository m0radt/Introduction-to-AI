
# class BayesianNetwork:
#     def __init__(self):
#         self.nodes = []

#     def add_node(self, node):
#         self.nodes.append(node)

#     def predict(self, query, evidence):
#         # Calculate the posterior distribution using Bayes' Rule
#         # P(query | evidence) = P(query, evidence) / P(evidence)
#         joint_prob = self.calculate_joint_prob(query, evidence)
#         evidence_prob = self.calculate_joint_prob(evidence, [])
#         posterior_prob = {}
#         for state in query.states:
#             posterior_prob[state] = joint_prob[state] / evidence_prob
#         return posterior_prob

#     def calculate_joint_prob(self, variables, given):
#         # Calculate joint probability of variables given the evidence
#         # This involves multiplying probabilities along each path in the graph
#         joint_prob = {}
#         for state in variables.states:
#             prob = self.calculate_probability(variables, state, given)
#             joint_prob[state] = prob
#         return joint_prob

#     def calculate_probability(self, node, state, given):
#         # Calculate the conditional probability of a node given its parents' states
#         prob = node.cpt[state]
#         for parent in node.parents:
#             prob *= self.calculate_probability(parent, given[parent], [])
#         return prob

from table import make_table
from node import Node

print(bool((2,)))
d ={():2, ("x",False):[2]}
print(d[("x",False)])

n1 = Node("X",make_table([[()]],[[0.2,0.8]],[]))
print(n1)
n2 = Node("X",make_table([[("Y", False),("Z", False)], [("Y", True),("Z", False)],[("Y", False),("Z", True)],[("Y", True),("Z", True)]],[[0.2,0.8],[0.4,0.6],[.1,.9], [0.5, 0.5]],["Y","Z"]))

print(n2)
print(n2.table.get_probability_given_parents(True, [("Z", True),("Y", False)]))


n3 = Node("X",make_table([[()]],[[0.1, 0.4, 0.5]],[],["low", "mid", "high"]))
print(n3)
a = 0.1
print(max(a, 1.))