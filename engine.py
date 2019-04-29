import tcod as libtcod
from girdi_kontrol import tus_kontrol
from varlik import Varlik
from gorus_fonk import initialize_gorus, hesapla_gorus
from render_fonk import clear_all, render_all
from harita_nesneleri.harita import Harita


def main():
    ekran_genislik = 80
    ekran_yukseklik = 50
    harita_genislik = 80
    harita_yukseklik = 45

    oda_max_boyut = 10
    oda_min_boyut = 6
    max_oda_sayisi = 30

    gorus_algoritmasi = 0
    gorus_acik_renk_duvar = True
    gorus_yaricap = 10

    renkler = {
        'koyu_duvar': libtcod.Color(0, 0, 100),
        'koyu_zemin': libtcod.Color(50, 50, 150),
        'acik_duvar': libtcod.Color(130, 110, 50),
        'acik_zemin': libtcod.Color(200, 180, 50)
    }

    oyuncu = Varlik(int(ekran_genislik / 2), int(ekran_yukseklik / 2), '@', libtcod.green)
    npc = Varlik(int(ekran_genislik / 2 - 5), int(ekran_yukseklik / 2 - 5), '@', libtcod.yellow)
    varliklar = [npc, oyuncu]

    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(ekran_genislik, ekran_yukseklik,
                              'HIRSIZ: Zindan Yağmacısı', False)

    term = libtcod.console_new(ekran_genislik, ekran_yukseklik)

    harita = Harita(harita_genislik, harita_yukseklik)
    harita.make_harita(max_oda_sayisi, oda_min_boyut, oda_max_boyut,
                       harita_genislik, harita_yukseklik, oyuncu)

    gorus_tekrar_hesapla = True

    gorus_harita = initialize_gorus(harita)

    tus = libtcod.Key()
    fare = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, tus, fare)

        if gorus_tekrar_hesapla:
            hesapla_gorus(gorus_harita, oyuncu.x, oyuncu.y,
                          gorus_yaricap, gorus_acik_renk_duvar, gorus_algoritmasi)

        render_all(term, varliklar, harita, gorus_harita, gorus_tekrar_hesapla,
                   ekran_genislik, ekran_yukseklik, renkler)
        gorus_tekrar_hesapla = False

        libtcod.console_flush()

        clear_all(term, varliklar)

        action = tus_kontrol(tus)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not harita.is_engelli(oyuncu.x + dx, oyuncu.y + dy):
                oyuncu.move(dx, dy)

                gorus_tekrar_hesapla = True
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
