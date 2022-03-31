import datetime
import time

from classes_code.JSONTreeLoader import write, read
from classes_code.Tree import Tree


def main():
    """
    This is the main code used to create a tree object and divide the object into different branches.
    """
    start_time = time.time()
    input_point_cloud_name = "iPad.ply"
    tree = Tree(input_point_cloud_name)
    write(tree)
    # tree_copy = read("gen_9_15_04_expanded.json")
    print("Runtime: {0} seconds".format((time.time() - start_time)))


if __name__ == '__main__':
    main()
