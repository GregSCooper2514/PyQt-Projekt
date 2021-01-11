import sys
import time
import csv
from pydub import *
from pydub.playback import play
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import *
note_list = dict()
note_list = {"0": "C-0", "1": "C#-0", "2": "D-0", "3": "C-1", "4": "C#-1", "5": "D-1",
             "6": "D#-1", "7": "E-1", "8": "E#-1", "9": "F-1", "10": "F#-1", "11": "G-1",
             "12": "G#-1", "13": "A-1", "14": "A#-1", "15": "B-1", "16": "B#-1", "17": "C-2",
             "18": "C#-2", "19": "D-2", "20": "D#-2", "21": "E-2", "22": "E#-2", "23": "F-2",
             "24": "F#-2", "25": "G-2", "26": "G#-2", "27": "A-2", "28": "A#-2", "29": "B-2",
             "30": "B#-2", "31": "C-3", "32": "C#-3", "33": "D-3", "34": "D#-3", "35": "E-3",
             "36": "E#-3", "37": "F-3", "38": "F#-3", "39": "G-3", "40": "G#-3", "41": "A-3",
             "42": "A#-3", "43": "B-3", "44": "B#-3", "45": "C-4", "46": "C#-4", "47": "D-4",
             "48": "D#-4", "49": "E-4", "50": "E#-4", "51": "F-4", "52": "F#-4", "53": "G-4",
             "54": "G#-4", "55": "A-4", "56": "A#-4", "57": "B-4", "58": "B#-4", "59": "C-5",
             "60": "C#-5", "61": "D-5", "62": "D#-5", "63": "E-5", "64": "E#-5", "65": "F-5",
             "66": "F#-5", "67": "G-5", "68": "G#-5", "69": "A-5", "70": "A#-5", "71": "B-5",
             "72": "B#-5", "73": "C-6", "74": "C#-6", "75": "D-6", "76": "D#-6", "77": "E-6",
             "78": "E#-6", "79": "F-6", "80": "F#-6", "81": "G-6", "82": "G#-6", "83": "A-6",
             "84": "A#-6", "85": "B-6", "86": "B#-6", "87": "C-7"}
default_sound = AudioSegment.from_wav("SoundSamples\\default.wav")
start_time = None
end_time = None
menubar = None
buttton_lay = None
KEYWIDTH, KEYHEIGHT = 18, 72
note_container = []


class Example(QWidget):
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
        self.action_Open = QAction("Open", self)
        self.actionFile.addAction(self.action_Open)
        self.action_Open.triggered.connect(self.open_file)
        self.action_Save = QAction("Save", self)
        self.actionFile.addAction(self.action_Save)
        self.action_Save.triggered.connect(self.save)
        self.action_sas = QAction("Save as sound file", self)
        self.actionFile.addAction(self.action_sas)
        self.action_sas.triggered.connect(self.save_as_sound)
        self.lay_button = QHBoxLayout()
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

    def open_file(self):
        global note_container
        if bool(note_container):
            buttonReply = QMessageBox.question(self, 'Piano', "Do you want to save?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            print(int(buttonReply))
            if buttonReply == QMessageBox.Yes:
                self.save()
            if buttonReply == QMessageBox.No:
                pass
            if buttonReply == QMessageBox.Cancel:
                return
        name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV (*.csv);;All Files (*)")
        self.file_name = name
        with open(name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i in enumerate(reader):
                note_container.append(i[1])
            pass

class PianoKey(QGraphicsRectItem):
    def __init__(self, black=False, rect = QRectF(), parent=None, num=0):
        super(PianoKey, self).__init__(rect, parent)
        self.m_pressed = False
        self.m_selectedBrush = QBrush()
        self.m_brush = QBrush(Qt.black) if black else QBrush(Qt.white)
        self.m_black = black
        self.m_number = 0

    def setPressedBrush(self, brush):
        self.m_selectedBrush = brush

    def paint(self, painter, option, widget):
        rendered = QSvgRenderer("key.svg")
        black_pen = QPen(Qt.black, 1)
        gray_pen = QPen(QBrush(Qt.gray), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        if self.m_pressed:
            if self.m_selectedBrush.style() != Qt.NoBrush:
                painter.setBrush(self.m_selectedBrush)
            else:
                painter.setBrush(QApplication.palette().highlight())
        else:
            painter.setBrush(self.m_brush)
        painter.setPen(black_pen)
        painter.drawRoundedRect(self.rect(), 15, 15, Qt.RelativeSize)
        if self.m_black:
            rendered.render(painter, self.rect())
        else:
            points = [
                QPointF(self.rect().left()+1.5, self.rect().bottom()-1),
                QPointF(self.rect().right()-1, self.rect().bottom()-1),
                QPointF(self.rect().right()-1, self.rect().top()+1)
            ]
            painter.setPen(gray_pen)
            painter.drawPolyline(QPolygonF(points))

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


class PianoKeyBoard(QGraphicsView):
    def __init__(self, num_octaves=7,  parent=None, end_octave=1, first_octave=3):
        super(PianoKeyBoard, self).__init__(parent)
        self.initialize()
        self.m_numOctaves = num_octaves
        scene = QGraphicsScene(QRectF(0, 0, KEYWIDTH * self.m_numOctaves * 7, KEYHEIGHT), self)
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
                key = PianoKey(rect=QRectF(x, 0, KEYWIDTH, KEYHEIGHT), black=False, num=i)
            else:
                x = (octave + j // 2) * KEYWIDTH + KEYWIDTH * 6 // 10 + 1
                key = PianoKey(rect=QRectF(x, 0, KEYWIDTH * 8 // 10 - 1, KEYHEIGHT * 6//10), black=True)
                key.setZValue(1)
            key.setPressedBrush(QApplication.palette().highlight())
            key.m_number = i
            self.scene().addItem(key)

    def initialize(self):
        self.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontClipPainter, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setBackgroundBrush(QApplication.palette().base())

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
    display_note()

def display_note():
    global note_container, note_list
    x = ""
    for a in note_container:
        x += note_list[str(a[0])]
        x += " "
    labell.setText(x)

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
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ex = Example()
    labell = QLineEdit()
    labell.setMinimumHeight(200)
    lay = QVBoxLayout(ex)
    lay.addWidget(menubar)
    lay.addLayout(buttton_lay)
    lay.addWidget(labell)
    lay.addWidget(PianoKeyBoard())
    ex.show()
    sys.exit(app.exec_())
