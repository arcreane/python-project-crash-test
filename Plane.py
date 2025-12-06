import math

class Airplane:
    counter = 1

    def __init__(self, x, y, angle_deg, image):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle_deg)
        self.speed = 3
        self.image = image
        self.w = image.width()
        self.h = image.height()

        self.name = f"Vol n°{Airplane.counter}"
        Airplane.counter += 1

        self.must_land = False
        self.emergency = False
        self.destination = "Transit"

        self.holding = False

        self.landing = False
        self.waypoints = []
        self.current_wp = 0

    def reached_waypoint(self):
        if not self.waypoints:
            return False

        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w/2
        cy = self.y + self.h/2

        return math.dist((cx, cy), (tx, ty)) < 15

    def update_landing_angle(self):
        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w/2
        cy = self.y + self.h/2

        self.angle = math.degrees(
            math.atan2(tx - cx, cy - ty)
        )

    def update_position(self, max_l, max_h):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        return 0 <= self.x <= max_l and 0 <= self.y <= max_h
