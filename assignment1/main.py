import heapq
import agent
import graph
import TreeNode




def mst_heuristic(vertex: TreeNode.TreeNode):
    packages,delivery,pickup_to_delivery= vertex.state.get_unvisited_vertices()
    if vertex.state.current_position not in delivery:
        delivery.append(vertex.state.current_position)

    new_graph =vertex.state.world.to_graph(packages,delivery,pickup_to_delivery)
    new_graph_mst = new_graph.MST()
    return new_graph_mst.get_sum_weights()



class Environment:
    
    def __init__(self):
        self.max_x =0
        self.max_y =0
        self.packages = []
        self.blocked_edges = set()
        self.fragile_edges = set()
        self.agents = []
        self.current_time = 0 

        

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

    def map_pickup_to_delivery(self):
        map = {}
        for package in self.packages:
            if package['start_time']<= self.current_time and package['status'] == 'available' :
                map[package['pickup']] = package['delivery']

        return map
    def current_packages(self):
        packages_list = []
        for package in self.packages:
            if package['start_time']<= self.current_time and package['status'] == 'available' :
                packages_list.append(package['pickup'])
                packages_list.append(package['delivery'])


        return packages_list

    def expand(self, vertex):
        res= []
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
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
                    
                    if package['start_time']<= world.current_time and(package.get('status') != 'picked_up'and package.get('status') != 'delivered' and package.get('pickup') == (col,row)) or (package.get('status') == 'delivered' and package.get('delivery') == (col,row)):
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
            
        while self.packages and not all(package['status'] == 'delivered' for package in self.packages):
            self.display()
            for agent in self.agents:
                agent.act(self)
            self.current_time += 1
        for agent in self.agents:
            print(agent)

            


    def to_graph(self,packages,delivery,pickup_to_delivery):  
        new_graph = graph.Graph()
        
        for vertex in delivery+packages + [pickup_to_delivery[x] for x in packages]:
            new_graph.add_vertex(vertex)
        for i, vertex1 in enumerate(delivery+packages):        
            for j, vertex2 in enumerate(delivery+packages):
                if(i <= j):continue

                weight = self.shortest_path(vertex1, vertex2)
                if(weight < 0):continue
                new_graph.add_edge(vertex1,vertex2,weight)
        for vertex in packages:
            weight = self.shortest_path(vertex, pickup_to_delivery[vertex])
            if(weight < 0):continue
            new_graph.add_edge(vertex,pickup_to_delivery[vertex],weight)

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
                case "#G":
                    self.add_agent(agent.GreedyAgent(int(words[1]),int(words[2])))
                case "#A":
                    self.add_agent(agent.AStarAgent(int(words[1]),int(words[2])))
                case "#R":
                    self.add_agent(agent.RealTimeAStarAgent(int(words[1]),int(words[2])))
                case "#S":
                    self.add_agent(agent.StupidGreedyAgent(int(words[1]),int(words[2])))
                case "#H":
                    self.add_agent(agent.Human(int(words[1]),int(words[2])))
                case "#I":
                    pass


 
 
        f.close()
    
    def shortest_path(self, start, target):
        heap = [(0,start)]
        visited = set()
        while heap:
            (cost,current) = heapq.heappop(heap)
            visited.add(current)
            if current == target:
                return cost
            

            x, y = current
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if self.inGrid(neighbor) and neighbor not in visited and (current,neighbor) not in self.blocked_edges:
                    heapq.heappush(heap, (cost + 1, neighbor))

        return -1
    def find_shortest_path(self, start, target):
        heap = [(0,start)]
        visited = set()
        parent = {}
        while heap:
            (cost,current) = heapq.heappop(heap)
            visited.add(current)
            if current == target:
                return self.reconstruct_path(start,current,parent)
            

            x, y = current
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            for neighbor in neighbors:
                if self.inGrid(neighbor) and neighbor not in visited and (current,neighbor) not in self.blocked_edges:
                    heapq.heappush(heap, (cost + 1, neighbor))
                    parent[neighbor] = current
        return None

    def inGrid(self, position):
        return  0 <= position[0] <= self.max_x and 0 <= position[1] <= self.max_y
    
    def reconstruct_path(self, start, end, parent):
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]
        return path
    def copy(self):
        pass
        #import copy copied_object = copy.deepcopy(original_object)


      
def k(world):
    print("packages_indexes")
    print(world.agents[0].packages_indexes) 
    print("delivery_goal")
    print(world.agents[0].delivery_goal)
    print("seq")
    print(world.agents[0].seq )
    print("package 0")
    print(world.packages[0])
    print("package 1")
    print(world.packages[1])

if __name__ == '__main__':
    world = Environment()

    world.load_input('input.txt')
    world.run_simulation()



