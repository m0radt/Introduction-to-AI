
class TreeNode(object):
	def __init__(self, state, parent, acc_weight, depth,move):
		self.state = state
		self.parent = parent
		self.acc_weight = acc_weight
		self.depth = depth
		self.move = move



def get_vertices_list_as_string(vertices_list):
	s = "[ "
	for vertex in vertices_list:
		s += str(vertex) + ", "
	last_index_of_comma = s.rfind(",")
	if last_index_of_comma != -1:
		s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]

	return s + "]"
