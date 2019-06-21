import tcod as libtcod

from oyun_durumu import Tur


def tus_kontrol(tus, oyun_durum):
    if oyun_durum == Tur.OYUNCU:
        return tus_oyuncu_kontrol(tus)
    elif oyun_durum in (Tur.OYUNCU_OLUM, Tur.OYUNCU_ZAFER):
        return tus_katledilen_oyuncu_kontrol(tus)
    elif oyun_durum in (Tur.ENVANTER_GOSTER, Tur.ENVANTER_ESYA_BIRAK):
        return tus_envanter_kontrol(tus)

    return {}


def tus_oyuncu_kontrol(tus):
    tus_char = chr(tus.c)

    # HAREKET
    if tus.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif tus.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif tus.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif tus.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}
    elif tus.vk == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif tus.vk == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif tus.vk == libtcod.KEY_KP3:
        return {'move': (1, 1)}
    elif tus.vk == libtcod.KEY_KP1:
        return {'move': (-1, 1)}

    # ENVANTER
    if tus_char == 'g':
        return {'pick_up': True}
    elif tus_char == 'h':
        return {'show_envanter': True}
    elif tus_char == 'b':
        return {'drop_envanter': True}

    # PENCERE İŞLEMLERİ
    if tus.vk == libtcod.KEY_ENTER and tus.lalt:
        return {'fullscreen': True}
    elif tus.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def tus_katledilen_oyuncu_kontrol(tus):
    tus_char = chr(tus.c)
    # ENVANTER
    if tus_char == 'g':
        return {'pick_up': True}
    elif tus_char == 'h':
        return {'show_envanter': True}

    # PENCERE İŞLEMLERİ
    if tus.vk == libtcod.KEY_ENTER and tus.lalt:
        return {'fullscreen': True}
    elif tus.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def tus_envanter_kontrol(tus):
    index = tus.c - ord('a')

    # ENVANTER EŞYA SEÇİMİ
    if index >= 0:
        return {'envanter_index': index}

    # PENCERE İŞLEMLERİ
    if tus.vk == libtcod.KEY_ENTER and tus.lalt:
        return {'fullscreen': True}
    elif tus.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
