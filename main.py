import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mingus.containers import Bar
import mingus.extra.LilyPond as LilyPond
os.chdir("C:\\Users\\Greg\\Downloads")
note_list = dict()
note_list = {"0": "C-0", "1": "C#-0", "2": "D-0", "3": "D#-0", "4": "E-0", "5": "E#-0", "6": "F-0",
             "7": "F#-0", "8": "G-0", "9": "G#-0", "10": "A-0", "11": "A#-0", "12": "B-0",
             "13": "B#-0", "14": "C-1", "15": "C#-1", "16": "D-1", "17": "D#-1", "18": "E-1",
             "19": "E#-1", "20": "F-1", "21": "F#-1", "22": "G-1", "23": "G#-1", "24": "A-1", 
             "25": "A#-1", "26": "B-1", "27": "B#-1", "27": "C-2", "28": "C#-2", "29": "D-2",
             "29": "D#-2", "30": "E-2", "31": "E#-2", "32": "F-2", "33": "F#-2", "34": "G-2",
             "35": "G#-2", "36": "A-2", "37": "A#-2", "38": "B-2", "39": "B#-2", "40": "C-3", 
             "41": "C#-3", "42": "D-3", "43": "D#-3", "44": "E-3", "45": "E#-3", "46": "F-3", 
             "47": "F#-3", "48": "G-3", "49": "G#-3", "50": "A-3", "51": "A#-3", "52": "B-3", 
             "53": "B#-3", "54": "C-4", "55": "C#-4", "56": "D-4", "57": "D#-4", "58": "E-4", 
             "59": "E#-4", "60": "F-4", "61": "F#-4", "62": "G-4", "63": "G#-4", "64": "A-4", 
             "65": "A#-4", "66": "B-4", "67": "B#-4", "68": "C-5", "69": "C#-5", "70": "D-5", 
             "71": "D#-5", "72": "E-5", "73": "E#-5", "74": "F-5", "75": "F#-5", "76": "G-5", 
             "77": "G#-5", "78": "A-5", "79": "A#-5", "80": "B-5", "81": "B#-5", "82": "C-6", 
             "83": "C#-6", "84": "D-6", "85": "D#-6", "86": "E-6", "87": "E#-6"}
start_time = None
end_time = None
menubar = None
buttton_lay = None
KEYWIDTH, KEYHEIGHT = 18, 72
note_container = []


class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global menubar
        global buttton_lay
        self.setGeometry(0, 0, 1280, 1024)
        self.setWindowTitle('NAME TBD')
        self.showMaximized()
        menubar = QMenuBar()
        self.actionFile = menubar.addMenu("File")
        self.actionFile.addAction("New")
        self.actionFile.addAction("Open")
        self.actionFile.addAction("Save")
        self.actionFile.addAction("Save as sound file")
        self.lay_button = QtWidgets.QHBoxLayout()
        self.key_text = QLabel("Ключ")
        self.key_text.adjustSize()
        self.lay_button.addWidget(self.key_text, alignment=QtCore.Qt.AlignLeft)
        self.combo = QComboBox(self)
        self.combo.addItem("Скрипичный")
        self.combo.addItem("Басовый")
        self.lay_button.addWidget(self.combo, alignment=QtCore.Qt.AlignLeft)
        self.play_but = QPushButton()
        self.play_but.setText("PLAY")
        self.lay_button.addWidget(self.play_but)
        self.stop_btn = QPushButton()
        self.stop_btn.setText("STOP")
        self.lay_button.addWidget(self.stop_btn)
        buttton_lay = self.lay_button


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
        add_note(self.m_number, start_time, end_time)
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

    def sizeHint(self):
        return self.mapFromScene(self.sceneRect()).boundingRect().size()


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
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)
        self.setRenderHints(QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontClipPainter, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.setBackgroundBrush(QtWidgets.QApplication.palette().base())


def add_note(note, start_time, end_time):
    global note_container
    lol1.setText(str(note))
    element = [note, end_time - start_time]
    note_container.append(element)


def get_png():
    global note_container
    b = Bar()
    for a in note_container:
        pass    


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    ex = Example()
    lol1 = QLineEdit()
    lay = QtWidgets.QVBoxLayout(ex)
    lay.addWidget(menubar)
    lay.addLayout(buttton_lay)
    lay.addWidget(lol1)
    lay.addWidget(NoteTable())
    lay.addWidget(PianoKeyBoard())
    ex.show()
    sys.exit(app.exec_())
