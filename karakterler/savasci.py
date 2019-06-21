import tcod as libtcod

from oyun_mesajlari import Mesaj


class Savasci:
    def __init__(self, can, zirh, guc, gorunmez_tur=0):
        self.maks_can = can
        self.can = can
        self.zirh = zirh
        self.guc = guc
        self.gorunmez_tur = gorunmez_tur

    def take_hasar(self, hasar):
        sonuclar = []

        self.can -= hasar

        if self.can <= 0:
            sonuclar.append({'katledildi': self.owner})

        return sonuclar

    def iyilestir(self, miktar):
        self.can += miktar

        if self.can > self.maks_can:
            self.can = self.maks_can

    def saldir(self, hedef):
        sonuclar = []

        hasar = self.guc - hedef.savasci.zirh

        if hasar > 0:
            sonuclar.append({'mesaj': Mesaj(
                '{0}, su hedefe vurdu: {1}. verilen hasar: {2}'.format(self.owner.isim, hedef.isim, str(hasar)),
                libtcod.white)})
            sonuclar.extend(hedef.savasci.take_hasar(hasar))

        else:
            sonuclar.append({'mesaj': Mesaj(
                '{0}, su hedefe vurdu ancak hasar veremedi: {1}'.format(self.owner.isim, hedef.isim),
                libtcod.white)})

        return sonuclar
