import math

class Plane:
    id_counter = 1

    def __init__(self, x, y, angle_deg, image):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle_deg)
        self.speed = 3
        self.image = image
        self.w = image.width()
        self.h = image.height()

        self.name = f"FLT{Plane.id_counter}"
        Plane.id_counter += 1

    def update_position(self, max_l, max_h):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        return 0 <= self.x <= max_l and 0 <= self.y <= max_h
