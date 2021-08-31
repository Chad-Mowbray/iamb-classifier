from .combinations_base import CombinationsBaseMixin
from .graph_base import GraphBase



class CombinationsGraph(CombinationsBaseMixin, GraphBase):
    """
    Uses CombinationsBaseMixin and GraphBase to construct new stress patterns for lines
    """

    def __init__(self, lines, product_possibles, is_odd_postition, target_stress):
        super().__init__(lines, product_possibles, is_odd_postition, target_stress)
        self.new_combinations = []
        self._all_paths = []
        self._path = []
        self._graph = {}

        self._main()


    def _final_processing(self):
        new_combinations = []
        for line in self._all_paths:
            new_line = [w[1] for w in line[1:]]
            new_combinations.append(tuple(new_line))
        self.new_combinations = new_combinations
        

    def _main(self):
        self._get_line_combinations()
        self._get_all_paths(0,len(self._graph) -1)
        self._final_processing()
