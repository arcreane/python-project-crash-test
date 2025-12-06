import sys
from Plane import *
from move import MovementManager
from Game import GameEngine
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt, Slot, Signal
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtUiTools import QUiLoader
from Spawn import SpawnManager
from ClicPlane import ClickManager







class Simulation(QMainWindow):

    change_name = Signal(str)
    change_speed = Signal(float)
    change_angle = Signal(float)

    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("radar.ui", self)
        self.setCentralWidget(self.ui.centralwidget)

        self.background = QPixmap("image/runway.png")
        self.plane_img = QPixmap("image/plane.png")

        self.planes = []
        self.selected_plane = None
        self.game_over = False

        self.game = GameEngine(self)
        self.movement_manager = MovementManager(self)
        self.spawn_manager = SpawnManager(self)
        self.click_manager = ClickManager(self)

        # Timer déplacement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.movement)
        self.timer.start(16)

        # Timer spawn avion
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_plane)
        self.spawn_timer.start(3000)

        QTimer.singleShot(200, self.spawn_plane)


        self.change_name.connect(self.name_plane)
        self.change_speed.connect(self.speed_plane)
        self.change_angle.connect(self.angle_plane)

    # --------------------------------------------------------
    # SPAWN
    # --------------------------------------------------------
    def spawn_plane(self):
        plane = self.spawn_manager.spawn_plane()
        self.planes.append(plane)

    # --------------------------------------------------------
    # MOUVEMENT
    # --------------------------------------------------------
    def movement(self):
        if self.game_over:
            return
        self.movement_manager.move_all()
        self.update_info_label()

    # --------------------------------------------------------
    # CLIC SUR UN AVION
    # --------------------------------------------------------
    def mousePressEvent(self, event):
        plane = self.click_manager.click(event)
        if plane:
            self.selected_plane = plane
            self.change_name.emit(plane.name)   # slot -> update label
            self.update_info_label()

    def send_to_hold(self):
        if self.selected_plane:
            self.selected_plane.holding = True

    def stop_hold(self):
        if self.selected_plane:
            self.selected_plane.holding = False

    # --------------------------------------------------------
    # SLOTS
    # --------------------------------------------------------
    @Slot(str)
    def name_plane(self, name):
        self.update_info_label()

    @Slot(float)
    def speed_plane(self, speed):
        if self.selected_plane:
            self.selected_plane.speed = speed
            self.update_info_label()

    @Slot(float)
    def angle_plane(self, angle):
        if self.selected_plane:
            self.selected_plane.angle = angle
            self.update_info_label()

    @Slot(int)
    def emit_angle_change(self, value):
        if self.selected_plane:
            self.change_angle.emit(float(value))

    @Slot(int)
    def emit_speed_change(self, value):
        if self.selected_plane:
            self.change_speed.emit(value / 10.0)


    def update_info_label(self):

        if self.selected_plane is None:
            self.ui.labelinfo.setText("")
            return

        p = self.selected_plane

        # vitesse en kt
        speed_kt = p.speed * 100 + 60

        text = (
            f"✈ Vol : {p.name}\n\n"
            f"📍 Position : ({p.x:.0f}, {p.y:.0f})\n\n"
            f"⚡ Vitesse : {speed_kt:.0f} kt\n\n"
            f"🧭 Cap : {p.angle:.1f}°"
        )

        self.ui.labelinfo.setText(text)


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
            painter.translate(
                fx + plane.x + plane.w/2,
                fy + plane.y + plane.h/2
            )
            painter.rotate(plane.angle)
            painter.drawPixmap(-plane.w/2, -plane.h/2, plane.image)
            painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Simulation()
    window.showMaximized()
    sys.exit(app.exec())