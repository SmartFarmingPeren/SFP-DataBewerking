from OpenGL.GL import *
from openalea.plantgl.gui.editablectrlpoint import *
import openalea.mtg.algo as mtgalgo

import math

import os
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import logging

def create_mtg(file_name):
    sc = Scene(file_name)
    points = sc[0].geometry.geometry
    pmin, pmax = points.getBounds()
    initp = (pmax + pmin) / 2
    initp.z = pmin.z
    root = points.findClosest(initp)[0]
    print(root)

    #
    # def setMTG(self, mtg, fname):
    #     self.mtg = mtg
    #     self.mtgfile = fname
    #
    #     self.selection = None
    #     self.focus = None
    #
    #     self.__update_all_mtg__()

def main():
    # Get the folder where the pointclouds are stored.
    base_dir = os.getcwd()
    input_folder = r"/input_tree_scans/"
    input_folder = base_dir + input_folder
    input_folder = input_folder.replace("\\", "/")
    input_files = os.listdir(input_folder)

    # Loop trough each input file recursively(might add multi processing later)
    for file in input_files:
        create_mtg(input_folder + file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/