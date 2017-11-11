import sys
import node
from PyQt4 import QtGui, QtCore

myMap = node.Graph(4, 4)

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("My Python")

        extractAction = QtGui.QAction("new", self)
        extractAction.setShortcut("CTRL+Q")
        extractAction.setStatusTip('New file')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        checkBox = QtGui.QCheckBox('Full Screen', self)
        checkBox.stateChanged.connect(self.enlargeWindow)
        checkBox.resize(150, 20)
        checkBox.move(0, 150)

        textArea = QtGui.QLabel(self)
        textArea.setText("Hello World")
        textArea.move(0,200)

        self.mapTest()
        self.home()

    def home(self): 
        btn = QtGui.QPushButton("Quit", self)
        btn.resize(btn.minimumSizeHint())
        btn.move(0, 100)
        btn.clicked.connect(self.close_application)
        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract',
                                            "Are you sure?",
                                            QtGui.QMessageBox.No |
                                            QtGui.QMessageBox.Yes)
        if choice == QtGui.QMessageBox.Yes:
            print("Goood bye!")
            sys.exit()
        else:
            pass

    def enlargeWindow(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(0, 0, 800, 480)
        else:
            self.setGeometry(50, 50, 500, 300)        

    def mapTest(self):
        myMap.removeEdge(5, 'south')
        myMap.removeEdge(5, 'east')

        for x in myMap.vert_dict:
            print('%s' %(myMap.vert_dict[x]))
        shortDist, shortPath = myMap.getShortestDistance(5)
        print('%s' %shortDist[10].distance)
        
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
