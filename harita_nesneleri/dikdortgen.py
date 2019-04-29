class Dikdortgen:

    def __init__(self, x, y, gen, yuk):
        self.x1 = x
        self.y1 = y
        self.x2 = x + gen
        self.y2 = y + yuk

    def merkez(self):
        merkez_x = int((self.x1 + self.x2) / 2)
        merkez_y = int((self.y1 + self.y2) / 2)
        return (merkez_x, merkez_y)

    def cakisma(self, diger):
        return (self.x1 <= diger.x2 and self.x2 >= diger.x1 and
                self.y1 <= diger.y2 and self.y2 >= diger.y1)
