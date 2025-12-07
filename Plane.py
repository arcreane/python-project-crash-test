import math


class Airplane:
    def __init__(self, x, y, angle_deg, image):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle_deg)
        self.speed = 1.5

        self.image = image
        self.w = image.width()
        self.h = image.height()

        # Atterrissage / tour de piste
        self.destination = "Transit"
        self.must_land = False

        self.landing = False
        self.waypoints = []
        self.current_wp = 0

        self.holding = False
        self.emergency = False

    def update_landing_angle(self):
        """Oriente l'avion vers le waypoint courant."""
        if not self.landing or not self.waypoints:
            return

        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        # repère avion : x += sin, y -= cos
        self.angle = math.degrees(math.atan2(
            tx - cx,
            cy - ty
        ))

    def reached_waypoint(self):
        """Retourne True si on est proche du waypoint courant."""
        if not self.waypoints:
            return False
        tx, ty = self.waypoints[self.current_wp]
        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        dist = math.sqrt((cx - tx) ** 2 + (cy - ty) ** 2)
        return dist < 20  # tolérance

    def update_position(self, max_w, max_h):
        """Avance l'avion selon son cap et sa vitesse."""
        rad = math.radians(self.angle)
        self.x += math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed
        return 0 <= self.x <= max_w and 0 <= self.y <= max_h

