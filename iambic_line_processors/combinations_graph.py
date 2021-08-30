from iambic_line_processors.combinations_base import CombinationsBaseMixin
from iambic_line_processors.graph_base import GraphBase



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



if __name__ == "__main__":
    from pprint import pprint

    # lines = [
    #         ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]),
    #         ([0], [0], [0], [1], [1, 2], [0, 1, 0, 0]),
    #         ]
    # all_lines = []
    # for line in lines:
    #     cg = CombinationsGraph([line])
    #     new_combos = cg.new_combinations
    #     for new_combo in new_combos:
    #         all_lines.append(new_combo)
    # pprint(all_lines)