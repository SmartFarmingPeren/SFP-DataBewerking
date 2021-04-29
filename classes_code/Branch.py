import numpy as np

from classes_code.Point import Point


class Branch:
    def __init__(self, v_array: np.array=None, age: int=None, child: 'Branch'=None):
        self.v_array = v_array
        self.age = age
        self.children = [child]
        print(self.children)

    def __str__(self):
        return "Branch age %d, children: %s" % (self.age, self.children)