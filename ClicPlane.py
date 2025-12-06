import math

class ClickManager:
    def __init__(self, sim):
        self.sim = sim

    def click(self, event):
        click_x = event.position().x()
        click_y = event.position().y()

        frame = self.sim.ui.frameCenter
        fx, fy = frame.x(), frame.y()

        for plane in self.sim.planes:
            cx = fx + plane.x + plane.w/2
            cy = fy + plane.y + plane.h/2
            if math.dist((click_x, click_y), (cx, cy)) < 40:
                return plane
        return None
