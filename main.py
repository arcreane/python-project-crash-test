import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Slot,Qt,QUrl
from PySide6.QtGui import QPainter,QPixmap
from PySide6.QtMultimedia import QSoundEffect



class Home(QMainWindow):
    def __init__(self, sim_window):
        super().__init__()
        Ui_Home, _ = loadUiType("Home.ui")
        self.ui = Ui_Home()
        self.ui.setupUi(self)
        self.home = QPixmap("image/atc.jpg")

        self.clic = QSoundEffect()
        self.clic.setSource(QUrl.fromLocalFile("audio/airplanecabin.wav"))
        self.clic.setLoopCount(1)
        self.clic.setVolume(0.9)

        self.back = QSoundEffect()
        self.back.setSource(QUrl.fromLocalFile("audio/back.wav"))
        self.back.setLoopCount(1)
        self.back.setVolume(0.5)

        self.music_muted = False

        self.sim_window = sim_window

    def showEvent(self, event):
        super().showEvent(event)
        if not self.music_muted:
            self.back.play()


    def paintEvent(self, event):
        painter = QPainter(self)
        W, H = self.width(), self.height()
        bg = self.home.scaled(W, H, Qt.KeepAspectRatioByExpanding)
        painter.drawPixmap(0, 0, bg)


    @Slot()
    def Musique(self):
        if not self.music_muted:
            self.back.stop()
            self.music_muted = True
        else:
            self.back.play()
            self.music_muted = False

    @Slot()
    def Level1(self):
        level = 5000
        self.clic.play()
        time.sleep(2)
        self.sim_window = Simulation(level=1)
        self.sim_window.spawn_level = level
        self.sim_window.spawn_timer.start(level)

        self.sim_window.showMaximized()
        self.hide()

    @Slot()
    def Level2(self):
        level = 5000
        self.clic.play()
        time.sleep(2)
        self.sim_window = Simulation(level=2)
        self.sim_window.spawn_level = level
        self.sim_window.spawn_timer.start(level)

        self.sim_window.showMaximized()
        self.hide()

    @Slot()
    def Level3(self):
        level = 3000
        self.clic.play()
        time.sleep(2)
        self.sim_window = Simulation(level=2)
        self.sim_window.spawn_level = level
        self.sim_window.spawn_timer.start(level)

        self.sim_window.showMaximized()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    from app import Simulation
    simulation_window = Simulation()
    simulation_window.hide()

    HOME = Home(simulation_window)

    HOME.showMaximized()
    sys.exit(app.exec())
