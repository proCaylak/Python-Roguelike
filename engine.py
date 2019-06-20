import tcod as libtcod

from olum_fonk import kill_oyuncu, kill_dusman
from karakterler.savasci import Savasci
from oyun_durumu import Tur
from girdi_kontrol import tus_kontrol
from varlik import Varlik, engelleyen_varlik_kontrolu
from gorus_fonk import initialize_gorus, hesapla_gorus
from render_fonk import clear_all, render_all, RenderSirasi
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

    maks_oda_basina_dusman = 3

    renkler = {
        'koyu_duvar': libtcod.Color(0, 0, 100),
        'koyu_zemin': libtcod.Color(50, 50, 150),
        'acik_duvar': libtcod.Color(130, 110, 50),
        'acik_zemin': libtcod.Color(200, 180, 50)
    }

    savasci_karakter = Savasci(can=30, zirh=2, guc=5)
    oyuncu = Varlik(0, 0, '@', libtcod.green, 'HIRSIZ', engel=True, render_sirasi=RenderSirasi.KARAKTER,
                    savasci=savasci_karakter)
    varliklar = [oyuncu]

    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(ekran_genislik, ekran_yukseklik,
                              'HIRSIZ: Zindan Yağmacısı', False)

    term = libtcod.console_new(ekran_genislik, ekran_yukseklik)

    harita = Harita(harita_genislik, harita_yukseklik)
    harita.make_harita(max_oda_sayisi, oda_min_boyut, oda_max_boyut,
                       harita_genislik, harita_yukseklik, oyuncu, varliklar, maks_oda_basina_dusman)

    gorus_tekrar_hesapla = True

    gorus_harita = initialize_gorus(harita)

    tus = libtcod.Key()
    fare = libtcod.Mouse()

    oyun_durumu = Tur.OYUNCU

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, tus, fare)

        if gorus_tekrar_hesapla:
            hesapla_gorus(gorus_harita, oyuncu.x, oyuncu.y,
                          gorus_yaricap, gorus_acik_renk_duvar, gorus_algoritmasi)

        render_all(term, varliklar, oyuncu, harita, gorus_harita, gorus_tekrar_hesapla,
                   ekran_genislik, ekran_yukseklik, renkler)
        gorus_tekrar_hesapla = False

        libtcod.console_flush()

        clear_all(term, varliklar)

        action = tus_kontrol(tus)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        oyuncu_tur_sonuclar = []

        if move and oyun_durumu == Tur.OYUNCU:
            dx, dy = move
            yol_x = oyuncu.x + dx
            yol_y = oyuncu.y + dy

            if not harita.is_engelli(yol_x, yol_y):
                hedef = engelleyen_varlik_kontrolu(varliklar, yol_x, yol_y)

                if hedef:
                    saldiri_sonuclari = oyuncu.savasci.saldir(hedef)
                    oyuncu_tur_sonuclar.extend(saldiri_sonuclari)

                else:
                    oyuncu.move(dx, dy)

                    gorus_tekrar_hesapla = True
                oyun_durumu = Tur.DUSMAN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for oyuncu_tur_sonuc in oyuncu_tur_sonuclar:
            mesaj = oyuncu_tur_sonuc.get('mesaj')
            olu_varlik = oyuncu_tur_sonuc.get('öldü')

            if mesaj:
                print(mesaj)

            if olu_varlik:
                if olu_varlik == oyuncu:
                    mesaj, oyun_durumu = kill_oyuncu(olu_varlik)
                else:
                    mesaj = kill_dusman(olu_varlik)

                print(mesaj)

        if oyun_durumu == Tur.DUSMAN:
            for varlik in varliklar:
                if varlik.bilgisayar:
                    dusman_tur_sonuclar = varlik.bilgisayar.tur(oyuncu, gorus_harita, harita, varliklar)

                    for dusman_tur_sonuc in dusman_tur_sonuclar:
                        mesaj = dusman_tur_sonuc.get('mesaj')
                        olu_varlik = dusman_tur_sonuc.get('öldü')

                        if mesaj:
                            print(mesaj)

                        if olu_varlik:
                            if olu_varlik == oyuncu:
                                mesaj, oyun_durumu = kill_oyuncu(olu_varlik)
                            else:
                                mesaj = kill_dusman(olu_varlik)

                            print(mesaj)

                            if oyun_durumu == Tur.OYUNCU_OLUM:
                                break
                    if oyun_durumu == Tur.OYUNCU_OLUM:
                        break
            else:
                oyun_durumu = Tur.OYUNCU


if __name__ == '__main__':
    main()
