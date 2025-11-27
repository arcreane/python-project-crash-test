import random
import math


def spawn(frame, plane_img):
    fw, fh = frame.width(), frame.height()

    # marge (entre bord , interdire le centre)
    margin = 60
    center_margin = min(fw, fh) * 0.4

    # Centre de la frame
    center_x = fw / 2
    center_y = fh / 2

    # Boucle pour faire spawn dans la zone admissible ( 60px du bord , zone centre)
    while True:
        x = random.randint(margin, fw - plane_img.width() - margin)
        y = random.randint(margin, fh - plane_img.height() - margin)

        # distance entre le centre (zone interdit)
        dx = (x + plane_img.width() / 2) - center_x
        dy = (y + plane_img.height() / 2) - center_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > center_margin:
            return x, y, math.degrees(math.atan2(center_y - (y + plane_img.height() / 2),
                                                 center_x - (x + plane_img.width() / 2)))
