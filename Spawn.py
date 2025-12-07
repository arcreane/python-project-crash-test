import random
import math
from Plane import Plane


def spawn_raw(frame, plane_img):
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
            angle = math.degrees(
                math.atan2(center_y - (y + plane_img.height() / 2),
                           center_x - (x + plane_img.width() / 2))
            )
            return x, y, angle


class SpawnManager:
    def __init__(self, sim):
        self.sim = sim

    def spawn_plane(self):
        x, y, angle = spawn_raw(self.sim.ui.frameCenter, self.sim.plane_img)
        plane = Plane(x, y, angle, self.sim.plane_img)

        r = random.random()
        if r < 0.10:
            plane.emergency = True
            plane.must_land = True
            plane.destination = "Piste 21 (EMERGENCY)"
        elif r < 0.30:
            plane.must_land = True
            plane.destination = "Piste 21"
        else:
            plane.must_land = False
            plane.destination = random.choice([
                "Paris",
                "Lyon",
                "Nice",
                "Lille",
                "Toulouse",
                "Nantes",
                "Bruxelles"])

        return plane