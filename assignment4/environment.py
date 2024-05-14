import itertools
import graph as g
import vertex as v
import state as s
import names
from mdp import value_iteration,print_policies
import agent


class Environment:
    
    def __init__(self):
        self.max_x =0
        self.max_y =0
        self.blocked_edges = set()
        self.fragile_edges = dict()
        self.package = None
        self.agent = None


        

    def set_package(self, pickup_x, pickup_y, delivery_x, delivery_y, start_time, deadline):
        package = {
            'pickup': (pickup_x, pickup_y),
            'delivery': (delivery_x, delivery_y),
            'start_time': start_time,
            'deadline': deadline,
        }
        self.package = package

    def add_blocked_edge(self, x1, y1, x2, y2):
        self.blocked_edges.add(((x1, y1), (x2, y2)))
        self.blocked_edges.add(((x2, y2), (x1, y1)))

    def add_fragile_edge(self, x1, y1, x2, y2, probability ):
        self.fragile_edges[((x1, y1), (x2, y2))] = probability
        self.fragile_edges[((x2, y2), (x1, y1))] = probability



    def add_agent(self, agent):
        self.agent = agent

 





    def display(self):
        print("".join(['*'] * (2 * self.max_x + 1)), end='')
        for row in reversed(range(self.max_y + 1)):
            edgesNCell = [' '] * (2 * self.max_x + 1)
            for col in range(self.max_x + 1):
                cell = ' '
                edgesNCell[col*2] = chr(9608)


                
                    
                if  self.package.get('pickup') == (col,row):
                    edgesNCell[col*2] = "P"
                if  self.package.get('delivery') == (col,row):
                    edgesNCell[col*2] = "D"
                    

                if ((col, row),(col+1, row)) in self.blocked_edges:
                    edgesNCell[col*2 +1]  = '#'
                elif ((col, row),(col+1, row)) in self.fragile_edges:
                    edgesNCell[col*2 +1]  = 'F'

                if ((col, row),(col, row+1)) in self.blocked_edges:
                    cell = '#'
                elif ((col, row),(col, row+1)) in self.fragile_edges:
                    cell = 'F'
                print(cell,end=' ')
            print()
            print("".join(edgesNCell))

        print("".join(['*'] * (2 * self.max_x + 1)))


    def to_graph(self):  
        name_vertices_dict = {}
        new_graph = g.Graph()
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                node = v.Vertex((x, y))
                
                if self.package['delivery'] == (x, y):
                    node.set_target(True)
                name_vertices_dict[node.location] = node 
                new_graph.add_vertex(node)

        
        

        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                vertex = (x, y)
                neighbors = self.get_unblocked_neighbors(vertex)
                for neighbor in neighbors:
                    edge_name = "E" + str((vertex, neighbor))
                    v1 = name_vertices_dict[vertex]
                    v2 = name_vertices_dict[neighbor]

                    if (vertex,neighbor) in self.fragile_edges:
                        new_graph.add_edge(v1,v2,1, edge_name,self.fragile_edges[(vertex,neighbor)]) 
                    else:
                        new_graph.add_edge(v1,v2,1, edge_name) 
                        
        return new_graph


        
    #X 4                ; Maximum x coordinate
#Y 3                ; Maximum y coordinate
#P 0 0 0  D 4 3 50  ; Package at (0,3) from time 5, deliver to (4,0) on or before time 50
#B 3 0 4 0          ; Edge from (3,0) to (4,0) is always blocked
#B 2 2 2 3          ; Edge from (2,2) to (2,3) is always blocked
#F 0 1 0 2 0.4      ; Edge from (0,1) to (0,2) is fragile, blocked with probability 0.4 
#A 0 0              ; Normal agent starts at (0,0)    

    def load_input(self,input_file):
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
                    self.max_x = int(words[1])

                case "#Y":
                    self.max_y = int(words[1])
                case "#P":
                    self.set_package(int(words[1]),int(words[2]),int(words[5]),int(words[6]),int(words[3]),int(words[7]))
                case "#B":
                    self.add_blocked_edge(int(words[1]),int(words[2]),int(words[3]),int(words[4]))

                case "#F":
                    self.add_fragile_edge(int(words[1]),int(words[2]),int(words[3]),int(words[4]), float(words[5]))



        f.close()
    


    def inGrid(self, position):
        return  0 <= position[0] <= self.max_x and 0 <= position[1] <= self.max_y
    

    def get_unblocked_neighbors(self, vertex):
        res= []
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        for move in moves:
                neighbor =(vertex[0]+move[0],vertex[1]+move[1])
                if self.inGrid(neighbor)  and (vertex,neighbor) not in self.blocked_edges :
                    res.append(neighbor)
        return res



      




if __name__ == '__main__':
    world = Environment()
    world.load_input(names.input_file)
    graph = world.to_graph()
    print("------------------------------------------------", "\nEnvironment:\n")
    world.display()
    print("The vertices:", graph.vertices_location())
    starting_vertex = graph.get_vertex(world.package['pickup'])
    states = s.generate_states(graph)
    policies = value_iteration(states, graph)
    print_policies(policies)
    print("\n\n\n", "------------------------------------------------", "\nSIMULATION:\n")
    blockable_edges_status = dict()
    for blockable_edge in graph.get_blockable_edges():
        blocking_input = input("Do you want to block edge " + blockable_edge.name + "? respond with y or n\n")
        if blocking_input == 'y':
            blockable_edges_status[blockable_edge] = True
        else:
            blockable_edges_status[blockable_edge] = False
    agent.find_target(graph, blockable_edges_status, policies, states, s.get_starting_state(states, starting_vertex))




