import math
import tcod as libtcod

from render_fonk import RenderSirasi


class Varlik:

    def __init__(self, x, y, char, renk, isim, engel=False, render_sirasi=RenderSirasi.CESET, savasci=None,
                 bilgisayar=None):
        self.x = x
        self.y = y
        self.char = char
        self.renk = renk
        self.isim = isim
        self.engel = engel
        self.render_sirasi = render_sirasi
        self.savasci = savasci
        self.bilgisayar = bilgisayar

        if self.savasci:
            self.savasci.owner = self

        if self.bilgisayar:
            self.bilgisayar.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_hedef(self, hedef_x, hedef_y, harita, varliklar):
        dx = hedef_x - self.x
        dy = hedef_y - self.y
        mesafe = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / mesafe))
        dy = int(round(dy / mesafe))

        yol_x = self.x + dx
        yol_y = self.y + dy

        if not (harita.is_engelli(yol_x, yol_y) or engelleyen_varlik_kontrolu(varliklar, yol_x, yol_y)):
            self.move(dx, dy)

    def move_hedef_a_star(self, hedef, harita, varliklar):
        gorus = libtcod.map_new(harita.genislik, harita.yukseklik)

        for y1 in range(harita.yukseklik):
            for x1 in range(harita.genislik):
                libtcod.map_set_properties(gorus, x1, y1, not harita.tiles[x1][y1].gorus_engel,
                                           not harita.tiles[x1][y1].engel)

        for varlik in varliklar:
            if varlik.engel and varlik != self and varlik != hedef:
                libtcod.map_set_properties(gorus, varlik.x, varlik.y, True, False)

        rota = libtcod.path_new_using_map(gorus)  # A* rotası

        libtcod.path_compute(rota, self.x, self.y, hedef.x, hedef.y)

        if not libtcod.path_is_empty(rota) and libtcod.path_size(rota) < 25:
            x, y = libtcod.path_walk(rota, True)
            if x or y:
                self.x = x
                self.y = y

        else:
            self.move_hedef(hedef.x, hedef.y, harita, varliklar)

        libtcod.path_delete(rota)

    def mesafe_hedef(self, hedef):
        dx = hedef.x - self.x
        dy = hedef.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def engelleyen_varlik_kontrolu(varliklar, yol_x, yol_y):
    for varlik in varliklar:
        if varlik.engel and varlik.x == yol_x and varlik.y == yol_y:
            return varlik

    return None
