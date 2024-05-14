import PriorityQueue as pq
import state
import TreeNode
import copy as c
import main

LIMIT = 10000
L_EXPANSIONS =10
T = 0.01

def get_vertices_list_as_vertices_status_dict(vertices_list):
    vertices_status_dict = dict()
    for vertex in vertices_list:
        vertices_status_dict[vertex] = False
    return vertices_status_dict

     
def generate_sequence(node):
    sequence = []
    current = node
    while current.parent is not None:
        sequence.append(current.state.current_position)
        current = current.parent
    return sequence


def g(vertex: TreeNode.TreeNode):
	return vertex.acc_weight

def goal_test(state: state.State):
	return not state.vertices_status or all(state.vertices_status.values())
class Agent:
    def __init__(self, X, Y, symbol):
        self.X = X
        self.Y = Y
        self.h = main.mst_heuristic
        self.packages_indexes = []
        self.delivery_goal = [] #(x, y)
        self.symbol = symbol
        self.seq = []
        self.time_passed =0
        self.num_of_expansions =0 
        self.num_of_movements = 0
        self.score = 0


    def act(self):
        pass
    def  formulate_state(self,world):
        for i,package in enumerate(world.packages):
            if package['start_time']<= world.current_time and package['status'] == 'available' and package['pickup'] == (self.X,self.Y) :
                package['status'] = 'picked_up'
                self.delivery_goal.append(package['delivery'])
                self.packages_indexes.append(i)

        for package_index in self.packages_indexes:     
            if world.packages[package_index]['status'] != 'delivered' and  world.packages[package_index]['delivery'] == (self.X,self.Y):
                if (self.X,self.Y) in self.delivery_goal:
                    self.delivery_goal.remove((self.X,self.Y) )
                self.score += 1    
                world.packages[package_index]['status'] = 'delivered'

    def search_with_limit(self, world, fringe:pq.PriorityQueue, limit ):
        counter = 0
        fringe.insert(TreeNode.TreeNode(state.State((self.X,self.Y),get_vertices_list_as_vertices_status_dict(world.current_packages() + self.delivery_goal),world.map_pickup_to_delivery(),self.delivery_goal, world), None, 0,0,(0,0)))
        while fringe.not_empty():

            node = fringe.pop()
            node_state = node.state

            node_state.visit_current_vertex_if_you_near()
            if counter == limit or goal_test(node_state):
                self.seq = generate_sequence(node)
                break
            counter += 1
            for direction in node_state.world.expand(node_state.current_position):
                neighbor_state = state.State(node_state.current_position, node_state.vertices_status,node_state.pickup_to_delivery,node_state.delivery,node_state.world)
                neighbor_state.move(direction)

                fringe.insert(TreeNode.TreeNode(neighbor_state, node, node.acc_weight + 1,node.depth +1,direction))
        return counter

    def act_with_limit(self, world, limit):

        self.formulate_state(world)
        if not self.seq:
            expansions_in_search = self.search(world, limit)
            self.num_of_expansions += expansions_in_search
            self.time_passed += T * expansions_in_search
            if not self.seq:
                return

        tmp_X, tmp_Y = self.X,self.Y
        self.X,self.Y = self.seq.pop()
        if ((tmp_X,tmp_Y),(self.X, self.Y )) in world.fragile_edges:
            world.add_blocked_edge(tmp_X,tmp_Y,self.X, self.Y)
            world.remove_fragile_edge(tmp_X,tmp_Y,self.X, self.Y)
        self.num_of_movements += 1
        self.time_passed += 1

    def __str__(self):
        agent_str = "-------------------------\n"
        agent_str += type(self).__name__ + "\n"
        agent_str += "Score: " + str(self.score) + "\n"
        agent_str += "Number of expansions: " + str(self.num_of_expansions) + "\n"
        agent_str += "Number of movements: " + str(self.num_of_movements) + "\n"
        agent_str += "Total time passed: " + str(self.time_passed) + "\n"
        agent_str += "-------------------------\n"
        return agent_str



        
