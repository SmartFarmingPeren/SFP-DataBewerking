import openalea.plantscan3d.mtgmanip as mm
from openalea.plantgl.math._pglmath import Vector3
from openalea.plantgl.scenegraph._pglsg import Scene
from openalea.plantscan3d.xumethod import xu_method


def setup():
    root = Vector3(0, 0, 0)
    mtg = mm.initialize_mtg(root)
    return mtg


def skeleton(mtg, points, binratio=50, k=30):
    mini, maxi = points.getZMinAndMaxIndex()
    root = Vector3(points[mini])
    mtg = mm.initialize_mtg(root)
    zdist = points[maxi].z - points[mini].z
    binlength = zdist / binratio
    vtx = list(mtg.vertices(mtg.max_scale()))
    startfrom = vtx[0]
    xu_method(mtg, startfrom, points, binlength)
    return mtg


def main():
    mtg = setup()  # van roy zn code
    stack_split = []
    scene = Scene('D:/ProjectMinor/Simpele_boom.ply')
    points = scene[0].geometry.pointList
    points.swapCoordinates(1, 2)
    mtg = setup()
    mtg = skeleton(mtg, points)

    for x in mtg.vertices():
        test = mtg.Sons(x, EdgeType='*')  # blijkbaar werkt dit? aantal zonen geboren uit x
        # print(x ," heeft de zonen vertex: ", test)
        # print("")
        if len(test) == 0:  # de laatste tak
            # print(x, "heeft geen zonen, dus is eerste jaars")
            predecessor = mtg.Father(x)  # ga terug en check de aantal zonen dit moet een 2 jaars tak zijn
            if predecessor is not None:
                # print("de vader: ",predecessor)
                zonen = mtg.Sons(predecessor, EdgeType='*')
                # print("de zonen van de vader zijn ", zonen)
                if len(zonen) == 1:
                    print(zonen, "snij 5 cm van de fork")
                if len(zonen) > 1:
                    print(zonen,
                          "snijd de hoogste 1e jaars tak 5 cm, rest kort op de tak.")  # kijken hoe dit vertaalt naar nodes
            elif predecessor is None:
                continue

        if mtg.Father(mtg.Father(x)) is None:  # als er geen opa is, dus de vader van de root bestaat niet
            if mtg.Father(x) is not None:
                print("")
                print("leiders zijn ", x, "en heeft zoon", mtg.Sons(x, EdgeType='*'))
                for u in mtg.Sons(x, EdgeType='*'):  # kinderen van de leider
                    is_empty = len(mtg.Sons(u, EdgeType='*'))
                    if is_empty:  # eerste jaars tak
                        print(u, "snoei 5 cm van de top")
                print("")


if __name__ == '__main__':
    main()
