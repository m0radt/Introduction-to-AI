import random
class PriorityQueue(object):

    def __init__(self, f):
        self.queue = []
        self.f = f

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0
    def not_empty(self):
        return len(self.queue) != 0

    def insert(self, data):
        self.queue.append(data)
    def insert_all(self, data_list):
        for data in data_list:
            self.queue.append(data)

    def pop(self):
        if self.is_empty():
            return None
        min_indexs = []
        min_value = self.f(self.queue[0])
        for i in range(len(self.queue)):
            current_f = self.f(self.queue[i])
            if current_f < min_value :
                min_indexs = [i]
                min_value = current_f
            elif current_f == min_value :
                min_indexs.append(i)
        min_index = random.choice(min_indexs)
        item = self.queue[min_index]
        # print(mst_heuristic(item))
        del self.queue[min_index]
        return item
    def mapf(self):
        l =[]
        for x in self.queue:
            l.append(self.f(x))
        return l


