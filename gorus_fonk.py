import tcod as libtcod


def initialize_gorus(harita):
    gorus_harita = libtcod.map_new(harita.genislik, harita.yukseklik)

    for y in range(harita.yukseklik):
        for x in range(harita.genislik):
            libtcod.map_set_properties(gorus_harita, x, y,
                                       not harita.tiles[x][y].gorus_engel,
                                       not harita.tiles[x][y].engel)

    return gorus_harita


def hesapla_gorus(gorus_harita, x, y, yaricap, acik_duvar=True, algoritma=0):
    libtcod.map_compute_fov(gorus_harita, x, y, yaricap, acik_duvar, algoritma)
