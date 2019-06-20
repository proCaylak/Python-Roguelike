import tcod as libtcod


def menu(term, baslik, secenekler, genislik, ekran_genislik, ekran_yukseklik):
    if len(secenekler) > 26: raise ValueError('26 secenekten fazla menu olusturulamaz!')

    baslik_yukseklik = libtcod.console_get_height_rect(term, 0, 0, genislik, ekran_yukseklik, baslik)
    yukseklik = len(secenekler) + baslik_yukseklik

    pencere = libtcod.console_new(genislik, yukseklik)

    libtcod.console_set_default_foreground(pencere, libtcod.white)
    libtcod.console_print_rect_ex(pencere, 0, 0, genislik, yukseklik, libtcod.BKGND_NONE, libtcod.LEFT, baslik)

    y = baslik_yukseklik
    harf_indeksi = ord('a')
    for secenek in secenekler:
        text = '(' + chr(harf_indeksi) + ') ' + secenek
        libtcod.console_print_ex(pencere, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        harf_indeksi += 1

    x = int(ekran_genislik / 2 - genislik / 2)
    y = int(ekran_yukseklik / 2 - yukseklik / 2)
    libtcod.console_blit(pencere, 0, 0, genislik, yukseklik, 0, x, y, 1.0, 0.7)


def envanter_menu(term, baslik, envanter, envanter_genislik, ekran_genislik, ekran_yukseklik):
    if len(envanter.esyalar) == 0:
        secenekler = ['Envanter bos.']
    else:
        secenekler = [esya.isim for esya in envanter.esyalar]

    menu(term, baslik, secenekler, envanter_genislik, ekran_genislik, ekran_yukseklik)
