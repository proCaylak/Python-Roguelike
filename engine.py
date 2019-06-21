import tcod as libtcod

from esyalar.envanter import Envanter
from oyun_mesajlari import Mesaj, MesajKaydi
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

    durum_ekran_genislik = 20
    durum_ekran_yukseklik = 7
    durum_ekran_y = ekran_yukseklik - durum_ekran_yukseklik

    mesaj_x = durum_ekran_genislik + 2
    mesaj_genislik = ekran_genislik - durum_ekran_genislik - 2
    mesaj_yukseklik = durum_ekran_yukseklik - 1

    harita_genislik = 80
    harita_yukseklik = 43

    oda_max_boyut = 10
    oda_min_boyut = 6
    max_oda_sayisi = 30

    gorus_algoritmasi = 0
    gorus_acik_renk_duvar = True
    gorus_yaricap = 10

    maks_oda_basina_dusman = 3
    maks_oda_basina_esya = 2

    renkler = {
        'koyu_duvar': libtcod.Color(0, 0, 100),
        'koyu_zemin': libtcod.Color(50, 50, 150),
        'acik_duvar': libtcod.Color(130, 110, 50),
        'acik_zemin': libtcod.Color(200, 180, 50)
    }

    savasci_karakter = Savasci(can=30, zirh=2, guc=5)
    envanter_esyalar = Envanter(26)
    oyuncu = Varlik(0, 0, '@', libtcod.green, 'HIRSIZ', engel=True, render_sirasi=RenderSirasi.KARAKTER,
                    savasci=savasci_karakter, envanter=envanter_esyalar)
    varliklar = [oyuncu]

    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(ekran_genislik, ekran_yukseklik,
                              'HIRSIZ: Zindan Yağmacısı', False)

    term = libtcod.console_new(ekran_genislik, ekran_yukseklik)
    durum_ekran = libtcod.console_new(ekran_genislik, durum_ekran_yukseklik)

    harita = Harita(harita_genislik, harita_yukseklik)
    harita.make_harita(max_oda_sayisi, oda_min_boyut, oda_max_boyut,
                       harita_genislik, harita_yukseklik, oyuncu, varliklar, maks_oda_basina_dusman,
                       maks_oda_basina_esya)

    gorus_tekrar_hesapla = True

    gorus_harita = initialize_gorus(harita)

    mesaj_kaydi = MesajKaydi(mesaj_x, mesaj_genislik, mesaj_yukseklik)

    tus = libtcod.Key()
    fare = libtcod.Mouse()

    oyun_durumu = Tur.OYUNCU
    onceki_oyun_durumu = oyun_durumu


    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, tus, fare)

        if gorus_tekrar_hesapla:
            hesapla_gorus(gorus_harita, oyuncu.x, oyuncu.y,
                          gorus_yaricap, gorus_acik_renk_duvar, gorus_algoritmasi)

        render_all(term, durum_ekran, varliklar, oyuncu, harita, gorus_harita, gorus_tekrar_hesapla,
                   ekran_genislik, ekran_yukseklik, durum_ekran_genislik, durum_ekran_yukseklik, durum_ekran_y,
                   mesaj_kaydi, fare, renkler, oyun_durumu)
        gorus_tekrar_hesapla = False

        libtcod.console_flush()

        clear_all(term, varliklar)

        action = tus_kontrol(tus, oyun_durumu)

        move = action.get('move')
        pick_up = action.get('pick_up')
        show_envanter = action.get('show_envanter')
        drop_envanter = action.get('drop_envanter')
        envanter_index = action.get('envanter_index')
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

        elif pick_up and oyun_durumu == Tur.OYUNCU:
            for varlik in varliklar:
                if varlik.esya and varlik.x == oyuncu.x and varlik.y == oyuncu.y:
                    pick_up_sonuclar = oyuncu.envanter.add_esya(varlik)
                    oyuncu_tur_sonuclar.extend(pick_up_sonuclar)

                    break
            else:
                mesaj_kaydi.add_mesaj(Mesaj('Burada alinabilecek hicbir sey yok.', libtcod.yellow))

        if show_envanter:
            onceki_oyun_durumu = oyun_durumu
            oyun_durumu = Tur.ENVANTER_GOSTER

        if drop_envanter:
            onceki_oyun_durumu = oyun_durumu
            oyun_durumu = Tur.ENVANTER_ESYA_BIRAK

        if envanter_index is not None and onceki_oyun_durumu != Tur.OYUNCU_OLUM and envanter_index < len(
                oyuncu.envanter.esyalar):
            esya = oyuncu.envanter.esyalar[envanter_index]

            if oyun_durumu == Tur.ENVANTER_GOSTER:
                oyuncu_tur_sonuclar.extend(oyuncu.envanter.kullan(esya, varliklar=varliklar, gorus_harita=gorus_harita))
            elif oyun_durumu == Tur.ENVANTER_ESYA_BIRAK:
                oyuncu_tur_sonuclar.extend(oyuncu.envanter.birak(esya))

        if exit:
            if oyun_durumu in (Tur.ENVANTER_GOSTER, Tur.ENVANTER_ESYA_BIRAK):
                oyun_durumu = onceki_oyun_durumu
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for oyuncu_tur_sonuc in oyuncu_tur_sonuclar:
            mesaj = oyuncu_tur_sonuc.get('mesaj')
            olu_varlik = oyuncu_tur_sonuc.get('katledildi')
            eklenen_esya = oyuncu_tur_sonuc.get('eklenen_esya')
            harcanan_esya = oyuncu_tur_sonuc.get('harcandi')
            birakilan_esya = oyuncu_tur_sonuc.get('birakilan_esya')


            if mesaj:
                mesaj_kaydi.add_mesaj(mesaj)

            if olu_varlik:
                if olu_varlik == oyuncu:
                    mesaj, oyun_durumu = kill_oyuncu(olu_varlik)
                else:
                    mesaj = kill_dusman(olu_varlik)

                mesaj_kaydi.add_mesaj(mesaj)

            if eklenen_esya:
                varliklar.remove(eklenen_esya)

                oyun_durumu = Tur.DUSMAN

            if harcanan_esya:
                oyun_durumu = Tur.DUSMAN

            if birakilan_esya:
                varliklar.append(birakilan_esya)

                oyun_durumu = Tur.DUSMAN

        if oyun_durumu == Tur.DUSMAN:
            if oyuncu.savasci.gorunmez_tur > 0:
                dusman_gorus_katsayi = 0
                oyuncu.savasci.gorunmez_tur -= 1

                if oyuncu.savasci.gorunmez_tur == 0:
                    mesaj_kaydi.add_mesaj(Mesaj('Gorunmezlik pelerini tukendi', libtcod.yellow))
                else:
                    mesaj_kaydi.add_mesaj(Mesaj('Kalan gorunmezlik tur sayisi: {0}'.format(
                        oyuncu.savasci.gorunmez_tur), libtcod.yellow))

            else:
                oyuncu.savasci.gorunmez_tur = 0
                dusman_gorus_katsayi = 0.75

            for varlik in varliklar:
                if varlik.bilgisayar:

                    dusman_gorus_yaricap = int(gorus_yaricap * dusman_gorus_katsayi)
                    dusman_tur_sonuclar = varlik.bilgisayar.tur(oyuncu, gorus_harita, harita, varliklar,
                                                                dusman_gorus_yaricap)

                    for dusman_tur_sonuc in dusman_tur_sonuclar:
                        mesaj = dusman_tur_sonuc.get('mesaj')
                        olu_varlik = dusman_tur_sonuc.get('katledildi')

                        if mesaj:
                            mesaj_kaydi.add_mesaj(mesaj)

                        if olu_varlik:
                            if olu_varlik == oyuncu:
                                mesaj, oyun_durumu = kill_oyuncu(olu_varlik)
                            else:
                                mesaj = kill_dusman(olu_varlik)

                            mesaj_kaydi.add_mesaj(mesaj)

                            if oyun_durumu == Tur.OYUNCU_OLUM:
                                break
                    if oyun_durumu == Tur.OYUNCU_OLUM:
                        break
            else:
                oyun_durumu = Tur.OYUNCU


if __name__ == '__main__':
    main()
