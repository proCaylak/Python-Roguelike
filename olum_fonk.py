import tcod as libtcod

from render_fonk import RenderSirasi
from oyun_durumu import Tur

def kill_oyuncu(oyuncu):
    oyuncu.char = '#'
    oyuncu.renk = libtcod.dark_red

    return 'Hayatını kaybettin!', Tur.OYUNCU_OLUM


def kill_dusman(dusman):
    olum_mesaji = '{0} öldürüldü!'.format(dusman.isim)

    dusman.char='%'
    dusman.renk=libtcod.dark_red
    dusman.engel=False
    dusman.savasci=None
    dusman.bilgisayar=None
    dusman.isim= dusman.isim + ' cesedi'
    dusman.render_sirasi = RenderSirasi.CESET

    return olum_mesaji