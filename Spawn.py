import random
import math
from Plane import Airplane
ALT_LEVELS = [3000, 5000, 7000, 10000]

def spawn(frame, plane_img):
    """
    Génère une position aléatoire dans frame, en évitant le centre.
    Retourne (x, y, angle_random).
    """
    fw, fh = frame.width(), frame.height()

    margin = 60
    center_margin = min(fw, fh) * 0.4
    center_x = fw / 2
    center_y = fh / 2

    while True:
        x = random.randint(margin, fw - plane_img.width() - margin)
        y = random.randint(margin, fh - plane_img.height() - margin)

        dx = (x + plane_img.width() / 2) - center_x
        dy = (y + plane_img.height() / 2) - center_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > center_margin:
            angle = random.randint(0, 359)
            return x, y, angle


class SpawnManager:
    """Gère la création des avions."""
    def __init__(self, sim):
        self.sim = sim

    def spawn_plane(self):
        """
        Crée un Airplane pour la simulation:
          - position aléatoire
          - angle tourné vers le centre
          - type de vol :
              * 10% : urgence → EMERGENCY
              * 30% : arrivée normale → Atterisage
              * 60% : transit / autre destination
        Retourne l'objet Airplane (ou None si game_over).
        """

        if self.sim.game_over:
            return None

        frame = self.sim.ui.frameCenter
        x, y, _ = spawn(frame, self.sim.plane_img)

        fw, fh = frame.width(), frame.height()
        cx, cy = fw / 2, fh / 2

        plane_cx = x + self.sim.plane_img.width() / 2
        plane_cy = y + self.sim.plane_img.height() / 2

        # angle initial vers le centre
        angle_to_center = math.degrees(
            math.atan2(cx - plane_cx, plane_cy - cy)
        )

        plane = Airplane(x, y, angle_to_center, self.sim.plane_img)

        # -------- Nom du vol --------
        plane.name = random.choice([
            "AF123", "BA204", "LH330", "DL450",
            "AZ622", "LX359", "IB741", "KL902"
        ])

        # -------- Type de vol (urgence / arrivée / transit) --------
        r = random.random()

        if r < 0.10:
            plane.emergency = True
            plane.must_land = True
            plane.destination = "EMERGENCY"
            plane.altitude = 7000
            plane.target_altitude = 3000
            self.sim.emergency_sound.play()
            plane.image = self.sim.plane_emergency

        elif r < 0.30:
            plane.emergency = False
            plane.must_land = True
            plane.altitude = 5000
            plane.target_altitude = 3000
            plane.destination = "Atterisage"

        else:
            plane.emergency = False
            plane.must_land = False
            plane.altitude = float(random.choice(ALT_LEVELS[1:]))
            plane.target_altitude = plane.altitude
            plane.destination = random.choice([
                "Lille", "Lyon", "Nice", "Nantes", "Londres",
                "Toulouse", "Bruxelles", "Marseille", "Amsterdam",
                "New York", "Madrid", "Rome"
            ])

        return plane
