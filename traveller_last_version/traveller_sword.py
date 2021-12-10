import math as m

class Sword:
    def __init__(self, x0, y0, x1, y1, l, phi, sharp, owner):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.l = l
        self.phi = phi
        self.sharp = sharp
        self.owner = owner

    def strike(self):
        self.phi = 5 * m.pi / 12
        self.sharp = 1