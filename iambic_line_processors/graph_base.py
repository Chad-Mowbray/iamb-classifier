from copy import deepcopy



class GraphBase():
    """
    Basic implementation of graph traversal to get all possible paths
    """

    def _build_graph(self, temp_line):
        graph = {i + 1: x for i,x in enumerate(temp_line) }
        for k,v in graph.items():
            graph[k] = tuple((k + 1,word) for word in v)
        graph[0] = ((1,[]),)
        graph[k+1] = ((),)
        self._graph = graph


    def _get_all_paths(self, current, end):
        if current == end:
            self._all_paths.append(deepcopy(self._path))
            return
        else:
            for sister in self._graph[current]:
                self._path.append(sister)
                self._get_all_paths(sister[0], end)
                self._path.pop()

