
# generate perso
# generate objet
# generate mario

# boucle
#   mouvement perso
#   tree
#   action mario
#   mouvement mario
#   refresh picture
#   tree

import cv2
import numpy as np

from map.map import *
from mario.mario import *
from tree.tree import *

class Main:
    """Lunch loop,
    recuperate gesture of mario,
    controle tree"""

    def __init__(self):
        """Contructor"""

        self.map_constructor = Map() # Generate map
        self.mario = Mario() # mario control
        self.tree = Tree() # tree

        self.pause = 0

    def display_picture(self, picture):
        cv2.imshow("picture", picture)
        if cv2.waitKey(self.pause) & 0xFF == ord('a'):
            self.pause = 0 if self.pause == 1 else 1



    def mario_and_recompense(self, arrival, death, action_by_mario, 
    position_of_mario, has_found_recompense, is_recompense):

        turn_off = False

        if position_of_mario == arrival and arrival is not None:
            self.tree.end_of_turn("a", None, None)
            turn_off = True

        if death == "s" and position_of_mario not in has_found_recompense:
            has_found_recompense += [position_of_mario]

        if death == "t" and position_of_mario in has_found_recompense:
            has_found_recompense.remove(position_of_mario)
            self.tree.end_of_turn("t", None, None)
            turn_off = True

        elif is_recompense and position_of_mario not in has_found_recompense:
            self.tree.end_of_turn("r", action_by_mario, position_of_mario)
            has_found_recompense += [position_of_mario]

        return turn_off


    def end_of_a_turn(self):
        self.tree.end_of_turn("t", None, None)
        self.tree.save_branch_in_tree()
        self.tree.recuperate_proba_of_tree()


    def main(self):

        # Stop a turn of mario
        session = 200

        while True:

            self.mario.initialisation_mario_position()
            self.tree.create_branch()

            self.mario.recuperate_position_recompense()

            has_found_recompense = []
            arrival = None

            for turn in range(session):

                picture = self.map_constructor.generate_map()

                if len(has_found_recompense) == 5:
                    picture, arrival = self.map_constructor.make_arrival(picture)

                road_convert_to_position = self.tree.getter_position_case()
                action_by_mario, death = self.mario.movement_of_mario(road_convert_to_position, has_found_recompense)

                self.mario.blit_mario_on_picture(picture)

                position_of_mario = self.mario.getter_position_mario()
                self.tree.save_action_in_branch(action_by_mario, position_of_mario)

                self.display_picture(picture)

                is_recompense = self.mario.has_found_recompense()

                if self.mario_and_recompense(arrival, death, action_by_mario, 
                    position_of_mario, has_found_recompense, is_recompense):
                    break

            self.end_of_a_turn()
 















if __name__ == "__main__":

    main = Main()
    main.main()


