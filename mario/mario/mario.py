import cv2
import numpy as np
import random
import os

from tree.tree import *

class Mario:

    def __init__(self):

        self.sprite = 25
        self.position_mario = (0, 0)

        self.map_path = r"C:\Users\jeanbaptiste\Desktop\mario\map\map.txt"
        path_picture_of_mario = r"C:\Users\jeanbaptiste\Desktop\mario\mario\mario.jpg"
        self.picture_of_mario = cv2.resize(cv2.imread(path_picture_of_mario), (self.sprite, self.sprite))

        self.last_movement_of_mario = self.sprite
        self.basics_movements = ["d", "g", "h", "b", "h"]

        self.movements = {"d": (self.sprite, 0), "g": (-self.sprite, 0), "b": (0, self.sprite), "h": (0, -self.sprite)}

        self.map_liste = [[j for i in line for j in i] for line in open(self.map_path, "r")]

        self.recompense_position = []
        self.poison_position = []
        self.recuperate_position_recompense()

        self.height_picture = len(self.map_liste) * self.sprite
        self.width_picture  = len(self.map_liste[0]) * self.sprite
        self.issus_interest = ("a", "r")


    # MOVEMENTS OF MARIO
    def can_mario_make_the_movement(self, new_move):

        liste = [line[:-1] if line[-1] == "\n" else line for line in self.map_liste]

        x_move, y_move = new_move
        x_file, y_file = [ int( abscisse // self.sprite ) for abscisse in [x_move, y_move] ]

        y_cond = 0 <= y_file < len(liste)
        x_cond = 0 <= x_file < len(liste[0])

        return True if (y_cond and x_cond and liste[y_file][x_file] is not "1") and\
                       (0 <= x_move < self.width_picture and 0 <= y_move < self.height_picture) else False


    def tree_from_case_position_of_mario(self, road_convert_to_position):
        """
            mario position: (50, 100)

            tree: [ ( [dddgggt], [(25, 0), (50, 0), (75, 0) ... (50, 100), (75, 100)] ),
                    ( [dddhbht], [(25, 0), (50, 0), (75, 0) ... (50, 100), (25, 100)] ) 
                  ]

            result: [ [ ggt, (50, 100), (75, 100) ], [ hbh, (50, 100), (25, 100) ] ]

            out: [ggt, hbh]

        """

        tree_from_position = []

        for road in road_convert_to_position:

            index_cases = [index for index, case in enumerate(road) if case == self.position_mario]
            if len(index_cases) > 0:
                index_case = index_cases[-1]
                road_lettre = [i for i in road[-1][index_case:]]
                tree_from_position += [road_lettre]

        return tree_from_position



    def recuperate_score_case_issu(self, branchs):

        """
        case_issus = [(g, a), (d, t), (h, t), (d, t), (h, a)]

        probability: [{d: 2/4, g: 1/4, h: 1/4}]
 
        issus = {
            g: {a: 1, t: 0, r: 0, total: 1},
            d: {a: 0, t: 2, r: 0, total: 2},
            h: {a: 1, t: 1, r: 0, total: 2}
        }

        issus_proba = {
            {g: a: 1.0, r: 0},
            {d: a: 0, r: 0},
            {h: a: 0.5, r:0.5},
        }

        out = {
            {g: a: (2/4) * 1.0, r: (2/4) * 0},
            {d: a: (1/4) * 0, r: (1/4) * 0},
            {h: a: (1/4) 0.5, r: (1/4) * 0.5},
        }

        """

        case_issus = [(branch[0], branch[-1]) for branch in branchs if len(branch) > 1]
        case = [branch[0] for branch in branchs]

        case_issus_set = list(set(case))

        nodes = {i: case.count(i) / len(case_issus) for i in case_issus_set if len(case_issus) > 0 and i in ["d", "h", "g", "b"]}
        issus = {i: {"a":0, "r":0, "t":0, "total": 0} for i in case_issus_set if i in ["d", "h", "g", "b"]}

        for (start, end) in case_issus:
            if start in issus and end in issus[start]:
                issus[start][end] += 1
                issus[start]["total"] += 1

        for case, data in issus.items():
            if issus[case]["total"] > 0:
                issus[case] = {
                    "a": issus[case]["a"] / issus[case]["total"], 
                    "r": issus[case]["r"] / issus[case]["total"], 
                }

        return issus



    def try_issus_if_thresholsd(self, issus):
        """

        case = {
            g: {a: 0, r: 1}
            d: {a: 0, r: 0.5}
        }

        movement_to_feed_back = [(g, r)]
        movement_gradient = [d]

        """

        movement_gradient = []
        movement_to_feed_back = []

        for case, probs in issus.items():
            issu, prob = sorted(probs.items(), key=lambda item: item[1])[::-1][0]
            data = (prob, case, issu)
            if prob >= 0.6 and issu in self.issus_interest:
                movement_to_feed_back += [data]
            if 0.6 > prob >= 0.4 and issu in self.issus_interest:
                movement_gradient += [data]

        force_movement = None
        movement_to_feed_back = sorted(movement_to_feed_back)[::-1]
        if len(movement_to_feed_back) > 0:
            prob, move, issu = movement_to_feed_back[0]
            if issu in self.issus_interest:
                force_movement = (move, issu)

        return force_movement, movement_gradient


    def probability_case(self, movement_gradient):
        """
            movement_gradient = [
                (0.5, g, t),
                (0.6, d, r),
                (0.5, h, t),
            ] 
            movement_gradient = [
                (0.6, d, r),
                (0.5, g, t),
                (0.5, h, t),
            ]
            out = d or None
        """

        case = sorted(movement_gradient)[::-1][0][1] if len(movement_gradient) > 0 else None
        return case


    def recuperate_new_movement(self, move):
        movement = self.position_mario
        if move in self.movements:
            x_move, y_move = self.movements[move]
            x, y = self.position_mario
            movement = (x + x_move, y + y_move)
        return movement


    def is_a_forced_movement_to_try(self, movement_forced, last_position, current_position, not_out_of_the_map):
        """
            proba = { g: {"a": 0, "r":1 } }
            movement_forced = g
            if g case is not "r":
                 issus_forced = "t"
            
            if issus_forced == "t":
                break loop
            
            break loop == mario death
        """

        _, issu = movement_forced

        mario_has_no_moved = last_position == current_position
        is_not_a_recompense = current_position not in self.recompense_position
        is_an_issu_recompense = issu in self.issus_interest

        issus_forced = "t" if (mario_has_no_moved or is_not_a_recompense) and is_an_issu_recompense else None

        if not_out_of_the_map:
            self.position_mario = current_position  

        return issus_forced


    def probabily_movement(self, to_try_grad, new_movement, move, not_out_of_the_map):

        # Gradient
        if to_try_grad is not None:
            move = to_try_grad
            new_movement = self.recuperate_new_movement(to_try_grad)
            if self.can_mario_make_the_movement(new_movement):
                self.position_mario = new_movement

        elif to_try_grad is None and not_out_of_the_map:
            self.position_mario = new_movement

        return move


    def has_already_found_recompense(self, recompense_found, road_convert_to_position):
        
        tree_from_position = []

        for road in road_convert_to_position:

            if road[-1] in self.issus_interest:
                issu = road[-2]
                if issu not in recompense_found:
                    tree_from_position += [road]

        return tree_from_position


    def movement_of_mario(self, road_convert_to_position, recompense):

        last_position = self.position_mario

        move = random.choice(self.basics_movements)

        #road_convert_to_position = self.has_already_found_recompense(recompense, road_convert_to_position)
        branchs = self.tree_from_case_position_of_mario(road_convert_to_position)

        issus = self.recuperate_score_case_issu(branchs)
        to_try, to_grad = self.try_issus_if_thresholsd(issus)
        to_try_grad = self.probability_case(to_grad)

        move = move if to_try is None else to_try[0]
        is_move_to_try = False if to_try is None else True

        new_movement = self.recuperate_new_movement(move)
        not_out_of_the_map = self.can_mario_make_the_movement(new_movement)

        to_do = None

        if not is_move_to_try:
            move = self.probabily_movement(to_try_grad, new_movement, move, not_out_of_the_map)

        elif is_move_to_try:
            to_do = self.is_a_forced_movement_to_try(to_try, last_position, new_movement, not_out_of_the_map)
            if to_do is None:
                to_do = "s"

        return move, to_do


    # CASE STOP A TURN
    def has_found_recompense(self):
        return True if self.position_mario in self.recompense_position else False

    # INIT CLASS
    def recuperate_position_recompense(self):
        self.recompense_position = [(x * self.sprite, y * self.sprite) for y, line in enumerate(self.map_liste)
                                    for x, _ in enumerate(line) if self.map_liste[y][x] == "R"]

    # DISPLAYING OF MARIO
    def initialisation_mario_position(self):
        self.position_mario = ( 0, (self.height_picture - self.sprite) )

    def getter_position_mario(self):
        return self.position_mario

    def blit_mario_on_picture(self, picture):
        x, y = self.position_mario
        picture[y:y+self.sprite, x:x+self.sprite] = self.picture_of_mario