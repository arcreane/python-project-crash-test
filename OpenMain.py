import sys
from Plane import *
from Spawn import *
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtUiTools import QUiLoader


class Simulation(QMainWindow):
    def __init__(self):
        super().__init__()

        # Charger interface .ui
        loader = QUiLoader()
        self.ui = loader.load("radartest.ui", self)
        self.setCentralWidget(self.ui.centralwidget)

        # Charger les images
        self.background = QPixmap("image/runway.png")
        self.plane_img = QPixmap("image/plane.png")

        # Gestion avion
        self.plane = None
        QTimer.singleShot(200, self.spawn_plane)  #évite de créer l'avion avant que l’interface soit prête

        # délais entre chaque appelle de move()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move)
        self.timer.start(16)

    def spawn_plane(self):
        frame = self.ui.frameCenter
        x, y, angle = spawn(frame, self.plane_img)
        self.plane = Plane(x, y, angle, self.plane_img)

    def move(self):
        if not self.plane:
            return

        frame = self.ui.frameCenter
        max_l = frame.width() - self.plane.w
        max_h = frame.height() - self.plane.h

        dans_la_zone = self.plane.update_position(max_l, max_h) #Recoit True or False
        if not dans_la_zone:
            self.plane = None
            QTimer.singleShot(100, self.spawn_plane)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        #FOND GLOBAL
        win_l, win_h = self.width(), self.height()
        if not self.background.isNull():
            bg = self.background.scaled(win_l, win_h, Qt.KeepAspectRatioByExpanding)
            painter.drawPixmap(0, 0, bg)

        #AVION
        if self.plane:
            frame = self.ui.frameCenter
            fx, fy = frame.x(), frame.y()
            painter.save()
            # Déplace le repère de dessin au centre de l’avion (coord x,y dans le frame)
            painter.translate(
                fx + self.plane.x + self.plane.w / 2,
                fy + self.plane.y + self.plane.h / 2
            )
            # Oriente le dessin selon l’angle actuel de l’avion
            painter.rotate(self.plane.angle)

            # Dessine l’image de l’avion centrée en (0,0) au point (x,y) sur le frame
            painter.drawPixmap(-self.plane.w / 2, -self.plane.h / 2, self.plane.image)
            painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Simulation()
    window.showMaximized()
    sys.exit(app.exec())
