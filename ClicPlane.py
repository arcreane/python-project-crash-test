import math

class ClicManager:
    """
    Gère la détection de clic sur les avions pour une simulation donnée.
    """
    def __init__(self, sim):
        self.sim = sim

    def clic_on_plane(self, event):
        """
        Détecte si un avion est cliqué.
        Retourne l'avion ou None.
        """
        if self.sim.game_over:
            return None

        click_x = event.position().x()
        click_y = event.position().y()

        frame = self.sim.ui.frameCenter
        fx, fy = frame.x(), frame.y()

        for plane in self.sim.planes:
            cx = fx + plane.x + plane.w / 2
            cy = fy + plane.y + plane.h / 2

            dx = click_x - cx
            dy = click_y - cy
            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= 50:  # rayon de clic
                return plane

        return None