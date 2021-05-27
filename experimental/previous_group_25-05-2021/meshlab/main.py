import pymeshlab

from utilities.configuration_file import *
from utilities.test_functions import *


def convert_xyz_to_ply_and_filter_points(mesh_set):
    thick_mesh_files = os.listdir(INPUT_MESHES_DIR)
    index = 0
    for thick_mesh in thick_mesh_files:
        if file_is_not_git_file(thick_mesh):
            # Load and set mesh
            mesh_set.load_new_mesh(INPUT_MESHES_DIR + thick_mesh)
            mesh_set.set_current_mesh(index)
            # Filter points
            mesh_set.simplification_clustering_decimation(threshold=0.5)
            # Save mesh as ply
            thick_mesh = thick_mesh.split(".")[0]
            mesh_set.save_current_mesh(OUTPUT_MESHES_DIR + thick_mesh + ".ply")
            # Repeat
            index += 1


def main():
    mesh_set = pymeshlab.MeshSet()
    convert_xyz_to_ply_and_filter_points(mesh_set)
    mesh_set.clear()


if __name__ == '__main__':
    main()
