import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
os.chdir("C:\\Users\\Greg\\Downloads")
note_list = dict()
note_list = {"0": "C-0", "1": "C#-0", "2": "D-0", "3": "C-1", "4": "C#-1", "5": "D-1", "6": "D#-1",
             "7": "E-1", "8": "E#-1", "9": "F-1", "10": "F#-1", "11": "G-1", "12": "G#-1", 
             "13": "A-1", "14": "A#-1", "15": "B-1", "16": "B#-1", "17": "C-2", "18": "C#-2",
             "19": "D-2", "20": "D#-2", "21": "E-2", "22": "E#-2", "23": "F-2", "24": "F#-2",
             "25": "G-2", "26": "G#-2", "27": "A-2", "28": "A#-2", "29": "B-2", "30": "B#-2", 
             "31": "C-3", "32": "C#-3", "33": "D-3", "34": "D#-3", "35": "E-3", "36": "E#-3", 
             "37": "F-3", "38": "F#-3", "39": "G-3", "40": "G#-3", "41": "A-3", "42": "A#-3", 
             "43": "B-3", "44": "B#-3", "45": "C-4", "46": "C#-4", "47": "D-4", "48": "D#-4", 
             "49": "E-4", "50": "E#-4", "51": "F-4", "52": "F#-4", "53": "G-4", "54": "G#-4", 
             "55": "A-4", "56": "A#-4", "57": "B-4", "58": "B#-4", "59": "C-5", "60": "C#-5", 
             "61": "D-5", "62": "D#-5", "63": "E-5", "64": "E#-5", "65": "F-5", "66": "F#-5", 
             "67": "G-5", "68": "G#-5", "69": "A-5", "70": "A#-5", "71": "B-5", "72": "B#-5", 
             "73": "C-6", "74": "C#-6", "75": "D-6", "76": "D#-6", "77": "E-6", "78": "E#-6", 
             "79": "F-6", "80": "F#-6", "81": "G-6", "82": "G#-6", "83": "A-6", "84": "A#-6", 
             "85": "B-6", "86": "B#-6", "87": "C-7"}
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


def add_note(note, start_time, end_time):
    global note_container
    lol1.setText(str(note))
    element = [note, end_time - start_time]
    note_container.append(element)
    get_png()


def get_png():
    global note_container
    t = Track(instrument=i)
    lol = Bar()
    t.add_bar(lol)
    for a in note_container:
        b = Bar("C", (1, 1))
        b + note_list[str(a[0])]
        t.add_bar(t)
    bar = LilyPond.from_Track(t)
    LilyPond.to_png(bar, "lol")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    ex = Example()
    lol1 = QLineEdit()
    lol1.setMinimumHeight(100)
    lay = QtWidgets.QVBoxLayout(ex)
    lay.addWidget(menubar)
    lay.addLayout(buttton_lay)
    lay.addWidget(lol1)
    lay.addWidget(PianoKeyBoard())
    ex.show()
    sys.exit(app.exec_())
