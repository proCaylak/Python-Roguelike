class Varlik:

    def __init__(self, x, y, char, renk, isim, engel=False, savasci=None, bilgisayar=None):
        self.x = x
        self.y = y
        self.char = char
        self.renk = renk
        self.isim = isim
        self.engel = engel
        self.savasci = savasci
        self.bilgisayar = bilgisayar

        if self.savasci:
            self.savasci.owner = self

        if self.bilgisayar:
            self.bilgisayar.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy



def engelleyen_varlik_kontrolu(varliklar, yol_x, yol_y):
    for varlik in varliklar:
        if varlik.engel and varlik.x == yol_x and varlik.y == yol_y:
            return varlik

    return None
