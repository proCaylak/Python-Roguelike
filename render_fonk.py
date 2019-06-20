import tcod as libtcod

from oyun_durumu import Tur
from menuler import envanter_menu
from enum import Enum


class RenderSirasi(Enum):
    CESET = 1
    ESYA = 2
    KARAKTER = 3


def get_imlec_altinda_isim(fare, varliklar, gorus_harita):
    (x, y) = (fare.cx, fare.cy)

    isimler = [varlik.isim for varlik in varliklar
               if varlik.x == x and varlik.y == y and libtcod.map_is_in_fov(gorus_harita, varlik.x, varlik.y)]
    isimler = ', '.join(isimler)

    return isimler


def render_durum_cubugu(durum_ekrani, x, y, toplam_genislik, isim, deger, maks, cubuk_renk, arka_plan_renk):
    cubuk_genislik = int(float(deger) / maks * toplam_genislik)

    libtcod.console_set_default_background(durum_ekrani, arka_plan_renk)
    libtcod.console_rect(durum_ekrani, x, y, toplam_genislik, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(durum_ekrani, cubuk_renk)
    if cubuk_genislik > 0:
        libtcod.console_rect(durum_ekrani, x, y, cubuk_genislik, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(durum_ekrani, libtcod.white)
    libtcod.console_print_ex(durum_ekrani, int(x + toplam_genislik / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(isim, deger, maks))


def render_all(term, durum_ekrani, varliklar, oyuncu, harita, gorus_harita, gorus_tekrar_hesapla,
               term_genislik, term_yukseklik,
               durum_cubugu_genislik, durum_cubugu_yukseklik, durum_cubugu_y,
               mesaj_kaydi, fare, renkler, oyun_durumu):
    if gorus_tekrar_hesapla:
        for y in range(harita.yukseklik):
            for x in range(harita.genislik):
                gorunur = libtcod.map_is_in_fov(gorus_harita, x, y)
                duvar = harita.tiles[x][y].gorus_engel

                if gorunur:
                    if duvar:
                        libtcod.console_set_char_background(term, x, y, renkler.get('acik_duvar'))
                    else:
                        libtcod.console_set_char_background(term, x, y, renkler.get('acik_zemin'))

                        harita.tiles[x][y].kesfedildi = True
                elif harita.tiles[x][y].kesfedildi:
                    if duvar:
                        libtcod.console_set_char_background(term, x, y, renkler.get('koyu_duvar'),
                                                            libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(term, x, y, renkler.get('koyu_zemin'),
                                                            libtcod.BKGND_SET)

    varliklar_render_sirali = sorted(varliklar, key=lambda x: x.render_sirasi.value)

    for varlik in varliklar_render_sirali:
        draw_varlik(term, varlik, gorus_harita)

    libtcod.console_blit(term, 0, 0, term_genislik, term_yukseklik, 0, 0, 0)

    if oyun_durumu in (Tur.ENVANTER_GOSTER, Tur.ENVANTER_ESYA_BIRAK):
        if oyun_durumu == Tur.ENVANTER_GOSTER:
            baslik = 'Esyanin yanindaki tusa basarak KULLAN, ESC tusuna basarak iptal et.\n'
        else:
            baslik = 'Esyanin yanindaki tusa basarak BIRAK, ESC tusuna basarak iptal et.\n'

        envanter_menu(term, baslik, oyuncu.envanter, 50, term_genislik, term_yukseklik)

    libtcod.console_set_default_background(durum_ekrani, libtcod.black)
    libtcod.console_clear(durum_ekrani)

    y = 1
    for mesaj in mesaj_kaydi.mesajlar:
        libtcod.console_set_default_foreground(durum_ekrani, mesaj.renk)
        libtcod.console_print_ex(durum_ekrani, mesaj_kaydi.x, y, libtcod.BKGND_NONE, libtcod.LEFT, mesaj.icerik)
        y += 1

    render_durum_cubugu(durum_ekrani, 1, 1, durum_cubugu_genislik, 'CAN', oyuncu.savasci.can, oyuncu.savasci.maks_can,
                        libtcod.light_red, libtcod.darker_red)

    libtcod.console_set_default_foreground(durum_ekrani, libtcod.light_gray)
    libtcod.console_print_ex(durum_ekrani, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_imlec_altinda_isim(fare, varliklar, gorus_harita))

    libtcod.console_blit(durum_ekrani, 0, 0, term_genislik, durum_cubugu_yukseklik, 0, 0, durum_cubugu_y)


def clear_all(terminal, varliklar):
    for varlik in varliklar:
        clear_varlik(terminal, varlik)


def draw_varlik(terminal, varlik, gorus_harita):
    if libtcod.map_is_in_fov(gorus_harita, varlik.x, varlik.y):
        libtcod.console_set_default_foreground(terminal, varlik.renk)
        libtcod.console_put_char(terminal, varlik.x, varlik.y, varlik.char, libtcod.BKGND_NONE)


def clear_varlik(terminal, varlik):
    libtcod.console_put_char(terminal, varlik.x, varlik.y, ' ', libtcod.BKGND_NONE)
