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
