import copy as c
import graph as g


class State:

	def __init__(self, current_position, vertices_status: dict,pickup_to_delivery,delivery,world ):
		self.current_position = current_position
		self.pickup_to_delivery = c.copy(pickup_to_delivery)
		self.delivery = c.copy(delivery)
		self.vertices_status = c.copy(vertices_status)# (0,1) -> boolean
		self.world = c.deepcopy(world)

	def __str__(self):
		s = "Current vertex: " + str(self.current_position) + "\n{"
		for vertex in self.vertices_status:
			s += str(vertex) + ": " + str(self.vertices_status[vertex])+"\n"
		return s+"}"

	def visit_current_vertex(self):
		self.vertices_status[self.current_position] = True



		
	def visit_current_vertex_if_you_near(self):
		if self.current_position in self.vertices_status.keys():
			self.visit_current_vertex()
				

	def get_unvisited_vertices(self):
		packages = []
		delivery = []
		for pickup in self.pickup_to_delivery.keys():
			if not self.vertices_status[pickup]:
				packages.append(pickup)
			elif not self.vertices_status[self.pickup_to_delivery[pickup]]:
				delivery.append(self.pickup_to_delivery[pickup])

		return packages,delivery +self.delivery,self.pickup_to_delivery


	def move(self,direction):
		prev = self.current_position
		self.current_position = (self.current_position[0] +direction[0],self.current_position[1] + direction[1])
		if(prev,self.current_position) in self.world.fragile_edges:
			self.world.add_blocked_edge(prev[0],prev[1],self.current_position[0], self.current_position[1])
			self.world.remove_fragile_edge(prev[0],prev[1],self.current_position[0], self.current_position[1])
		






