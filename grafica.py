from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        # self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        #self.ejes = self.fig.add_subplot(111)

        
        #self.ejes.set_xlim(xlim)
        #self.ejes.set_ylim(ylim)
        #self.ejes.scatter(5, 8)
        #self.ejes.errorbar([2,20],[4,8])
        # Añadimos esta linea para que no aparezcan los ejes
        #self.axes.axis('off')

class Grafica(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)