import sys
import node
import person
from PyQt4 import QtGui, QtCore

width = 10
height = 10
FRAME_WIDTH = 500
FRAME_HEIGHT = 300
myMap = node.Graph(width, height)

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, FRAME_WIDTH, FRAME_HEIGHT)
        self.setWindowTitle("My Python")

        person.Person('Jimmy', myMap, 8, 3)
        self.generateMap();
        self.menu = QtGui.QLabel(self)
        self.menuOption1 = QtGui.QLabel(self)
        self.menuOption1.setFont(QtGui.QFont('Arial', 7))
        self.menuOption2 = QtGui.QLabel(self)
        self.menuOption2.setFont(QtGui.QFont('Arial', 7))
        #extractAction = QtGui.QAction("new", self)
        #extractAction.setShortcut("CTRL+Q")
        #extractAction.setStatusTip('New file')
        #extractAction.triggered.connect(self.close_application)

        #self.statusBar()

        #mainMenu = self.menuBar()
        #fileMenu = mainMenu.addMenu('&File')
        #fileMenu.addAction(extractAction)

        checkBox = QtGui.QCheckBox('Full Screen', self)
        checkBox.stateChanged.connect(self.enlargeWindow)
        checkBox.resize(150, 20)
        checkBox.move(0, 150)

        textArea = QtGui.QLabel(self)
        textArea.setText("Hello World")
        textArea.move(0,200)

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

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.x() >= 150 and QMouseEvent.x() <= 400:
            if QMouseEvent.y() >= 10 and QMouseEvent.y() <= 260:
                xTile = (QMouseEvent.x()-150)/25
                yTile = (QMouseEvent.y()-10)/25
                personPix = QtGui.QPixmap('img/menu.png')
                personPix = personPix.scaled(75, 100)
                self.menu.setPixmap(personPix)
                self.menu.resize(75,100)
                self.menu.show()
                self.menuOption1.show()
                self.menuOption1.setText("Move Here")
                self.menuOption2.show()
                self.menuOption2.setText("Harvest")
                if QMouseEvent.y() < FRAME_HEIGHT-100:
                    self.menuX = QMouseEvent.x()
                    self.menuY = QMouseEvent.y()
                    self.menu.move(QMouseEvent.x(), QMouseEvent.y())
                    self.menuOption1.move(QMouseEvent.x()+15, QMouseEvent.y()+5)
                    self.menuOption2.move(QMouseEvent.x()+15, QMouseEvent.y()+15)
                else:
                    self.menuX = QMouseEvent.x()
                    self.menuY = QMouseEvent.y()-100
                    self.menu.move(QMouseEvent.x(), QMouseEvent.y()-100)
                    self.menuOption1.move(QMouseEvent.x()+15, QMouseEvent.y()-95)
                    self.menuOption2.move(QMouseEvent.x()+15, QMouseEvent.y()-85)
                self.leftClick = 'true'

    def mouseReleaseEvent(self, QMouseEvent):
        print('%s, %s' %(QMouseEvent.x() - self.menuX, QMouseEvent.y() - self.menuY))
        if self.leftClick == 'true':
            self.menu.hide()
            self.menuOption1.hide()
            self.menuOption2.hide()
            if (QMouseEvent.x() - self.menuX) >= 0 and (QMouseEvent.x() - self.menuX) <= 75:
                if(QMouseEvent.y() - self.menuY) >= 0 and (QMouseEvent.y() - self.menuY) <= 20:
                    print 'option 1'
                elif (QMouseEvent.y() - self.menuY) >= 21 and (QMouseEvent.y() - self.menuY) <= 50:
                    print 'option 2'
    
    def enlargeWindow(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(0, 0, 800, 480)
        else:
            self.setGeometry(50, 50, 500, 300)        

    def generateMap(self):
        for y in range(0, 10):
            for x in range(0, 10):
                pic = QtGui.QLabel(self)
                pic.setPixmap(self.generateImage(x,y))
                pic.show()        
                pic.resize(25,25)
                pic.move(150+(x*25),10+(y*25))

        for y in range(0, 10):
            for x in range(0, 10):
                if myMap.getExistance(x,y) <> None:
                    pic = QtGui.QLabel(self)
                    personPix = QtGui.QPixmap('img/person.png')
                    personPix = personPix.scaled(25, 25)
                    pic.setPixmap(personPix)
                    pic.show()
                    pic.move(155+(x*25), 10+(y*25))

    def generateImage(self, x, y):
        tile = myMap.getTile(myMap.cordsConversion(x, y))
        if tile == 'Grass':
            tileStr = 'img/grass.png'
        elif tile == 'Dirt':
            tileStr = 'img/dirt.png'
        return QtGui.QPixmap(tileStr)
            

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
