import numpy as np
from openalea.plantgl.math import Vector3

from classes_code.JSONTreeLoader import write
from classes_code.Tree import Tree


def main():
    input_point_cloud_name = "gen_9_15_04_expanded.ply"
    tree = Tree(input_point_cloud_name)
    write(tree)


if __name__ == '__main__':
    main()
