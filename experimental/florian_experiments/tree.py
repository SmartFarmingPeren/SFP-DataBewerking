from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
import openalea.plantscan3d.mtgmanip as mm
from openalea.plantscan3d.xumethod import xu_method
import branch as br


class Boom:
    def __init__(self, zooi):
        tree = self.setup()  # van roy zn code
        stack_split = []
        print("1")
        scene = Scene(zooi)
        print("2")
        points = scene[0].geometry.pointList
        print("3")
        points.swapCoordinates(1, 2)
        print("4")
        self.tree = self.setup()
        print("5")
        self.tree = self.skeleton(tree, points)
        print("6")
        self.branche = list()  # ff dit voor testing purposes, anders functie maken die alle takken maakt
        print("Tree loaded")

    def getBranches(self):
        print("hoe de fuck komt het programma al hier")
        i = 0
        self.branche.append(br.branch())  # init
        print(self.branche[i].end)
        for x in self.tree.vertices():  # moet in principe vanaf een bepaalde tak array beginnen. voor nu nog hele boom.
            if self.branche[i].makenext == 1:
                print("creating new branch")
                i = i + 1
                self.branche.append(br.branch())
                self.branche[i].begin = x
                print(self.branche[i-1].end, "en", self.branche[i].begin)
            opslag = len(self.tree.Sons(x, EdgeType='+'))
            if opslag != 0:  # aftakking gevonden
                self.branche[i].makenext = 1
                self.branche[i].end = x
                print("starting new branch")
                continue
            if len(self.tree.Sons(x, EdgeType='<')) == 1:  # groeit door lengte ++1
                self.branche[i].length = self.branche[i].length + 1
            self.branche[-1].end = self.branche[-1].begin + 1 + self.branche[-1].length
        print("last is", self.branche[-1].end)

    def setup(self):
        root = Vector3(0, 0, 0)
        mtg = mm.initialize_mtg(root)
        return mtg

    def skeleton(self, mtg, points, binratio=50, k=30):
        mini, maxi = points.getZMinAndMaxIndex()
        root = Vector3(points[mini])
        mtg = mm.initialize_mtg(root)
        zdist = points[maxi].z - points[mini].z
        binlength = zdist / binratio
        vtx = list(mtg.vertices(mtg.max_scale()))
        startfrom = vtx[0]
        xu_method(mtg, startfrom, points, binlength)
        return mtg


    def branchParent(self, branch):
        self.branches.parent = self.tree.Father(branch)
        return print("parent is ", self.branch.parent)

    # def branchAge(self):

    def SnoeiPlek(self): # deze zooi moet nog wat aanpassingen krijgen. locatie klopt nog niet altijd.
        # TODO: vanaf de leider zoeken, 1 jaar op 3 jaar.
        for x in self.tree.vertices():
            test = self.tree.Sons(x, EdgeType='+')  # blijkbaar werkt dit? aantal zonen geboren uit x
            # print(x ," heeft de zonen vertex: ", test)
            print("")
            if len(test) == 0:  # de laatste tak
                print(x, "heeft geen zonen, dus is eerste jaars")
                predecessor = self.tree.Father(x)  # ga terug en check de aantal zonen dit moet een 2 jaars tak zijn
                if predecessor is not None:
                    print("de vader: ", predecessor)
                    zonen = self.tree.Sons(predecessor, EdgeType='*')
                    print("de zonen van de vader zijn ", zonen)
                    if len(zonen) == 1:
                        print(zonen, "snij 5 cm van de fork")
                    if len(zonen) > 1:
                        print(zonen, "snijd de hoogste 1e jaars tak 5 cm, rest kort op de tak.")  # kijken hoe dit
                        # vertaalt naar nodes
                elif predecessor is None:
                    continue

            if self.tree.Father(self.tree.Father(x)) is None:  # als er geen opa is, dus de vader van de root bestaat
                # niet
                if self.tree.Father(x) is not None:
                    print("")
                    print("leiders zijn ", x, "en heeft zoon", self.tree.Sons(x, EdgeType='*'))
                    for u in self.tree.Sons(x, EdgeType='*'):  # kinderen van de leider
                        is_empty = len(self.tree.Sons(u, EdgeType='*'))
                        if is_empty:  # eerste jaars tak
                            print(u, "snoei 5 cm van de top")
                    print("")
