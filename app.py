import sys
from Plane import *
from Spawn import *
from move import move_all
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtUiTools import QUiLoader


class Simulation(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("radartest.ui", self)
        self.setCentralWidget(self.ui.centralwidget)

        self.background = QPixmap("image/runway.png")
        self.plane_img = QPixmap("image/plane.png")

        self.planes = []

        # Timer déplacement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.movement)
        self.timer.start(16)

        # Timer spawn
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.spawn_timer.start(3000)

        QTimer.singleShot(200, self.spawn_plane)

    def spawn_plane(self):
        frame = self.ui.frameCenter
        x, y, angle = spawn(frame, self.plane_img)
        plane = Plane(x, y, angle, self.plane_img)
        self.planes.append(plane)

    def movement(self):
        # délègue à move_all
        move_all(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        win_l, win_h = self.width(), self.height()
        if not self.background.isNull():
            bg = self.background.scaled(win_l, win_h, Qt.KeepAspectRatioByExpanding)
            painter.drawPixmap(0, 0, bg)

        frame = self.ui.frameCenter
        fx, fy = frame.x(), frame.y()

        for plane in self.planes:
            painter.save()
            painter.translate(fx + plane.x + plane.w / 2,
                              fy + plane.y + plane.h / 2)
            painter.rotate(plane.angle)
            painter.drawPixmap(-plane.w / 2, -plane.h / 2, plane.image)
            painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Simulation()
    window.showMaximized()
    sys.exit(app.exec())
