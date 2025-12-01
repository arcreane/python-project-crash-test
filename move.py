import math

def move_all(sim):
    """
    Gère le déplacement de tous les avions + collisions
    """
    if not sim.planes:
        return

    frame = sim.ui.frameCenter
    max_w = frame.width()
    max_h = frame.height()

    for plane in list(sim.planes):
        in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
        if not in_bounds:
            # avion sorti de l'écran
            if hasattr(sim, "game"):
                sim.game.add_managed_plane()
            sim.planes.remove(plane)

    check_collisions(sim)

    sim.update()


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
