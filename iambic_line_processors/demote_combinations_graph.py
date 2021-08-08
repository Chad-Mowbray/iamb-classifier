from copy import deepcopy
import itertools

class DemoteCombinationsGraph:

    def __init__(self, lines):
        self.all_paths = []
        self.path = []
        self.lines = lines
        self.graph = {}
        self.new_combinations = []

        self.main()

    def get_word_combinations(self, word, primary_stress_idxs):
        possible_words = []
        for possible in itertools.product([2, 1],repeat=len(primary_stress_idxs)):
            word_copy = [s for s in word]
            for i,p in enumerate(possible):
                for j,s in enumerate(word_copy):
                    if j != primary_stress_idxs[i]:
                        word_copy[j] = s
                    else:
                        word_copy[j] = p            
            possible_words.append(word_copy)
        return possible_words


    def get_line_combinations(self):
        line_pos = 0
        for line in self.lines:
            temp_line = []
            for word in line:
                if len(word) < 2:
                    line_pos += len(word)
                    temp_line.append([word])
                    continue
                primary_stress_idxs = [i for i,syl in enumerate(word) if (i + line_pos) % 2 == 0 and syl == 1]
                if primary_stress_idxs:
                    word_combinations = self.get_word_combinations(word, primary_stress_idxs)
                    temp_line.append(word_combinations)
                else:
                    temp_line.append([word])
                line_pos += len(word)
            line_pos = 0
            self.build_graph(temp_line)


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
            # ([0], [0], [0], [1], [0, 1], [0, 1, 0, 0]),
            ([1], [0, 1, 2, 0, 2], [1], [1], [1, 2]),
            ]
    all_lines = []
    for line in lines:
        cg = DemoteCombinationsGraph([line])
        new_combos = cg.new_combinations
        for new_combo in new_combos:
            all_lines.append(new_combo)
    pprint(all_lines)