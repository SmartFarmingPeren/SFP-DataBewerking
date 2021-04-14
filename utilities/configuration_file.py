import os

# [Directory static values]
# CWD
CURRENT_WORKING_DIR = os.getcwd().replace("\\", "/").split("utilities")[0]
# Experimental dir
EXPERIMENTAL_DIR = CURRENT_WORKING_DIR + "experimental/"
# Graphs dir
GRAPHS_DIR = CURRENT_WORKING_DIR + "graphs/"
# Input dirs
INPUT_DIR = CURRENT_WORKING_DIR + "input/"
INPUT_POINT_CLOUDS_DIR = INPUT_DIR + "point_clouds/"
# Output dirs
OUTPUT_DIR = CURRENT_WORKING_DIR + "outputs/"
OUTPUT_BMTG_DIR = OUTPUT_DIR + "bmtg_files/"
OUTPUT_GRAPHS_DIR = OUTPUT_DIR + "graphs/"
OUTPUT_MTG_DIR = OUTPUT_DIR + "mtg_files/"
# Skeletonization dir
SKELETONIZATION_DIR = CURRENT_WORKING_DIR + "skeletonization/"
# Utilities dir
UTILITIES_DIR = CURRENT_WORKING_DIR + "utilities/"


