import math


class MovementManager:
    def __init__(self, sim):
        self.sim = sim

    @staticmethod
    def rotate_point(px, py, angle_deg):
        a = math.radians(angle_deg)
        rx = px * math.cos(a) - py * math.sin(a)
        ry = px * math.sin(a) + py * math.cos(a)
        return rx, ry

    def hold(self, plane):
        TURN_RATE = 1.3
        plane.angle = (plane.angle + TURN_RATE) % 360

    # -------- COLLISIONS --------
    def check_collisions(self):
        if self.sim.game_over:
            return

        n = len(self.sim.planes)
        if n < 2:
            return

        collision_radius = 30
        vertical_separation_min = 900

        for i in range(n):
            for j in range(i + 1, n):
                p1 = self.sim.planes[i]
                p2 = self.sim.planes[j]

                cx1 = p1.x + p1.w / 2
                cy1 = p1.y + p1.h / 2
                cx2 = p2.x + p2.w / 2
                cy2 = p2.y + p2.h / 2

                dx = cx2 - cx1
                dy = cy2 - cy1
                dist = math.sqrt(dx*dx + dy*dy)

                vertical_separation = abs(p1.altitude - p2.altitude)

                if dist < collision_radius and vertical_separation < vertical_separation_min:
                    self.sim.game_over = True
                    self.sim.timer.stop()
                    self.sim.spawn_timer.stop()
                    self.sim.ui.labelinfo.setText(f"⚠ COLLISION !")
                    self.sim.game.stop_all()
                    return

    # -------- MOUVEMENT GLOBAL --------
    def move_all(self):
        if self.sim.game_over:
            return
        if not self.sim.planes:
            return

        frame = self.sim.ui.frameCenter
        max_w = frame.width()
        max_h = frame.height()

        for plane in list(self.sim.planes):

            # Altitude
            plane.update_altitude()

            # HOLD
            if plane.holding:
                self.hold(plane)
                in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
                if not in_bounds:
                    self.sim.planes.remove(plane)
                continue

            # ATTERRISSAGE
            if plane.landing:
                if plane.reached_waypoint() and plane.current_wp == len(plane.waypoints) - 1:
                    self.sim.game.add_landing_score(plane)
                    self.sim.game.add_managed_plane(plane)
                    self.sim.planes.remove(plane)
                    continue

                plane.update_landing_angle()
                if plane.reached_waypoint():
                    if plane.current_wp == len(plane.waypoints) - 3:
                        plane.target_altitude = 1000
                    if plane.current_wp == len(plane.waypoints) - 2:
                        plane.target_altitude = 0
                    plane.current_wp += 1

            # MOUVEMENT NORMAL
            in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
            if not in_bounds:
                self.sim.planes.remove(plane)
                continue

        self.check_collisions()
        self.sim.update()
