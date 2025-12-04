import math

class Plane:
    counter = 1

    def __init__(self, x, y, angle_deg, image):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle_deg)
        self.speed = 3
        self.image = image
        self.w = image.width()
        self.h = image.height()

        self.name = f"Vol n°{Plane.counter}"
        Plane.counter += 1

        self.must_land = False
        self.emergency = False
        self.destination = "Transit"

        self.holding = False

    def update_position(self, max_l, max_h):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        return 0 <= self.x <= max_l and 0 <= self.y <= max_h
