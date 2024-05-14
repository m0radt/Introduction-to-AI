import copy as c


class State:

	def __init__(self, max_agent_index, min_agent_index,world ,depth, parent=None):
		self.parent = parent
		self.max_agent_index = max_agent_index
		self.min_agent_index  = min_agent_index
		self.depth = depth
		self.world = c.deepcopy(world)




	def max_successors(self):
		new_states = []
		max_agent = self.world.agents[self.max_agent_index]
		for direction in self.world.expand((max_agent.X,max_agent.Y)):
			neighbor_state = State(self.max_agent_index, self.min_agent_index, self.world ,self.depth +1,self)
			neighbor_state.move_max_agent(direction)
			neighbor_state.update_max_state()
			neighbor_state.world.increment_time()
			new_states.append(neighbor_state)
			

		return new_states
	def max_successors_with_direction(self):
		new_states = []
		max_agent = self.world.agents[self.max_agent_index]
		for direction in self.world.expand((max_agent.X,max_agent.Y)):
			neighbor_state = State(self.max_agent_index, self.min_agent_index, self.world ,self.depth +1,self)
			# print("agent is in : " + str(neighbor_state.world.agents[1].X)+ ", " +str(neighbor_state.world.agents[1].Y))
			# print("Agent dir :" + str(direction))
			neighbor_state.move_max_agent(direction)
			# print("agent went to : " + str(neighbor_state.world.agents[1].X)+ ", " +str(neighbor_state.world.agents[1].Y))
			neighbor_state.update_max_state()
			neighbor_state.world.increment_time()
			new_states.append((direction,neighbor_state))
			

		return new_states

	def min_successors(self):
		new_states = []
		min_agent = self.world.agents[self.min_agent_index]
		for direction in self.world.expand((min_agent.X,min_agent.Y)):
			neighbor_state = State(self.max_agent_index, self.min_agent_index, self.world ,self.depth +1,self)
			neighbor_state.move_min_agent(direction)
			neighbor_state.update_min_state()
			neighbor_state.world.increment_time()
			new_states.append(neighbor_state)
			

		return new_states

	def evaluate_alpha_beta(self):
		return self.world.agents[self.max_agent_index].score- self.world.agents[self.min_agent_index].score
	def utility_alpha_beta(self):
		return (self.world.agents[self.max_agent_index].score + (len(self.world.agents[self.max_agent_index].delivery_goal) * (1/4)))- (self.world.agents[self.min_agent_index].score + (len(self.world.agents[self.min_agent_index].delivery_goal) * (1/4)))
	
	def evaluate(self):
		return self.world.agents[self.max_agent_index].score, self.world.agents[self.min_agent_index].score,self.depth
	def utility(self):
		return self.world.agents[self.max_agent_index].score + (len(self.world.agents[self.max_agent_index].delivery_goal) * (1/4)), self.world.agents[self.min_agent_index].score + (len(self.world.agents[self.min_agent_index].delivery_goal) * (1/4)),self.depth
	

	def __str__(self):
		s = "max agent: " + "(" + str(self.world.agents[self.max_agent_index].X)+", "+ str(self.world.agents[self.max_agent_index].Y) +")"+ "\n" + "min agent: " + "(" + str(self.world.agents[self.min_agent_index].X)+", "+ str(self.world.agents[self.min_agent_index].Y) +")" 
		return s


	
	def move_max_agent(self,direction):
		max_agent = self.world.agents[self.max_agent_index]
		
		prev = (max_agent.X,max_agent.Y)
		max_agent.X, max_agent.Y= max_agent.X +direction[0],max_agent.Y + direction[1]
		if(prev,(max_agent.X,max_agent.Y)) in self.world.fragile_edges:
			self.world.add_blocked_edge(prev[0],prev[1],max_agent.X, max_agent.Y)
			self.world.remove_fragile_edge(prev[0],prev[1],max_agent.X, max_agent.Y)

	def move_min_agent(self,direction):
		min_agent = self.world.agents[self.min_agent_index]
		prev = (min_agent.X,min_agent.Y)
		min_agent.X, min_agent.Y= min_agent.X +direction[0],min_agent.Y + direction[1]
		if(prev,(min_agent.X,min_agent.Y)) in self.world.fragile_edges:
			self.world.add_blocked_edge(prev[0],prev[1],min_agent.X, min_agent.Y)
			self.world.remove_fragile_edge(prev[0],prev[1],min_agent.X, min_agent.Y)
			
	def update_max_state(self):
		max_agent = self.world.agents[self.max_agent_index]
		for i,package in enumerate(self.world.packages):#if you are on package pick it up
			if package['start_time'] <= self.world.current_time  <= package['deadline'] and package['status'] == 'available' and package['pickup'] == (max_agent.X,max_agent.Y) :
				package['status'] = 'picked_up'
				max_agent.delivery_goal.append(package['delivery'])
				max_agent.packages_indexes.append(i)
            #if you are on package delievery leave it up
		for package_index in max_agent.packages_indexes:     
			if self.world.packages[package_index]['status'] != 'delivered' and  self.world.packages[package_index]['delivery'] == (max_agent.X,max_agent.Y) and self.world.current_time <= self.world.packages[package_index]['deadline']:
				if (max_agent.X,max_agent.Y) in max_agent.delivery_goal:
					max_agent.delivery_goal.remove((max_agent.X,max_agent.Y) )
				max_agent.score += 1    
				self.world.packages[package_index]['status'] = 'delivered'
	def update_min_state(self):
		min_agent = self.world.agents[self.min_agent_index]
		for i,package in enumerate(self.world.packages):#if you are on package pick it up
			if package['start_time'] <= self.world.current_time  <= package['deadline'] and package['status'] == 'available' and package['pickup'] == (min_agent.X,min_agent.Y) :
				package['status'] = 'picked_up'
				min_agent.delivery_goal.append(package['delivery'])
				min_agent.packages_indexes.append(i)
            #if you are on package delievery leave it up
		for package_index in min_agent.packages_indexes:     
			if self.world.packages[package_index]['status'] != 'delivered' and  self.world.packages[package_index]['delivery'] == (min_agent.X,min_agent.Y)and self.world.current_time <= self.world.packages[package_index]['deadline']:
				if (min_agent.X,min_agent.Y) in min_agent.delivery_goal:
					min_agent.delivery_goal.remove((min_agent.X,min_agent.Y) )
				min_agent.score += 1    
				self.world.packages[package_index]['status'] = 'delivered'
		






