import os

# [Directory static values]
# CWD
PATH_CWD_PARENT = os.path.dirname(os.getcwd())
os.chdir(PATH_CWD_PARENT)
CURRENT_WORKING_DIR = os.getcwd().replace("\\", "/") + "/"
print(CURRENT_WORKING_DIR)
# Experimental dir
EXPERIMENTAL_DIR = CURRENT_WORKING_DIR + "experimental/"
# Graphs dir
GRAPHS_DIR = CURRENT_WORKING_DIR + "graphs/"
# Input dirs
INPUT_DIR = CURRENT_WORKING_DIR + "inputs/"
INPUT_POINT_CLOUDS_DIR = INPUT_DIR + "point_clouds/"
INPUT_MESHES_DIR = INPUT_DIR + "meshes/"
# Output dirs
OUTPUT_DIR = CURRENT_WORKING_DIR + "outputs/"
OUTPUT_BMTG_DIR = OUTPUT_DIR + "bmtg_files/"
OUTPUT_GRAPHS_DIR = OUTPUT_DIR + "graphs/"
OUTPUT_MTG_DIR = OUTPUT_DIR + "mtg_files/"
OUTPUT_LOG_DIR = OUTPUT_DIR + "log_files/"
OUTPUT_MESHES_DIR = OUTPUT_DIR + "meshes/"
# Skeletonization dir
SKELETONIZATION_DIR = CURRENT_WORKING_DIR + "skeletonization/"
# Utilities dir
UTILITIES_DIR = CURRENT_WORKING_DIR + "utilities/"

# [Static file names]
LOG_FILE_NAME = 'code_logging.log'
