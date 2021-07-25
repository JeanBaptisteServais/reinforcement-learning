import cv2
import numpy as np


class Map:

    def __init__(self):

        self.map_path = r"C:\Users\jeanbaptiste\Desktop\mario\map\map.txt"
        self.sprite = 25

        self.map_liste = [[j for i in line for j in i] for line in open(self.map_path, "r")]
        self.height = len(self.map_liste) * self.sprite
        self.width = len(self.map_liste[0]) * self.sprite


    def make_rectangles(self, picture):
        """Draw case of the map"""
        [cv2.rectangle(picture, (x, y), (x + self.sprite, y + self.sprite), (0, 0, 0), 1)
        for y in range(0, self.height, self.sprite) for x in range(0, self.width, self.sprite)]


    def display_recompense(self, liste_recompense):
        """Display recompense"""

        picture = 255 * np.ones((self.height, self.width, 3), np.uint8)

        self.make_rectangles(picture)
        self.make_arrival(picture)

        for (x_, y_) in liste_recompense:
            picture[y_:y_+self.sprite, x_:x_+self.sprite] = (255, 0, 0)

        for y, line in enumerate(self.map_liste):
            for x, case in enumerate(line):
                if self.map_liste[y][x] == "1":
                    x_ = x * self.sprite
                    y_ = y * self.sprite
                    picture[y_:y_+self.sprite, x_:x_+self.sprite] = (42, 42, 165)

        return picture


    def make_brique(self, picture):
        """Display wall"""

        dico_color = {"1": (42, 42, 165), "R": (255, 0, 0)}

        for y, line in enumerate(self.map_liste):
            for x, case in enumerate(line):

                x_ = x * self.sprite
                y_ = y * self.sprite

                try:
                    picture[y_:y_+self.sprite, x_:x_+self.sprite] = dico_color[self.map_liste[y][x]]
                except:
                    pass

    def make_arrival(self, picture):
        """Display arrival"""
        picture[self.height-self.sprite: self.height, 2*self.sprite:(2*self.sprite)+self.sprite] = (0, 255, 0)
        return picture, (2*self.sprite, self.height-self.sprite)

    def generate_map(self):
        """Create map"""
        picture = 255 * np.ones((self.height, self.width, 3), np.uint8) # map
        self.make_brique(picture)
        self.make_rectangles(picture)

        return picture
