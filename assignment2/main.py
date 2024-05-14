import random
import agent
import graph


class Environment:
    
    def __init__(self):
        self.max_x =0
        self.max_y =0
        self.packages = []
        self.blocked_edges = set()
        self.fragile_edges = set()
        self.agents = []
        self.current_time = 0
    

    def increment_time(self):
        self.current_time += 1

        

    def add_package(self, pickup_x, pickup_y, delivery_x, delivery_y, start_time, deadline):
        package = {
            'pickup': (pickup_x, pickup_y),
            'delivery': (delivery_x, delivery_y),
            'start_time': start_time,
            'deadline': deadline,
            'status': 'available' # 'delivered' 'waiting-to-get-picked-up'
        }
        self.packages.append(package)

    def add_blocked_edge(self, x1, y1, x2, y2):
        self.blocked_edges.add(((x1, y1), (x2, y2)))
        self.blocked_edges.add(((x2, y2), (x1, y1)))

    def add_fragile_edge(self, x1, y1, x2, y2):
        self.fragile_edges.add(((x1, y1), (x2, y2)))
        self.fragile_edges.add(((x2, y2), (x1, y1)))

    def remove_fragile_edge(self, x1, y1, x2, y2):
        self.fragile_edges.remove(((x1, y1), (x2, y2)))
        self.fragile_edges.remove(((x2, y2), (x1, y1)))

    def add_agent(self, agent):
        self.agents.append(agent)
    def current_packages(self):
        packages_list = []
        for package in self.packages:
            if package['start_time']<= self.current_time  <= package['deadline'] and package['status'] == 'available' :
                packages_list.append(package['pickup'])
                packages_list.append(package['delivery'])


        return packages_list

    def expand(self, vertex):
        res= []
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(moves)
        for move in moves:
                neighbor =(vertex[0]+move[0],vertex[1]+move[1])
                if self.inGrid(neighbor)  and (vertex,neighbor) not in self.blocked_edges :
                    res.append(move)
        return res

    # display for debugging
    def display(self):
        print("".join(['*'] * (2 * self.max_x + 1)), end='')
        for row in reversed(range(self.max_y + 1)):
            edgesNCell = [' '] * (2 * self.max_x + 1)
            for col in range(self.max_x + 1):
                cell = ' '
                edgesNCell[col*2] = chr(9608)


                for i, package in enumerate(self.packages):
                    
                    if  package['start_time']<= self.current_time <= package['deadline'] and (package.get('status') != 'picked_up'and package.get('status') != 'delivered' and package.get('pickup') == (col,row)) or (package.get('status') == 'delivered' and package.get('delivery') == (col,row)):
                        edgesNCell[col*2] = str(i)
                for agent in self.agents:
                    if agent.X == col and agent.Y == row:
                       edgesNCell[col*2] = agent.symbol
                    

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

    def run_simulation(self):
            
        while self.packages and not all(package['status'] == 'delivered'  or  self.current_time > package['deadline'] for package in self.packages):
            self.display()
            for agent in self.agents:
                agent.act(self)
            self.increment_time()
        for agent in self.agents:
            print(agent)

            


    def to_graph(self,vertices_list):  
        new_graph = graph.Graph()
        
        for vertex in vertices_list:
            new_graph.add_vertex(vertex)
        for i, vertex1 in enumerate(new_graph.get_vertices()):        
            for j, vertex2 in enumerate(new_graph.get_vertices()):
                if(i <= j):continue

                weight = self.shortest_path(vertex1, vertex2)
                if(weight < 0):continue
                new_graph.add_edge(vertex1,vertex2,weight)
        return new_graph


        
        

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
                    self.add_package(int(words[1]),int(words[2]),int(words[5]),int(words[6]),int(words[3]),int(words[7]))
                case "#B":
                    self.add_blocked_edge(int(words[1]),int(words[2]),int(words[3]),int(words[4]))

                case "#F":
                    self.add_fragile_edge(int(words[1]),int(words[2]),int(words[3]),int(words[4]))
                case "#Adversarial":               
                    agent1 = agent.MinimaxAgent(int(words[1]),int(words[2]), len(self.agents), len(self.agents)+1,False,True)
                    agent2 = agent.MinimaxAgent(int(words[3]),int(words[4]), len(self.agents) + 1, len(self.agents),False,True)
                    self.add_agent(agent1)
                    self.add_agent(agent2)
                case "#Semi-Cooperative":               
                    agent1 = agent.MinimaxAgent(int(words[1]),int(words[2]), len(self.agents), len(self.agents)+1, True,False)
                    agent2 = agent.MinimaxAgent(int(words[3]),int(words[4]), len(self.agents) + 1, len(self.agents), True,False)
                    self.add_agent(agent1)
                    self.add_agent(agent2)
                case "#Fully-Cooperative":               
                    agent1 = agent.MinimaxAgent(int(words[1]),int(words[2]), len(self.agents), len(self.agents)+1,False,False)
                    agent2 = agent.MinimaxAgent(int(words[3]),int(words[4]), len(self.agents) + 1, len(self.agents),False, False)
                    self.add_agent(agent1)
                    self.add_agent(agent2)


                case "#H":
                    self.add_agent(agent.Human(int(words[1]),int(words[2])))



 
 
        f.close()
    

    def inGrid(self, position):
        return  0 <= position[0] <= self.max_x and 0 <= position[1] <= self.max_y
    
    def reconstruct_path(self, start, end, parent):
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        return path
 


      


if __name__ == '__main__':
    world = Environment()

    world.load_input('input.txt')
    world.run_simulation()

    

    

    



