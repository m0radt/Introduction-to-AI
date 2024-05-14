

def make_table(entries: list, values: list, evidences: list, var_values: list = None):
	table = Table(evidences,var_values)
	entries_values = zip(entries, values)
	for entry_value in entries_values:
		entry = entry_value[0]
		value = entry_value[1]
		table.add_entry(entry, value)
	return table


class Table:

	def __init__(self, evidences, var_values):
		self.probabilities = {}
		self.evidences = evidences	
		self.values = [True, False] if var_values is None else var_values

	# entry is a row in the prob table. for example T T 0.4
	def add_entry(self, tuples: list, value: float):
		if tuples[0] == ():
			self.probabilities[()] = value
		else:
			if len(tuples) > 1:
				self.probabilities[tuple(tuples)] = value
			else:
				self.probabilities[tuples[0]] = value
	# def reset_probabilities(self,  entries: list, values: list):
	# 	self.probabilities.clear()
	# 	entries_values = zip(entries, values)
	# 	for entry_value in entries_values:
	# 		entry = entry_value[0]
	# 		value = entry_value[1]
	# 		self.add_entry(entry, value)
		

	def get_probability_given_parents(self, value , parents: list) -> float:
		# parents should be list of tuble os this form (varible,(true/false))
		parents_tuple = None
		if len(parents) == 0:
			return self.probabilities[()][self.values.index(value)]
		elif len(parents) == 1:
			parents_tuple = parents[0]

		else:
			#sort parents according to element of evidences
			parents.sort( key=lambda x: self.evidences.index(x[0]))
			parents_tuple = tuple(parents)

		return self.probabilities[parents_tuple][self.values.index(value)]

			



