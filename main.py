import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import *
os.chdir("C:\\Users\\Greg\\Downloads")
start_time = None
end_time = None
menubar = None
KEYWIDTH, KEYHEIGHT = 18, 72


class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global menubar
        self.setGeometry(0, 0, 1280, 1024)
        self.setWindowTitle('NAME TBD')
        self.showMaximized()
        menubar = QMenuBar()
        self.actionFile = menubar.addMenu("File")
        self.actionFile.addAction("New")
        self.actionFile.addAction("Open")
        self.actionFile.addAction("Save")
        self.actionFile.addAction("Save as sound file")


class PianoKey(QtWidgets.QGraphicsRectItem):
    def __init__(self, black=False, rect = QtCore.QRectF(), parent=None, num=0):
        super(PianoKey, self).__init__(rect, parent)
        self.m_pressed = False
        self.m_selectedBrush = QtGui.QBrush()
        self.m_brush = QtGui.QBrush(QtCore.Qt.black) if black else QtGui.QBrush(QtCore.Qt.white)
        self.m_black = black
        self.m_number = 0

    def setPressedBrush(self, brush):
        self.m_selectedBrush = brush

    def paint(self, painter, option, widget):
        rendered = QtSvg.QSvgRenderer("key.svg")
        black_pen = QtGui.QPen(QtCore.Qt.black, 1)
        gray_pen = QtGui.QPen(QtGui.QBrush(QtCore.Qt.gray), 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        if self.m_pressed:
            if self.m_selectedBrush.style() != QtCore.Qt.NoBrush:
                painter.setBrush(self.m_selectedBrush)
            else:
                painter.setBrush(QtWidgets.QApplication.palette().highlight())
        else:
            painter.setBrush(self.m_brush)
        painter.setPen(black_pen)
        painter.drawRoundedRect(self.rect(), 15, 15, QtCore.Qt.RelativeSize)
        if self.m_black:
            rendered.render(painter, self.rect())
        else:
            points = [
                QtCore.QPointF(self.rect().left()+1.5, self.rect().bottom()-1),
                QtCore.QPointF(self.rect().right()-1, self.rect().bottom()-1),
                QtCore.QPointF(self.rect().right()-1, self.rect().top()+1)
            ]
            painter.setPen(gray_pen)
            painter.drawPolyline(QtGui.QPolygonF(points))

    def mousePressEvent(self, event):
        global start_time
        self.m_pressed = True
        self.update()
        start_time = time.time()
        super(PianoKey, self).mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        global end_time
        self.m_pressed = False
        self.update()
        end_time = time.time()
        addnote(self.m_number, start_time, end_time)
        super(PianoKey, self).mouseReleaseEvent(event)


class PianoKeyBoard(QtWidgets.QGraphicsView):
    def __init__(self, num_octaves=7,  parent=None, end_octave=1, first_octave=3):
        super(PianoKeyBoard, self).__init__(parent)
        self.initialize()
        self.m_numOctaves = num_octaves
        scene = QtWidgets.QGraphicsScene(QtCore.QRectF(0, 0, KEYWIDTH * self.m_numOctaves * 7, KEYHEIGHT), self)
        self.setScene(scene)
        numkeys = self.m_numOctaves * 12 + end_octave + first_octave
        shift_octave = 0
        if first_octave > 0:
            if first_octave % 12 < 9:
                shift_octave = (first_octave % 12) // 2 + 1
            else:
                shift_octave = (first_octave % 12 + 1) // 2 + 1

        for i in range(numkeys):
            octave = 0
            if shift_octave > 0 and i > 0:
                if i >= first_octave % 12:
                    octave = (i - first_octave % 12) // 12 * 7 + shift_octave
                    j = (i - first_octave % 12) % 12
                    if j >= 5: j += 1
                else:
                    if (first_octave - i) < 4:
                        j = i
                    else:
                        j = i + 1
            else:
                octave = i // 12 * 7
                j = i % 12
                if j >= 5: j += 1
            if j % 2 == 0:
                x = (octave + j / 2)*KEYWIDTH
                key = PianoKey(rect=QtCore.QRectF(x, 0, KEYWIDTH, KEYHEIGHT), black=False, num=i)
            else:
                x = (octave + j // 2) * KEYWIDTH + KEYWIDTH * 6 // 10 + 1
                key = PianoKey(rect=QtCore.QRectF(x, 0, KEYWIDTH * 8 // 10 - 1, KEYHEIGHT * 6//10), black=True)
                key.setZValue(1)
            key.setPressedBrush(QtWidgets.QApplication.palette().highlight())
            key.m_number = i
            self.scene().addItem(key)

    def initialize(self):
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled, False)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)
        self.setRenderHints(QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontClipPainter, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.setBackgroundBrush(QtWidgets.QApplication.palette().base())

    #def resizeEvent(self, event):
    #    super(PianoKeyBoard, self).resizeEvent(event)
    #    self.fitInView(self.scene().sceneRect(), QtCore.Qt.KeepAspectRatio)

    def sizeHint(self):
        return self.mapFromScene(self.sceneRect()).boundingRect().size()


def addnote(note, start_time, end_time):
    x = str(end_time - start_time) + " " + str(note)
    lol1.setText(x)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    ex = Example()
    lol1 = QPushButton("d")
    lol1.resize(1280, 512)
    lay = QtWidgets.QVBoxLayout(ex)
    lay.addWidget(menubar)
    lay.addWidget(lol1)
    lay.addWidget(PianoKeyBoard())
    ex.show()
    sys.exit(app.exec_())
