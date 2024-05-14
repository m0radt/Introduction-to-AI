from node import Node   
from bayesian_network import BayesianNetwork , create_all_entries_for_season,create_all_entries_for_two_evidences
from table import make_table


def create_BayesianNetwork(input_file):
    max_x, max_y =0, 0
    leakage_probability = 0
    packages_loc = {}
    fragile_edges = []
    blocked_edges = []
    season_node = None
    network = BayesianNetwork()
 
    f = open(input_file, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        words = line.split()
        if len(words) ==0:
            continue
                
        match words[0]:
            case "#X":
                max_x = int(words[1])
            case "#Y":
                max_y = int(words[1])
            case "#B":
                blocked_edges.append((int(words[1]), int(words[2]), int(words[3]), int(words[4])))
            case "#F":
                fragile_edges.append(((int(words[1]), int(words[2]), int(words[3]), int(words[4])), float(words[5])))
                
                



            case "#V":
                vertex_name = "V" + str((int(words[1]), int(words[2])))
                package_prob = float(words[4])
                packages_loc[vertex_name]=  package_prob


            case "#S":
                low_prob = float(words[1])
                mid_prob = float(words[2])
                high_prob = float(words[3])
                season_node = Node("Season",make_table([[()]],[[low_prob, mid_prob, high_prob]],[],["low", "medium", "high"]))
                network.add_node(season_node)
            case "#L":
                leakage_probability = float(words[1])
                

                        

    f.close()

    vertex_name_with_packages = packages_loc.keys()
    for y in range(max_y +1):
        for x in range(max_x +1):
            vertex_name = "V" + str((x, y))
            vertex_node = None
            if vertex_name in vertex_name_with_packages:
                vertex_node = Node(vertex_name, make_table(create_all_entries_for_season(),
                                                    calculate_prob_for_vertex_to_have_package(packages_loc[vertex_name]),
                                                    ["Season"]),
                                                    [season_node])
            else:
                vertex_node = Node(vertex_name, make_table([[()]],
                                                    [[0.0,1.0]],
                                                    []))
            network.add_node(vertex_node)

    for frag in fragile_edges:
        vertex_name1 = "V" + str((frag[0][0], frag[0][1]))
        vertex_name2 = "V" + str((frag[0][2], frag[0][3]))
        package_prob = frag[1]
        node1 = network.get_node(vertex_name1)
        node2 = network.get_node(vertex_name2)
        edge_name = "E" + str(((frag[0][0], frag[0][1]), (frag[0][2], frag[0][3])))
        edge_node = Node(edge_name, make_table(create_all_entries_for_two_evidences(vertex_name1, vertex_name2),
                                               calculate_edge_block_prob(leakage_probability, package_prob),
                                               [vertex_name1, vertex_name2]),
                                               [node1, node2])
        network.add_node(edge_node)

        
    return network,blocked_edges,[f[0] for f in fragile_edges]

    
def has_value_in_evidence(Y, evidence):
    for tup in evidence:
        if tup[0] == Y:
            return True, tup[1]
    return False, -1

def get_parent_assignment_in_evidence(Y: str, evidence: set, network: BayesianNetwork) -> list:
    parents_in_evidence = []
    parents_in_bayes = network.get_parents(Y)
    parents_in_bayes_names = [node.name for node in parents_in_bayes]
    for assignment in evidence:
        parent_name = assignment[0]
        if parent_name in parents_in_bayes_names:
            parents_in_evidence.append(assignment)
    return parents_in_evidence

def normalize(distribution):
    acc = 0
    for value in distribution.values():
        acc += value
    if not acc == 0:
        for key_value in distribution.items():
            key = key_value[0]
            value = key_value[1]
            distribution[key] = round(value / acc, 3)
    return distribution


def enumeration_ask(x_query, evidence: set, network: BayesianNetwork):
    distribution_x = {}  
    options = network.get_node(x_query).get_values()
    variables = [node.name for node in network.get_all_nodes()]
    for assignment in options:
        extended_evidence = evidence.union({(x_query,assignment)} )                              
        prob = enumeration_all(variables, extended_evidence, network)
        distribution_x[assignment] = prob
    return normalize(distribution_x)


def enumeration_all(variables, evidence, network: BayesianNetwork): 
    if len(variables) == 0:
        return 1
    Y = variables[0]
    Y_node = network.get_node(Y)
    has_val, val = has_value_in_evidence(Y, evidence)
    Y_parents = get_parent_assignment_in_evidence(Y, evidence, network)
    if has_val:
        prob_Y_given_parents = Y_node.table.get_probability_given_parents(val, Y_parents)
        return prob_Y_given_parents * enumeration_all(variables[1:], evidence, network)
    else:
        prob_sum = 0
        for value in Y_node.get_values():
            prob_sum += Y_node.table.get_probability_given_parents(value, Y_parents) * enumeration_all(variables[1:], evidence.union({(Y,value)}), network)
        return prob_sum
    

def calculate_prob_for_vertex_to_have_package(prob: float):
    return [[prob, 1-prob], [min(prob*2, 1.0), 1.0 - min(prob*2, 1.0)], [min(prob*3, 1.0) , 1.0 - min(prob*3, 1.0)]]
 
def calculate_edge_block_prob(leakage_probability: float, p: float):
    return [[leakage_probability, 1-leakage_probability], [p, 1-p], [p, 1-p],[1 - pow(1-p, 2), pow(1-p, 2)]]

def get_variables_assignment_set(vars_list):
    output_set = set()

    for item in vars_list.split('|'):
        item = item.split('=')
        if len(item) == 1 :#and (item== "quit" or item== "q" or item== "Quit"):
            return output_set
        var = item[0]
        val = item[1]
        match val:
            case 'T':
                val = True
            case 'True':
                val = True
            case 'F' :
                val = False
            case 'False' :
                val = False
            case "mid":
                val = "medium"

        output_set.add((var, val))
    return output_set    


if __name__ == '__main__':

    bayesian_network,blocked_edges, fragile_edges= create_BayesianNetwork('input.txt')
    blocked_edges_name = ["E" + str(((e[0], e[1]), (e[2], e[3]))) for e in blocked_edges] + ["E" + str(((e[2], e[3]), (e[0], e[1])))  for e in blocked_edges]
    fragile_edges_name = ["E" + str(((e[0], e[1]), (e[2], e[3]))) for e in fragile_edges] + ["E" + str(((e[2], e[3]), (e[0], e[1])))  for e in fragile_edges]
    # print(bayesian_network)

    evidences_list = (input('Insert evidence separated by | for each variable followed by its boolean value \n (i.e V(1, 0)=F|E((1, 0), (1, 1))=T|Season=medium for vertex (1, 0) NOT containing packages, edge between (1, 0) and (1, 1) is blocked and season is medium ) \n'))
    evidence = get_variables_assignment_set(evidences_list)
    # evidence = {("V(1, 0)",True),("V(1, 1)",True)}
    print("your evidence is " + str(evidence))

    x_query = input("Type your query \n")
    print("your query is \"" + x_query+ "\"")
    distribution = None
    if x_query[0]== 'E':
        if x_query in blocked_edges_name:
            distribution = {True: 1.0, False: 0.0}
        elif x_query not in fragile_edges_name:
            distribution = {True: 0.0, False: 1.0}
        else:
            distribution = enumeration_ask(x_query, evidence, bayesian_network)
    else:
        distribution = enumeration_ask(x_query, evidence, bayesian_network)


    
    print(distribution)
 

    

    

    



