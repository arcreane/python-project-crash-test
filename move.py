import math

def move_all(sim):
    """
    Gère le déplacement de tous les avions de la simulation `sim`.
    """
    if not sim.planes:
        return

    frame = sim.ui.frameCenter
    max_w = frame.width()
    max_h = frame.height()

    for plane in list(sim.planes):
        in_bounds = plane.update_position(max_w - plane.w, max_h - plane.h)
        if not in_bounds:
            sim.planes.remove(plane)

    sim.update()
