import math
import random

ALT_LEVELS = [3000, 5000, 7000, 10000]


class Airplane:
    def __init__(self, x, y, angle_deg, image):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle_deg)
        self.speed = 1.5

        self.image = image
        self.w = image.width()
        self.h = image.height()

        # Atterrissage
        self.destination = "Transit"
        self.must_land = False
        self.landing = False
        self.waypoints = []
        self.current_wp = 0
        self.holding = False
        self.emergency = False

        self.altitude = float(random.choice(ALT_LEVELS[1:]))
        self.target_altitude = self.altitude
        self.vertical_speed = 600.0

    def update_landing_angle(self):
        if not self.landing or not self.waypoints:
            return

        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        self.angle = math.degrees(math.atan2(
            tx - cx,
            cy - ty
        ))

    def reached_waypoint(self):
        if not self.waypoints:
            return False

        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        dist = math.sqrt((cx - tx)**2 + (cy - ty)**2)
        return dist < 20

    def update_position(self, max_w, max_h):
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed
        return 0 <= self.x <= max_w and 0 <= self.y <= max_h

    def update_altitude(self):
        climb = self.vertical_speed / 60.0  # ft/frame

        diff = self.target_altitude - self.altitude

        if abs(diff) <= climb:
            self.altitude = self.target_altitude
            return

        if diff > 0:
            self.altitude += climb
        else:
            self.altitude -= climb
