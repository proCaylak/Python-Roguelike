import tcod as libtcod

from oyun_mesajlari import Mesaj


def iyilestir(*args, **kwargs):
    varlik = args[0]
    miktar = kwargs.get('miktar')

    sonuclar = []

    if varlik.savasci.can == varlik.savasci.maks_can:
        sonuclar.append(
            {'harcandi': False, 'mesaj': Mesaj('Karakter maksimum canda, iksir harcanmadi.', libtcod.yellow)})
    else:
        varlik.savasci.iyilestir(miktar)
        sonuclar.append(
            {'harcandi': True, 'mesaj': Mesaj('Karakter kendisini daha iyi hissediyor.', libtcod.green)})

    return sonuclar


def gorunmezlik(*args, **kwargs):
    varlik = args[0]
    tur_sayisi = kwargs.get('tur_sayisi')

    sonuclar = []

    varlik.savasci.gorunmez_tur += tur_sayisi
    if varlik.savasci.gorunmez_tur == tur_sayisi:
        sonuclar.append(
            {'harcandi': True, 'mesaj': Mesaj('{0}, {1} tur boyunca gorunmez'.format(varlik.isim, tur_sayisi))})
    else:
        sonuclar.append(
            {'harcandi': True, 'mesaj': Mesaj('{0}, {1} tur daha gorunmez'.format(varlik.isim, tur_sayisi))})

    return sonuclar


def throw_cirit(*args, **kwargs):
    atici = args[0]
    varliklar = kwargs.get('varliklar')
    gorus_harita = kwargs.get('gorus_harita')
    hasar = kwargs.get('hasar')
    maks_menzil = kwargs.get('maks_menzil')

    sonuclar = []

    hedef = None
    en_yakin_mesafe = maks_menzil + 1

    for varlik in varliklar:
        if varlik.savasci and varlik != atici and libtcod.map_is_in_fov(gorus_harita, varlik.x, varlik.y):
            mesafe = atici.mesafe_hedef(varlik)

            if mesafe < en_yakin_mesafe:
                hedef = varlik
                en_yakin_mesafe = mesafe

    if hedef:
        sonuclar.append({'harcandi': True, 'hedef': hedef, 'mesaj': Mesaj(
            'Cirit atarak su hedefi vurdun: {0}. Verilen hasar: {1}'.format(hedef.isim, hasar))})
        sonuclar.extend(hedef.savasci.take_hasar(hasar))
    else:
        sonuclar.append(
            {'harcandi': False, 'hedef': None, 'mesaj': Mesaj('Hicbir dusman cirit menzilinde degil!', libtcod.red)})

    return sonuclar
