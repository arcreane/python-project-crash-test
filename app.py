import sys
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Qt, Slot, Signal,QUrl
from PySide6.QtGui import QPainter, QPixmap, QTransform
from PySide6.QtMultimedia import QSoundEffect


from Game import GameEngine
from Spawn import SpawnManager
from move import MovementManager
from ClicPlane import ClicManager


class Simulation(QMainWindow):

    change_name = Signal(str)
    change_speed = Signal(float)
    change_angle = Signal(float)

    def __init__(self,level=2):
        super().__init__()
        self.level = level

        # --------------- UI SELON LE NIVEAU ----------------
        if self.level == 1:
            ui_file = "radar.ui"
            self.background = QPixmap("image/runway.png")
        elif self.level == 2:
            ui_file = "radar2.ui"
            self.background = QPixmap("image/runway2.png")
        else:
            ui_file = "radar.ui"
            self.background = QPixmap("image/runway.png")

        ui_class, _ = loadUiType(ui_file)
        self.ui = ui_class()
        self.ui.setupUi(self)

        # Images
        self.plane_img = QPixmap("image/plane.png")
        self.plane_emergency = QPixmap("image/plane_panne.png")
        self.needle_img = QPixmap("image/test4.png")

        # QLabel ne bloque pas la souris
        self.ui.labelCompas.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.ui.labelPlane.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.update_compass(self.ui.dial.value())
        self.ui.dial.valueChanged.connect(self.update_compass)

        # Son d’urgence
        self.emergency_sound = QSoundEffect()
        self.emergency_sound.setSource(QUrl.fromLocalFile("audio/Mayday.wav"))
        self.emergency_sound.setLoopCount(1)
        self.emergency_sound.setVolume(0.4)

        # État
        self.planes = []
        self.selected_plane = None
        self.game_over = False


        self.spawn_manager = SpawnManager(self)
        self.movement_manager = MovementManager(self)
        self.clic_manager = ClicManager(self)


        self.game = GameEngine(self)
        self.game.timer_label()

        # Timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.movement)
        self.timer.start(16)

        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_plane)

        self.spawn_level = 3000  # valeur par défaut


        self.change_name.connect(self.name_plane)
        self.change_speed.connect(self.speed_plane)
        self.change_angle.connect(self.angle_plane)

        # Musique
        self.music = QSoundEffect()
        self.music.setSource(QUrl.fromLocalFile("audio/music.wav"))
        self.music.setLoopCount(-1)
        self.music.setVolume(0.3)


    def showEvent(self, event):
        super().showEvent(event)
        self.spawn_timer.start(self.spawn_level)
        self.music.play()


    def hideEvent(self, event):
        super().hideEvent(event)
        self.music.stop()

    # --------------------------------------------------------
    #  COMPAS
    # --------------------------------------------------------
    def update_compass(self, angle):
        rotated = self.needle_img.transformed(QTransform().rotate(angle))
        self.ui.labelPlane.setPixmap(rotated)

    # --------------------------------------------------------
    #  SPAWN
    # --------------------------------------------------------
    def spawn_plane(self):
        plane = self.spawn_manager.spawn_plane()
        if plane:
            self.planes.append(plane)

    # --------------------------------------------------------
    #  MOUVEMENT
    # --------------------------------------------------------
    def movement(self):
        self.movement_manager.move_all()

    # --------------------------------------------------------
    #  AFFICHAGE
    # --------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        W, H = self.width(), self.height()
        bg = self.background.scaled(W, H, Qt.KeepAspectRatioByExpanding)
        painter.drawPixmap(0, 0, bg)

        frame = self.ui.frameCenter
        fx, fy = frame.x(), frame.y()

        for plane in self.planes:
            painter.save()
            painter.translate(fx + plane.x + plane.w / 2,
                              fy + plane.y + plane.h / 2)
            painter.rotate(plane.angle - 90)
            painter.drawPixmap(-plane.w / 2, -plane.h / 2, plane.image)
            painter.restore()

    # --------------------------------------------------------
    #  CLIC SUR AVION
    # --------------------------------------------------------
    def mousePressEvent(self, event):
        plane = self.clic_manager.clic_on_plane(event)
        if plane:
            self.selected_plane = plane
            self.game.register_click(plane)
            self.change_name.emit(plane.name)

    # --------------------------------------------------------
    #  INFOS AVION
    # --------------------------------------------------------
    def update_info_label(self):
        if self.selected_plane:
            p = self.selected_plane
            speed_kt = p.speed * 100 + 60
            text = (
                f"   N° Vol : {p.name}\n\n\n\n"
                f"   Destination : {p.destination}\n\n\n\n"
                f"   Vitesse : {speed_kt:.0f} kt\n\n\n\n"
                f"   Cap : {p.angle:.1f}°"
            )
            self.ui.labelinfo.setText(text)

    # --------------------------------------------------------
    #  HOLD
    # --------------------------------------------------------
    @Slot()
    def send_hold(self):
        if self.selected_plane:
            self.movement_manager.send_plane_to_hold(self.selected_plane)

    @Slot()
    def stop_hold(self):
        if self.selected_plane:
            self.movement_manager.release_hold(self.selected_plane)

    # --------------------------------------------------------
    #  TOUR DE PISTE
    # --------------------------------------------------------
    @Slot()
    def land_plane21(self):
        if self.game_over or not self.selected_plane:
            return
        if not self.selected_plane.must_land:
            return

        plane = self.selected_plane
        frame = self.ui.frameCenter

        cx = frame.width() / 2
        cy = frame.height() / 2

        relative_wps = [
            (+120, +40),
            (0, +300),
            (-120, +260),
            (-10, -125)
        ]

        piste_angle = 205

        final_wps = []
        for lx, ly in relative_wps:
            rx, ry = MovementManager.rotate_point(lx, ly, piste_angle)
            final_wps.append((cx + rx, cy + ry))

        plane.waypoints = final_wps
        plane.current_wp = 0
        plane.landing = True
        plane.speed = 1

    @Slot()
    def land_plane30(self):
        if self.game_over or not self.selected_plane:
            return
        if not self.selected_plane.must_land:
            return

        plane = self.selected_plane
        frame = self.ui.frameCenter

        cx = frame.width() / 2
        cy = frame.height() / 2

        wps_piste30 = [
            (-300, 0),
            (-300, 400),
            (120, 400),
            (120, 300),
            (-200, 85),
        ]

        final_wps = [(cx + dx, cy + dy) for (dx, dy) in wps_piste30]

        plane.waypoints = final_wps
        plane.current_wp = 0
        plane.landing = True
        plane.speed = 1

    # --------------------------------------------------------
    #  SLIDERS/BOUTONS
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
        if not self.game_over and self.selected_plane:
            self.change_angle.emit(float(value))

    @Slot(int)
    def emit_speed_change(self, value):
        if not self.game_over and self.selected_plane:
            self.change_speed.emit(value / 10.0)


    @Slot()
    def restart_game(self):
        self.game_over = False
        self.planes.clear()
        self.selected_plane = None

        # reset moteur de jeu
        self.game.score = 0
        self.game.managed_planes = 0
        self.game.update_score_label()

        # reset timer survie
        self.game.survival_time = 0
        self.game.timer_label()

        # relance les timers
        self.game.survival_timer.start(1000)
        self.game.score_timer.start(10000)

        # relance spawn
        self.timer.start(16)
        self.spawn_timer.start(self.spawn_level)

        self.ui.labelinfo.setText("Cliquez sur un avion pour le contrôler")
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Simulation()
    window.showMaximized()
    sys.exit(app.exec())
