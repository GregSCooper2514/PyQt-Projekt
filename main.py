import os
import sys
import time
import csv
from pydub import *
from pydub.playback import play
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
os.chdir("C:\\Users\\Greg\\Downloads")
default_sound = AudioSegment.from_wav("default.wav")
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
        global menubar, buttton_lay
        self.setGeometry(0, 0, 1280, 1024)
        self.setWindowTitle('Piano')
        self.showMaximized()
        self.file_name = None
        menubar = QMenuBar()
        self.actionFile = menubar.addMenu("File")
        self.action_New = QAction("New", self)
        self.actionFile.addAction(self.action_New)
        self.action_New.triggered.connect(self.new)
        self.actionFile.addAction("Open")
        self.action_Save = QAction("Save", self)
        self.actionFile.addAction(self.action_Save)
        self.action_Save.triggered.connect(self.save)
        self.action_sas = QAction("Save as sound file", self)
        self.actionFile.addAction(self.action_sas)
        self.action_sas.triggered.connect(self.save_as_sound)
        self.lay_button = QtWidgets.QHBoxLayout()
        self.play_but = QPushButton()
        self.play_but.setText("PLAY")
        self.play_but.clicked.connect(play_sound)
        self.lay_button.addWidget(self.play_but)
        self.stop_btn = QPushButton()
        buttton_lay = self.lay_button

    def new(self):
        global note_container
        if bool(note_container):
            buttonReply = QMessageBox.question(self, 'Piano', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            print(int(buttonReply))
            if buttonReply == QMessageBox.Yes:
                self.save()
                note_container = []
            if buttonReply == QMessageBox.No:
                note_container = []
            if buttonReply == QMessageBox.Cancel:
                pass

    def save_as_sound(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', self.file_name, "Waveform Audio File (*.wav);;All Files (*)")
        save_soundfile(name)

    def save(self):
        global note_container
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', self.file_name, "CSV (*.csv);;All Files (*)")
        if bool(name):
            self.file_name = name
            with open(name, 'w', newline='') as csvfile:
                writer = csv.writer(
                csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in note_container:
                    writer.writerow([i[0], i[1]])


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
                x = (octave + j / 2) * KEYWIDTH
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
    global note_container, default_sound
    time = (end_time - start_time) * 100
    if time < 90:
        value = 120
    if 90 < time < 180:
        value = 240
    if 180 < time < 360:
        value = 480
    if time > 360:
        value = 960
    element = [note, value]
    note_container.append(element)

def save_soundfile(filename):
    global note_container, default_sound
    container = note_container
    sound = default_sound
    for a in container:
        file_path = str(a[0]) + ".wav"
        cur_note = AudioSegment.from_wav(f"SoundSamples\\{file_path}")
        cut_note = cur_note[:int(a[1])]
        sound += cut_note
    sound.export(filename, format="wav")

def play_sound():
    global note_container, default_sound
    container = note_container
    sound = default_sound
    for a in container:
        file_path = str(a[0]) + ".wav"
        cur_note = AudioSegment.from_wav(f"SoundSamples\\{file_path}")
        cut_note = cur_note[:int(a[1])]
        sound += cut_note
    play(sound)

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
