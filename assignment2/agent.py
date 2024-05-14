import state as s
import comparators as comp


CUTOFF = 7



def get_vertices_list_as_vertices_status_dict(vertices_list):
    vertices_status_dict = dict()
    for vertex in vertices_list:
        vertices_status_dict[vertex] = False
    return vertices_status_dict

     
def generate_sequence(node):
    sequence = []
    current = node
    while current.parent is not None:
        sequence.append((current.world.agents[current.max_agent_index].X,current.world.agents[current.max_agent_index].Y))
        current = current.parent
    return sequence


def terminal_test(state: s.State):
	return all(package['status'] == 'delivered'or state.world.current_time > package['deadline'] for package in state.world.packages)
class Agent:
    def __init__(self, X, Y, agent_index,other_agent_index, pruning, symbol):
        self.X = X
        self.Y = Y
        self.agent_index = agent_index
        self.other_agent_index = other_agent_index
        self.pruning =pruning
        self.packages_indexes = []
        self.delivery_goal = [] #(x, y)
        self.symbol = symbol
        self.time_passed =0
        self.num_of_expansions =0 
        self.num_of_movements = 0
        self.score = 0


    def act(self, world):

        self.formulate_state(world)
        state = s.State(self.agent_index,self.other_agent_index, world, 0)

        direction =  self.alpha_beta_decision(state) if self.pruning else self.minimax_decision(state)

        tmp_X, tmp_Y = self.X,self.Y
        self.X,self.Y = self.X + direction[0],self.Y + direction[1]
        if ((tmp_X,tmp_Y),(self.X, self.Y )) in world.fragile_edges:
            world.add_blocked_edge(tmp_X,tmp_Y,self.X, self.Y)
            world.remove_fragile_edge(tmp_X,tmp_Y,self.X, self.Y)
        self.num_of_movements += 1
        self.time_passed += 1

    def  formulate_state(self,world):
        for i,package in enumerate(world.packages):
            #if you are on package pick it up
            if package['start_time']<= world.current_time <= package['deadline'] and package['status'] == 'available' and package['pickup'] == (self.X,self.Y) :
                package['status'] = 'picked_up'
                self.delivery_goal.append(package['delivery'])
                self.packages_indexes.append(i)
        #if you are on package delievery leave it up
        for package_index in self.packages_indexes:     
            if world.packages[package_index]['status'] != 'delivered' and  world.packages[package_index]['delivery'] == (self.X,self.Y) and world.current_time <= world.packages[package_index]['deadline'] :
                if (self.X,self.Y) in self.delivery_goal:
                    self.delivery_goal.remove((self.X,self.Y) )
                self.score += 1    
                world.packages[package_index]['status'] = 'delivered'



    

    def __str__(self):
        agent_str = "-------------------------\n"
        agent_str += type(self).__name__+" " + str(self.agent_index) + "\n"
        agent_str += "Score: " + str(self.score) + "\n"
        agent_str += "Number of expansions: " + str(self.num_of_expansions) + "\n"
        agent_str += "Number of movements: " + str(self.num_of_movements) + "\n"
        agent_str += "Total time passed: " + str(self.time_passed) + "\n"
        agent_str += "-------------------------\n"
        return agent_str



        


class MinimaxAgent(Agent):
    def __init__(self, X, Y,agent_index ,other_agent_index,semi_cooperative,pruning):
        self.max_comparator = comp.max_semi_cooperative_comparator if semi_cooperative else comp.fully_cooperative_comparator
        self.min_comparator = comp.min_semi_cooperative_comparator if semi_cooperative else comp.fully_cooperative_comparator
        
        super().__init__(X,Y,agent_index, other_agent_index, pruning, 'A')

    

    def alpha_beta_decision(self, state):
        best_move = (0, 0)
        v = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for direction, succ_state in state.max_successors_with_direction():
            value_of_succ_state = self.alpha_beta_min_value(succ_state, alpha, beta)
            if v < value_of_succ_state:
                v = value_of_succ_state
                best_move = direction 
            alpha = max(v, alpha)
        return best_move
    

    def minimax_decision(self, state):
        best_move = (0, 0)
        v = None
        for direction, succ_state in state.max_successors_with_direction():
            value_of_succ_state = self.min_value(succ_state)
            if v is None:
                v = value_of_succ_state
                best_move = direction 
            if(0 > self.max_comparator(value_of_succ_state,v)):
                v = value_of_succ_state
                best_move = direction 
        return best_move
    
    def max_value(self, state):
        if terminal_test(state):
            return state.evaluate()
        if  state.depth >= CUTOFF:
            return state.utility()

        v = None
        for succ in state.max_successors():
            value_of_succ_state =  self.min_value(succ)
            if v is None: v = value_of_succ_state
            if(0 > self.max_comparator(value_of_succ_state,v)):
                 v = value_of_succ_state

        return v

    def min_value(self, state):
        if terminal_test(state):
            return state.evaluate()
        if  state.depth >= CUTOFF:
            return state.utility()
        v = None
        for succ in state.min_successors():
            value_of_succ_state =  self.max_value(succ)
            if v is None: v = value_of_succ_state
            if(0 < self.min_comparator(value_of_succ_state,v)):
                 v = value_of_succ_state
        return v

        
    def alpha_beta_max_value(self, state, alpha, beta):
        if terminal_test(state):
            return state.evaluate_alpha_beta()
        if  state.depth >= CUTOFF:
            return state.utility_alpha_beta()
        v = float('-inf')
        for succ in state.max_successors():
            v = max(v, self.alpha_beta_min_value(succ, alpha, beta))
            if v >= beta:
                return v
            alpha= max(alpha,v)
        return v

    def alpha_beta_min_value(self, state, alpha, beta):
        if terminal_test(state):
            return state.evaluate_alpha_beta()
        if  state.depth >= CUTOFF:
            return state.utility_alpha_beta()
        v = float('inf')
        for succ in state.min_successors():
            v = min(v, self.alpha_beta_max_value(succ, alpha, beta))
            if v <= alpha:
                return v
            beta= min(beta,v)
        return v










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
    
             
