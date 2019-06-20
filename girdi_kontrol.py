import tcod as libtcod


def tus_kontrol(tus):
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

    if tus.vk == libtcod.KEY_ENTER and tus.lalt:
        return {'fullscreen': True}

    elif tus.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
