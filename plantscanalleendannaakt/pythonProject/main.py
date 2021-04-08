from PyQt5.Qt import *
from OpenGL.GL import *




def importPoints(self):
    fname = QFileDialog.getOpenFileName(self, "Open Points file",
                                        initialname,
                                        "Points Files (*.asc *.xyz *.pwn *.pts *.txt *.bgeom *.xyz *.ply);;All Files (*.*)")
    #if not fname: return
    #fname = str(fname[0])
    self.filehistory.add(fname, 'PTS')
    self.readPoints(fname)
    self.open_file.emit()

def readPoints(self, fname):
    self.progressdialog.setOneShot(True)
    try:
        sc = Scene(fname)
    finally:
        self.progressdialog.setOneShot(False)

    if len(sc) == 0:
        QMessageBox.warning(self, 'file error', 'Not able to read points from file ' + repr(fname))
        return
    try:
        points = sc[0].geometry.geometry
        self.translation = sc[0].geometry.translation
        points.pointList.translate(self.translation)
    except AttributeError:
        points = sc[0].geometry
        self.translation = Vector3(0, 0, 0)
    self.setPoints(points)
    self.showEntireScene()

def setPoints(self, points, keepInfo=False):
    self.points = points

    self.pointsAttributeRep = None
    if not keepInfo:
        self.pointinfo = PointInfo()

    if self.points.colorList is None:
        self.points.colorList = generate_point_color(self.points)

    self.selectBuffSize = len(self.points.pointList) * 5
    self.setSelectBufferSize(self.selectBuffSize)

    self.adjustTo(points)
    self.createPointsRepresentation()

def reorient(self):
    if not self.check_input_points(): return

    self.points.pointList.swapCoordinates(1, 2)
    if self.pointsRep[0].geometry.pointList.getPglId() != self.points.pointList.getPglId():
        self.pointsRep[0].geometry.pointList.swapCoordinates(1, 2)
    self.updateGL()

def addBottomCenterRoot(self):
    if self.points is None:
        root = Vector3(0, 0, 0)
    else:
        points = self.points.pointList
        pmin,pmax = points.getBounds()
        initp = (pmax+pmin)/2
        initp.z = pmin.z
        root = points.findClosest(initp)[0]
    self.addRoot(root)

def xuReconstruction(self, startfrom=None):
    print('Xu Reconstruction')

    startfrom, points = self.getStartFrom(startfrom)
    if startfrom is None: return

    binratio, ok = QInputDialog.getInt(self, 'Bin Ratio', 'Select a bin ratio', self.getparamcache('binratio', 50), 10, 1000)

    if ok:
        self.setparamcache('binratio', binratio)
        self.createBackup('mtg')
        self.showMessage("Apply Xu et al. reconstruction from  node " + str(startfrom) + ".")
        mini, maxi = self.points.pointList.getZMinAndMaxIndex()
        zdist = self.points.pointList[maxi].z - self.points.pointList[mini].z
        binlength = zdist / binratio
        if points is None:
            print('filter', len(self.points.pointList), 'points with distance', binlength)
            points, emptycolor = self.filter_points(PointSet(self.points.pointList), binlength)  # ,[startfrom])
            if len(points) < 10:
                self.showMessage("Not enough points (" + str(len(points)) + ") to apply reconstruction from " + str(startfrom) + ".")
                return
        from .xumethod import xu_method
        xu_method(self.mtg, startfrom, points, binlength)
        self.updateMTGView()
        self.updateGL()

if __name__ == '__main__':
    print_hi('PyCharm')