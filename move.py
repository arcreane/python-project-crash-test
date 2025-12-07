import math


class MovementManager:
    """
    Gère tous les mouvements, holds, collisions, sorties d'écran, etc.
    """
    def __init__(self, sim):
        self.sim = sim

    @staticmethod
    def rotate_point(px, py, angle_deg):
        """Rotation d'un point autour de (0,0)."""
        a = math.radians(angle_deg)
        rx = px * math.cos(a) - py * math.sin(a)
        ry = px * math.sin(a) + py * math.cos(a)
        return rx, ry


    def hold(self, plane):
        """
        L'avion tourne continuellement (rate turn), mais garde sa vitesse
        => trajectoire arrondie naturelle.
        """
        TURN_RATE = 1.3  # degrés par tick (0.8 = large virage / 3 = serré)
        plane.angle = (plane.angle + TURN_RATE) % 360


    def check_collisions(self):
        """Stoppe le jeu si deux avions se percutent."""
        if self.sim.game_over:
            return

        n = len(self.sim.planes)
        if n < 2:
            return

        collision_radius = 30  # zone de collision

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
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= collision_radius:
                    self.sim.game_over = True
                    self.sim.timer.stop()
                    self.sim.spawn_timer.stop()
                    self.sim.ui.labelinfo.setText("⚠ COLLISION ! Jeu arrêté")
                    self.sim.game.stop_all()
                    return


    def send_plane_to_hold(self, plane):
        """Met un avion en hold"""
        plane.holding = True

    def release_hold(self, plane):
        """Sort l'avion du HOLD"""
        plane.holding = False

    # ==========================================================
    #   MOUVEMENT GLOBAL
    # ==========================================================
    def move_all(self):
        """Gestion du déplacement de tous les avions."""
        if self.sim.game_over:
            return
        if not self.sim.planes:
            return

        frame = self.sim.ui.frameCenter
        max_w = frame.width()
        max_h = frame.height()

        # Mise à jour de chaque avion
        for plane in list(self.sim.planes):

            # ----------- HOLD (virage continu) -------------
            if plane.holding:
                self.hold(plane)
                in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)

                if not in_bounds:
                    if plane.must_land:
                        self.sim.game.score -= 5
                        self.sim.game.update_score_label()
                    else:
                        self.sim.game.add_managed_plane(plane)

                    self.sim.planes.remove(plane)
                    if plane == self.sim.selected_plane:
                        self.sim.selected_plane = None
                continue

            # ----------- ATTERRISSAGE-------------
            if plane.landing:
                if plane.reached_waypoint() and plane.current_wp == len(plane.waypoints) - 1:
                    self.sim.game.add_landing_score(plane)
                    self.sim.game.add_managed_plane(plane)
                    self.sim.planes.remove(plane)
                    if plane == self.sim.selected_plane:
                        self.sim.selected_plane = None
                    continue

                plane.update_landing_angle()
                if plane.reached_waypoint():
                    plane.current_wp += 1

            # ----------- VOL NORMAL -------------
            in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
            if not in_bounds:
                if plane.must_land:
                    self.sim.game.score -= 5
                    self.sim.game.update_score_label()
                else:
                    self.sim.game.add_managed_plane(plane)
                self.sim.planes.remove(plane)
                if plane == self.sim.selected_plane:
                    self.sim.selected_plane = None

        self.check_collisions()
        self.sim.update()
