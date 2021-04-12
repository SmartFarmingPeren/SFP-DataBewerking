from OpenGL.GL import *
from openalea.plantgl.gui.editablectrlpoint import *
import openalea.mtg.algo as mtgalgo

import math

import os
import sys
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def create_tmg():
    file_name = 'pointcloud.ply'
    sc = Scene(file_name)
    points = sc[0].geometry.geometry
    pmin, pmax = points.getBounds()
    initp = (pmax + pmin) / 2
    initp.z = pmin.z
    root = points.findClosest(initp)[0]


    def setMTG(self, mtg, fname):
        self.mtg = mtg
        self.mtgfile = fname

        self.selection = None
        self.focus = None

        self.__update_all_mtg__()

def main():
    import sys, os
    #print("test2")
    f = open("luca.txt", "w+")
    f.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/