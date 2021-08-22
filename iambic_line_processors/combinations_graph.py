from iambic_line_processors.combinations_base import CombinationsBaseMixin
from iambic_line_processors.graph_base import GraphBase


# class CombinationsGraph(GraphBase, CombinationsBaseMixin):
class CombinationsGraph(CombinationsBaseMixin, GraphBase):

    """
    Uses CombinationsBaseMixin and GraphBase to construct new stress patterns for lines
    """

    def __init__(self, lines, product_possibles, is_odd_postition, target_stress):
        super().__init__(lines, product_possibles, is_odd_postition, target_stress)
        self.all_paths = []
        self.path = []
        self.graph = {}
        self.new_combinations = []

        self.main()


    def final_processing(self):
        new_combinations = []
        for line in self.all_paths:
            new_line = [w[1] for w in line[1:]]
            new_combinations.append(tuple(new_line))
        self.new_combinations = new_combinations
        

    def main(self):
        self.get_line_combinations()
        self.get_all_paths(0,len(self.graph) -1)
        self.final_processing()



if __name__ == "__main__":
    from pprint import pprint

    lines = [
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]),
            ([0], [0], [0], [1], [1, 2], [0, 1, 0, 0]),
            ]
    all_lines = []
    for line in lines:
        cg = CombinationsGraph([line])
        new_combos = cg.new_combinations
        for new_combo in new_combos:
            all_lines.append(new_combo)
    pprint(all_lines)