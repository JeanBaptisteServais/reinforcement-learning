# créer une branche
# save action in branch
# save branch in tree
# recup proba de tree
# convert road to (x, y)

import os



class Tree:

    def __init__(self):
        self.tree = []
        self.tree_position = []
        self.probabilities = []

    # CONTAINERS TREE
    def create_branch(self):
        self.branch = []
        self.branch_position = [(0, 100)]

    def save_action_in_branch(self, action, position):
        self.branch += [action]
        self.branch_position += [position]


    def save_branch_in_tree(self):
        if self.branch_position not in self.tree_position:
            self.tree += [self.branch]
            self.tree_position += [self.branch_position]

    def end_of_turn(self, issus, action, position):

        if len(self.branch) > 0 and self.branch[-1] not in ["a", "t", "r"]:
            if issus != "r":
                self.branch += [issus]
                self.branch_position += ["".join(self.branch)]

            elif issus == "r":

                self.branch += ["r"]
                self.branch_position += ["".join(self.branch)]

                self.save_branch_in_tree()

                #self.recuperate_proba_of_tree()
                self.branch = []
                self.branch_position = [position]


        print(self.branch_position)


    # PROBABILITIES
    def recuperate_branch_of_tree(self, tree):

        dico = {}

        for branch in tree:
            for n in range(len(branch) + 1):

                data = "".join(branch[:n])
                if data is not "" and data not in dico:
                    dico[data] = 1
                elif data is not "" and data in dico:
                    dico[data] += 1


        return dico


    def recuperate_nodes_of_branchs(self, length, dico):
        nodes = []
        for n in range(1, length + 1):
            nodes += [ [ [k, v] for k, v in dico.items() if len(k) == n ] ]
        return nodes


    def scoring_branch_of_tree(self, liste):

        liste2 = []
        for nb, i in enumerate(liste):
            liste_work = []
            if nb == 0:
                total = sum([n for move, n in i])
                for j in i:
                    j += [total]
                    liste_work += [j]

            else:
                for j in i:
                    last = j[0][:-1]
                    total = 0

                    for (move, score, total) in liste[nb - 1]:
                        if move == last:
                            total = score
                            break
                    j += [total]
                    liste_work += [j]
            liste2 += [liste_work]

        return liste2


    def recuperate_probabilities(self, branchs_nodes):
        probabilities = []
        for nodes in branchs_nodes:
            data = [(road, f"{nb_move}/{total_move}") for (road, nb_move, total_move) in nodes]
            probabilities += [data]
        return probabilities


    def recuperate_proba_of_tree(self):

        max_length_of_a_branch = max([len(branch) for branch in self.tree])

        branchs = self.recuperate_branch_of_tree(self.tree)
        branchs_nodes = self.recuperate_nodes_of_branchs(max_length_of_a_branch, branchs)
        score_tree = self.scoring_branch_of_tree(branchs_nodes)
        self.probabilities = self.recuperate_probabilities(score_tree)


    def getter_probabilities(self):
        return self.probabilities

    def getter_position_case(self):
        return self.tree_position




