import tcod as libtcod

from enum import Enum


class RenderSirasi(Enum):
    CESET = 1
    ESYA = 2
    KARAKTER = 3


def render_all(terminal, varliklar, oyuncu, harita, gorus_harita, gorus_tekrar_hesapla, genislik, yukseklik, renkler):
    if gorus_tekrar_hesapla:
        for y in range(harita.yukseklik):
            for x in range(harita.genislik):
                gorunur = libtcod.map_is_in_fov(gorus_harita, x, y)
                duvar = harita.tiles[x][y].gorus_engel

                if gorunur:
                    if duvar:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('acik_duvar'))
                    else:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('acik_zemin'))

                        harita.tiles[x][y].kesfedildi = True
                elif harita.tiles[x][y].kesfedildi:
                    if duvar:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('koyu_duvar'),
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('koyu_zemin'),
                                                            libtcod.BKGND_SET)

    varliklar_render_sirali = sorted(varliklar, key=lambda x: x.render_sirasi.value)

    for varlik in varliklar_render_sirali:
        draw_varlik(terminal, varlik, gorus_harita)

    libtcod.console_set_default_foreground(terminal, libtcod.white)
    libtcod.console_print_ex(terminal, 1, yukseklik - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                             'CAN: {0:02}/{1:02}'.format(oyuncu.savasci.can, oyuncu.savasci.max_can))

    libtcod.console_blit(terminal, 0, 0, genislik, yukseklik, 0, 0, 0)


def clear_all(terminal, varliklar):
    for varlik in varliklar:
        clear_varlik(terminal, varlik)


def draw_varlik(terminal, varlik, gorus_harita):
    if libtcod.map_is_in_fov(gorus_harita, varlik.x, varlik.y):
        libtcod.console_set_default_foreground(terminal, varlik.renk)
        libtcod.console_put_char(terminal, varlik.x, varlik.y, varlik.char, libtcod.BKGND_NONE)


def clear_varlik(terminal, varlik):
    libtcod.console_put_char(terminal, varlik.x, varlik.y, ' ', libtcod.BKGND_NONE)