class Human(Agent):
    def __init__(self, X, Y):
        super().__init__(X, Y, 'H') 

    def search(self, world, limit):
        pass
    def act(self,world):
        world.display()
        move = input("Enter your move (u/d/l/r/n): ")  
        self.takeAction(move)

    def takeAction(self,world,move):
        x, y = self.X, self.Y
        match move:
            case 'u':
                if y < world.max_y and not ((x,y),(x, y + 1)) in world.blocked_edges:
                    self.Y += 1
                    if ((x,y),(x, y + 1)) in world.fragile_edges:
                        world.add_blocked_edge(x, y, x, y+1)
                        world.remove_fragile_edge(x, y, x, y+1)
                else:
                    print("You can't go up")
            case 'r':
                if x< world.max_x and not ((x,y),(x +1, y)) in world.blocked_edges:
                    self.X += 1
                    if ((x,y),(x + 1, y)) in world.fragile_edges:
                        world.add_blocked_edge(x, y, x + 1, y)
                        world.remove_fragile_edge(x, y, x + 1, y)
                else:
                    print("You can't go right")
            case 'd':
                if y > 0 and not ((x,y),(x, y - 1)) in world.blocked_edges:
                    self.Y -= 1
                    if ((x,y),(x, y - 1)) in world.fragile_edges:
                        world.add_blocked_edge(x, y, x, y-1)
                        world.remove_fragile_edge(x, y, x, y-1)


                else:
                    print("You can't go down")
            case 'l':
                if x >0 and not ((x,y),(x - 1, y)) in world.blocked_edges:
                    self.X -= 1
                    if ((x,y),(x - 1, y)) in world.fragile_edges:
                        world.add_blocked_edge(x, y, x - 1, y)
                        world.remove_fragile_edge(x, y, x - 1, y)
                else:
                    print("You can't go left")
            case 'n':
                pass
    
             

        
              

            
class StupidGreedyAgent(Agent):

    def __init__(self, X, Y):
        super().__init__(X, Y, 'S') 
        self.packages_indexes = []
        self.path = []
        self.state ='looking up for package'#'pick up a package'
        self.delivery_goal = [] #(x, y)
        self.pickup_package_index = -1
        self.deliver_package = False #if false we are look for a package or going to get a package else we are delevering a package.

    def  formulate_state(self,world):
        for i,package in enumerate(world.packages):
            if package['pickup'] == (self.X,self.Y) :
                package['status'] = 'picked_up'
                self.delivery_goal.append(package['delivery'])
                self.packages_indexes.append(i)

        for package_index in self.packages_indexes:     
            if world.packages[package_index]['delivery'] == (self.X,self.Y):
                if package_index == self.pickup_package_index:
                    self.pickup_package_index = -1
                elif (self.X,self.Y) in self.delivery_goal:
                    self.delivery_goal.remove((self.X,self.Y) )

                world.packages[package_index]['status'] = 'delivered'


        

    def  formulate_goal(self,world):
        length = len(world.packages)
        for i in range(length):
            if world.packages[i]['status'] == 'available':
                world.packages[i]['status'] = 'waiting-to-get-picked-up'
                self.packages_indexes.append(i)
                return (i,world.packages[i]['delivery'])
        
        return None



    def act(self,world):
        self.state = self.formulate_state(world)

        if not self.path:
            if self.delivery_goal:
                target = self.delivery_goal.pop(0)
                self.path = world.find_shortest_path((self.X,self.Y),target)
                if not self.path:
                    print("fail________1__________________")
                    return
            else:
                g = self.formulate_goal(world)
                if not g :
                    print("fail___________2_______________")
                    return
                self.pickup_package_index = g[0]
                self.delivery_goal.append(g[1])
                print("self.goal is : " +' '.join(str(x) for x in self.delivery_goal) )
                self.path = world.find_shortest_path((self.X,self.Y),world.packages[self.pickup_package_index]['pickup'])
                if not self.path:
                    print("fail____________3______________")
                    self.pickup_package_index = -1
                    self.delivery_goal.pop()
                    return


        tmp_X, tmp_Y = self.X,self.Y
        self.X,self.Y = self.path.pop()
        if ((tmp_X,tmp_Y),(self.X, self.Y )) in world.fragile_edges:
            world.add_blocked_edge(tmp_X,tmp_Y,self.X, self.Y)
            world.remove_fragile_edge(tmp_X,tmp_Y,self.X, self.Y)
                        



class GreedyAgent(Agent):
    def __init__(self,X,Y):
        super().__init__(X,Y,'G')

    def search(self,world,limit):
        fringe = pq.PriorityQueue(self.h)
        return self.search_with_limit(world,fringe,limit)
    
    def act(self,world):
        return self.act_with_limit(world,LIMIT)

class AStarAgent(Agent):
    def __init__(self,X,Y):
        super().__init__(X,Y,'A')

    def search(self,world,limit):
        fringe = pq.PriorityQueue(lambda x: self.h(x) + g(x))
        return self.search_with_limit(world,fringe,limit)
    
    def act(self,world):
        return self.act_with_limit(world,LIMIT)

class RealTimeAStarAgent(Agent):
    def __init__(self,X,Y):
        super().__init__(X,Y,'R')

    def search(self,world,limit):
        fringe = pq.PriorityQueue(lambda x: self.h(x) + g(x))
        return self.search_with_limit(world,fringe,limit)
    
    def act(self,world):
        return self.act_with_limit(world,L_EXPANSIONS)

