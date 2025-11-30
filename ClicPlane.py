import math

def click_on_plane(event, sim):
    """
    Détecte si un avion est cliqué.
    Retourne l'avion cliqué ou None.
    """
    click_x = event.position().x()
    click_y = event.position().y()

    frame = sim.ui.frameCenter
    fx, fy = frame.x(), frame.y()

    for plane in sim.planes:
        cx = fx + plane.x + plane.w / 2
        cy = fy + plane.y + plane.h / 2

        dx = click_x - cx
        dy = click_y - cy
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= 50:  # rayon de clic
            return plane

    return None
