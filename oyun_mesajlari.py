import tcod as libtcod

import textwrap


class Mesaj:
    def __init__(self, icerik, renk=libtcod.white):
        self.icerik = icerik
        self.renk = renk


class MesajKaydi:
    def __init__(self, x, genislik, yukseklik):
        self.mesajlar = []
        self.x = x
        self.genislik = genislik
        self.yukseklik = yukseklik

    def add_mesaj(self, mesaj):

        yeni_mesaj = textwrap.wrap(mesaj.icerik, self.genislik)

        for satir in yeni_mesaj:

            if len(self.mesajlar) == self.yukseklik:
                del self.mesajlar[0]

            self.mesajlar.append(Mesaj(satir, mesaj.renk))
