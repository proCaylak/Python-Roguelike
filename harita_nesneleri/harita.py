import tcod as libtcod
from random import randint

from esya_fonk import iyilestir
from esyalar.esya import Esya
from render_fonk import RenderSirasi
from karakterler.savasci import Savasci
from karakterler.bilgisayar import StandartDusman
from varlik import Varlik
from harita_nesneleri.tile import Tile
from harita_nesneleri.dikdortgen import Dikdortgen


class Harita:

    def __init__(self, genislik, yukseklik):
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.yukseklik)] for x in range(self.genislik)]

        return tiles

    def make_harita(self, max_oda_sayisi, oda_min_boyut, oda_max_boyut, harita_genislik, harita_yukseklik, oyuncu,
                    varliklar, maks_oda_basina_dusman, maks_oda_basina_esya):
        odalar = []
        oda_sayisi = 0

        for r in range(max_oda_sayisi):
            gen = randint(oda_min_boyut, oda_max_boyut)
            yuk = randint(oda_min_boyut, oda_max_boyut)

            x = randint(0, harita_genislik - gen - 1)
            y = randint(0, harita_yukseklik - yuk - 1)

            yeni_oda = Dikdortgen(x, y, gen, yuk)

            for diger_oda in odalar:
                if yeni_oda.cakisma(diger_oda):
                    break
            else:
                self.create_oda(yeni_oda)

                (yeni_x, yeni_y) = yeni_oda.merkez()

                if oda_sayisi == 0:
                    oyuncu.x = yeni_x
                    oyuncu.y = yeni_y
                else:
                    (onceki_x, onceki_y) = odalar[oda_sayisi - 1].merkez()

                    if randint(0, 1) == 1:
                        self.create_yatay_tunel(onceki_x, yeni_x, onceki_y)
                        self.create_dikey_tunel(onceki_y, yeni_y, onceki_x)
                    else:
                        self.create_dikey_tunel(onceki_y, yeni_y, onceki_x)
                        self.create_yatay_tunel(onceki_x, yeni_x, onceki_y)

                self.place_varlik(yeni_oda, varliklar, maks_oda_basina_dusman, maks_oda_basina_esya)

                odalar.append(yeni_oda)
                oda_sayisi += 1

    def create_oda(self, oda):
        for x in range(oda.x1 + 1, oda.x2):
            for y in range(oda.y1 + 1, oda.y2):
                self.tiles[x][y].engel = False
                self.tiles[x][y].gorus_engel = False

    def create_yatay_tunel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)):
            self.tiles[x][y].engel = False
            self.tiles[x][y].gorus_engel = False

    def create_dikey_tunel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].engel = False
            self.tiles[x][y].gorus_engel = False

    def place_varlik(self, oda, varliklar, maks_oda_basina_dusman, maks_oda_basina_esya):

        dusman_sayisi = randint(0, maks_oda_basina_dusman)
        esya_sayisi = randint(0, maks_oda_basina_esya)

        for i in range(dusman_sayisi):
            x = randint(oda.x1 + 1, oda.x2 - 1)
            y = randint(oda.y1 + 1, oda.y2 - 1)

            if not any([varlik for varlik in varliklar if varlik.x == x and varlik.y == y]):
                if randint(0, 100) < 80:
                    savasci_karakter = Savasci(can=10, zirh=0, guc=3)
                    yapay_zeka = StandartDusman()

                    dusman = Varlik(x, y, 'a', libtcod.dark_red, 'Er', engel=True, render_sirasi=RenderSirasi.KARAKTER,
                                    savasci=savasci_karakter, bilgisayar=yapay_zeka)
                else:
                    savasci_karakter = Savasci(can=16, zirh=1, guc=4)
                    yapay_zeka = StandartDusman()

                    dusman = Varlik(x, y, 'b', libtcod.light_red, 'Onbasi', engel=True,
                                    render_sirasi=RenderSirasi.KARAKTER,
                                    savasci=savasci_karakter, bilgisayar=yapay_zeka)

                varliklar.append(dusman)

        for i in range(esya_sayisi):
            x = randint(oda.x1 + 1, oda.x2 - 1)
            y = randint(oda.y1 + 1, oda.y2 - 1)

            if not any([varlik for varlik in varliklar if varlik.x == x and varlik.y == y]):
                esya_esyalar = Esya(kullanim=iyilestir, miktar=4)
                esya = Varlik(x, y, '+', libtcod.violet, 'Can iksiri', render_sirasi=RenderSirasi.ESYA,
                              esya=esya_esyalar)

                varliklar.append(esya)

    def is_engelli(self, x, y):
        if self.tiles[x][y].engel:
            return True

        return False
