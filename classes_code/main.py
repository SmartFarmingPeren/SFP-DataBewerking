from classes_code.JSONTreeLoader import write
from classes_code.Tree import Tree


def main():
    """
    This is the main code used to create a tree object and divide the object into different branches.
    """
    input_point_cloud_name = "Simpele_boom.ply"
    tree = Tree(input_point_cloud_name)
    write(tree)


if __name__ == '__main__':
    main()
