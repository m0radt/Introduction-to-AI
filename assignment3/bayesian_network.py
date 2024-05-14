from node import Node


class BayesianNetwork:
    def __init__(self) :
        self.nodes = []

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.append(node)

    def add_relation(self, parent: Node, child: Node):
        if parent not in child.parents:
            child.parents.append(parent)

    def get_node(self, node_name: str):
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None
    
    def get_parents(self, node_name: str) -> list:
        node = self.get_node(node_name)
        return node.parents
    def get_all_nodes(self) -> list:
        return self.nodes
    
    def __str__(self):
        s = 'Bayesian Network:\n'
        s += 'nodes: \n'
        for node in self.nodes:
            s += str(node)
        return s


def create_all_entries_for_one_evidence(name):
    return [[(name, False)], [(name, True)]]

def create_all_entries_for_season(name = "Season"):
    return [[(name, "low")], [(name, "medium")], [(name, "high")]] 

def create_all_entries_for_two_evidences(name1, name2):
    return [[(name1, False), (name2, False)], [(name1, False), (name2, True)],
             [(name1, True), (name2, False)], [(name1, True), (name2, True)]]
