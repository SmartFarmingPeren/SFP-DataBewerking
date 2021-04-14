from pyvis.network import Network
import networkx as nx

from openalea.plantgl.all import *

from Skeletonization.main import skeleton

scene = Scene('D:/PearTreeDataProcessing/Skeletonization/gen_2_23_03_expanded.ply')
points = scene[0].geometry.pointList

mtg = skeleton(points)
nx_graph = nx.cycle_graph(10)
nx_graph.nodes("MTG(mtg)")


nt = Network('500px', '500px')
# populates the nodes and edges data structures
nt.from_nx(nx_graph)
nt.show('nx.html')