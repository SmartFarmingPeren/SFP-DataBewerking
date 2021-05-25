from classes_code.JSONTreeLoader import write
from classes_code.Tree import Tree


def main():
    input_point_cloud_name = "Simpele_boom.ply"
    tree = Tree(input_point_cloud_name)
    write(tree)


if __name__ == '__main__':
    main()
