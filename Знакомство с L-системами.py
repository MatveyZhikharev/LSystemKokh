import sys

from PyQt5.QtWidgets import QWidget, QApplication, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

from math import sin, cos, radians

Kokh_line = {}


def read_kokh():
    with open('data.txt', "rt", encoding='utf8') as f:
        data = f.readlines()
    Kokh_line['name'] = data[0].strip()
    Kokh_line['degr'] = 360 / int(data[1].strip())
    Kokh_line['axioma'] = data[2].strip()
    Kokh_line['theorema'] = data[3].strip().split()[1]


def buildlsystem(n):
    result = Kokh_line['axioma']
    for i in range(n):
        new = ''
        for ch in result:
            if ch == Kokh_line['axioma']:
                new += Kokh_line['theorema']
            else:
                new += ch
        result += new
    return result


class LSystemKokh(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1500, 500)
        self.setWindowTitle('Кривая Коха')

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setValue(1)
        self.sld.setTickInterval(1)
        self.sld.resize(500, 50)
        self.sld.setRange(1, 5)
        self.sld.setTickPosition(QSlider.TicksBothSides)
        self.sld.setSingleStep(1)
        self.sld.setFocusPolicy(Qt.StrongFocus)
        self.sld.valueChanged.connect(self.paintEvent)
        self.show()

    def paintEvent(self, event):
        self.qp = QPainter()
        self.qp.begin(self)
        self.drawFlag()
        self.qp.end()

    def drawFlag(self):
        pos = [10, 300, 0]

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        self.qp.setPen(pen)
        read_kokh()

        flag = buildlsystem(self.sld.value())
        for ch in flag:
            if ch == "F":
                self.qp.drawLine(pos[0], pos[1], pos[0] + int(15 * cos(radians(pos[2]))),
                                 pos[1] + int(15 * sin(radians(pos[2]))))
                pos[0] += int(15 * cos(radians(pos[2])))
                pos[1] += int(15 * sin(radians(pos[2])))
            elif ch == '-':
                pos[2] -= Kokh_line['degr']
            elif ch == '+':
                pos[2] += Kokh_line['degr']
        self.update()


def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = excepthook
    ex = LSystemKokh()
    sys.exit(app.exec_())
