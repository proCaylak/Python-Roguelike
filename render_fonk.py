import tcod as libtcod


def render_all(terminal, varliklar, harita, gorus_harita, gorus_tekrar_hesapla, genislik, yukseklik, renkler):
    if gorus_tekrar_hesapla:
        for y in range(harita.yukseklik):
            for x in range(harita.genislik):
                gorunur = libtcod.map_is_in_fov(gorus_harita, x, y)
                duvar = harita.tiles[x][y].gorus_engel

                if gorunur:
                    if duvar:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('acik_duvar'))
                    else:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('acik_zemin'))

                        harita.tiles[x][y].kesfedildi = True
                elif harita.tiles[x][y].kesfedildi:
                    if duvar:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('koyu_duvar'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(terminal, x, y, renkler.get('koyu_zemin'), libtcod.BKGND_SET)

    for varlik in varliklar:
        draw_varlik(terminal, varlik, gorus_harita)

    libtcod.console_blit(terminal, 0, 0, genislik, yukseklik, 0, 0, 0)


def clear_all(terminal, varliklar):
    for varlik in varliklar:
        clear_varlik(terminal, varlik)


def draw_varlik(terminal, varlik, gorus_harita):
    if libtcod.map_is_in_fov(gorus_harita, varlik.x, varlik.y):
        libtcod.console_set_default_foreground(terminal, varlik.renk)
        libtcod.console_put_char(terminal, varlik.x, varlik.y, varlik.char, libtcod.BKGND_NONE)


def clear_varlik(terminal, varlik):
    libtcod.console_put_char(terminal, varlik.x, varlik.y, ' ', libtcod.BKGND_NONE)
