import tcod as libtcod

from oyun_mesajlari import Mesaj
from render_fonk import RenderSirasi
from oyun_durumu import Tur


def kill_oyuncu(oyuncu):
    oyuncu.char = '#'
    oyuncu.renk = libtcod.dark_red

    return Mesaj('Son nefesini verdin!', libtcod.red), Tur.OYUNCU_OLUM


def kill_dusman(dusman):
    olum_mesaji = Mesaj('{0} katledildi!'.format(dusman.isim), libtcod.orange)

    dusman.char = '%'
    dusman.renk = libtcod.dark_red
    dusman.engel = False
    dusman.savasci = None
    dusman.bilgisayar = None
    dusman.isim = dusman.isim + ' cesedi'
    dusman.render_sirasi = RenderSirasi.CESET

    return olum_mesaji
