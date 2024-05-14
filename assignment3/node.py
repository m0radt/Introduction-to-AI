from table import Table


class Node:

    def __init__(self, name: str, table: Table , parents = None ):
        self.name = name
        self.table = table
        
        self.parents = [] if parents is None else parents 
        
    def get_values(self):
        return self.table.values

    def __str__(self):
        s = ""
        s += "Node Name: " + self.name + "\n"
        s += '\nparents: \n'
        s += str([parent.name for parent in self.parents])
        s += '\n'
        s += "Probability Table: " + "\n"
        s += "-------------------------------\n"
        for i, value in enumerate(self.table.values):
            for table_entry in self.table.probabilities.keys():
                
                
                prob = round(self.table.probabilities.get(table_entry)[i], 3)
                if table_entry == ():
                    s += "P(" + self.name + " = "+ str(value) + ") = " + str(
                    prob) + "\n"
                else:
                    s += "P(" + self.name + " = "+ str(value) +" |  " + str(table_entry) + ") = " + str(
                    prob) + "\n"

                
        s += "-------------------------------\n\n"
        return s
