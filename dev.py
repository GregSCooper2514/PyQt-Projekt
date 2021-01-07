import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
class NoteTable(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(NoteTable, self).__init__(parent)
        self.initialize()
        scene = QtWidgets.QGraphicsScene(QtCore.QRectF(0, 0, 100, 100), self)
        self.setScene(scene)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(30, 30, 120, 30)
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(30, 60, 120, 30)
        qp.setBrush(QColor(0, 0, 255))
        qp.drawRect(30, 90, 120, 30)

    def initialize(self):
        self.setAttribute(QtCore.Qt.WA_InputMethodEnabled, False)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)
        self.setRenderHints(QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontClipPainter, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.setBackgroundBrush(QtWidgets.QApplication.palette().base())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    lay.addWidget(NoteTable())
    w.resize(640, 480)
    w.setWindowTitle("asd")
    w.show()
    sys.exit(app.exec_()) 