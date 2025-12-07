import math

class MovementManager:
    def __init__(self, sim):
        self.sim = sim

    def move_plane(self, plane, max_w, max_h):
        # HOLD
        if plane.holding:
            plane.angle = (plane.angle + 1.5) % 360

        return plane.update_position(max_w, max_h)

    def move_all(self):
        frame = self.sim.ui.frameCenter
        max_w = frame.width()
        max_h = frame.height()

        for plane in list(self.sim.planes):
            alive = self.move_plane(plane, max_w - plane.w, max_h - plane.h)
            if not alive:
                self.sim.planes.remove(plane)
    TURN_RATE = 1.5

    for plane in list(sim.planes):
        in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
        if plane.holding:
            plane.angle = (plane.angle + TURN_RATE) % 360

        if not in_bounds:
            # avion sorti de l'écran
            if hasattr(sim, "game"):
                sim.game.add_managed_plane()
            sim.planes.remove(plane)

    check_collisions(sim)

        self.sim.update()

    def check_collisions(sim):
        """
        Si deux avions sont trop proches, on arrête la partie.
        """
        n = len(sim.planes)
        if n < 2:
            return

        collision_radius = 30

        for i in range(n):
            for j in range(i + 1, n):
                p1 = sim.planes[i]
                p2 = sim.planes[j]

                cx1 = p1.x + p1.w / 2
                cy1 = p1.y + p1.h / 2
                cx2 = p2.x + p2.w / 2
                cy2 = p2.y + p2.h / 2

                dx = cx2 - cx1
                dy = cy2 - cy1
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= collision_radius:
                    sim.game_over = True
                    sim.timer.stop()
                    sim.spawn_timer.stop()
                    if hasattr(sim, "game"):
                        sim.game.stop_all()
                    return
