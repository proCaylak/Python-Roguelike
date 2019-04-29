import tcod as libtcod


def tus_kontrol(tus):
    if tus.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif tus.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif tus.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif tus.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if tus.vk == libtcod.KEY_ENTER and tus.lalt:
        return {'fullscreen': True}

    elif tus.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}
