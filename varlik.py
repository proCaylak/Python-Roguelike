class Varlik:

    def __init__(self, x, y, char, renk):
        self.x = x
        self.y = y
        self.char = char
        self.renk = renk

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
