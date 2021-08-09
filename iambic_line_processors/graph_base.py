from copy import deepcopy


class GraphBase:

    def __init__(self):
        self.all_paths = []
        self.path = []
        self.graph = {}
        self.new_combinations = []


    def build_graph(self, temp_line):
        graph = {i + 1: x for i,x in enumerate(temp_line) }
        for k,v in graph.items():
            graph[k] = tuple((k + 1,word) for word in v)
        graph[0] = ((1,[]),)
        graph[k+1] = ((),)
        self.graph = graph


    def get_all_paths(self, current, end):
        if(current == end):
            self.all_paths.append(deepcopy(self.path))
            return
        else:
            for sister in self.graph[current]:
                self.path.append(sister)
                self.get_all_paths(sister[0], end)
                self.path.pop()
