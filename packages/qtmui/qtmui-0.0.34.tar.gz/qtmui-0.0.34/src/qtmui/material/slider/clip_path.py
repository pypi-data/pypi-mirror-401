import sys
from PySide6 import QtCore, QtGui, QtWidgets

class HexButton(QtWidgets.QPushButton):
    size = 100
    x = (3**0.5 / 2)
    font = QtGui.QFont('Arial', size*0.08)
    hexaPoints = [QtCore.QPoint(size/4,0),
                    QtCore.QPoint(size/4 + size/2,0),
                    QtCore.QPoint(size,size*0.5*x),
                    QtCore.QPoint(size/4 + size/2,size*x),
                    QtCore.QPoint(size/4,size*x),
                    QtCore.QPoint(0,size*0.5*x)]
    hexaPointsF = [QtCore.QPointF(size/4,0),
                    QtCore.QPointF(size/4 + size/2,0),
                    QtCore.QPointF(size,size*0.5*x),
                    QtCore.QPointF(size/4 + size/2,size*x),
                    QtCore.QPointF(size/4,size*x),
                    QtCore.QPointF(0,size*0.5*x)]
    hexa = QtGui.QPolygon(hexaPoints)
    hexaF = QtGui.QPolygonF(hexaPointsF)

    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self)
        self.setMinimumSize(HexButton.size + 10, HexButton.size + 10)
        self.text = None
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.color = QtGui.QColor(241, 186, 82)
        self.setFlat(True)

    def setText(self, text):
        self.text = text
        self.update()

    def setColor(self, r,g,b):
        self.color = QtGui.QColor(r,g,b)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        self.style().drawControl(QtWidgets.QStyle.CE_PushButton, opt, qp, self)
        qp.end()
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.color)
        basePoly = QtGui.QPolygonF(HexButton.hexaF)
        ss = 0.98
        basePoly.translate(QtCore.QPointF(HexButton.size*(1.03-ss)*0.8, HexButton.size*(1.19-ss)*0.6*HexButton.x))
        painter.drawPolygon(basePoly)
        plist = HexButton.hexaPointsF + [HexButton.hexaPointsF[0]]
        s = 0.95
        painter.translate(QtCore.QPointF(HexButton.size*(1.03-s)*0.8, HexButton.size*(1.2-s)*0.6*HexButton.x))
        painter.scale(s, s)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), (HexButton.size*0.016)*(1/s)))
        painter.drawPolyline(*plist)
        painter.resetTransform()
        if self.text:
            pen_text = QtGui.QPen()
            pen_text.setBrush(QtGui.QColor(0,0,0))
            painter.setPen(pen_text)
            painter.setFont(HexButton.font)
            painter.drawText(0, 0, HexButton.size+10, HexButton.size*HexButton.x+20, QtCore.Qt.AlignCenter, self.text)
        painter.end()


class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        centralwidget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QHBoxLayout(centralwidget)
        self.button = HexButton()
        self.button.setText("Foooooo")
        self.anotherButton = HexButton()
        self.anotherButton.setText("Barrr")
        self.anotherButton.setColor(255, 102, 102)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.anotherButton)
        self.setCentralWidget(centralwidget)


def main():
     app = QtWidgets.QApplication(sys.argv)
     form = MainDialog()
     form.show()
     app.exec_()

if __name__ == '__main__':
     main()