import tcod as libtcod


class StandartDusman:
    def tur(self, hedef, gorus_harita, harita, varliklar, dusman_gorus_yaricap):
        sonuclar = []

        dusman = self.owner
        if libtcod.map_is_in_fov(gorus_harita, dusman.x, dusman.y) and dusman.mesafe_hedef(
                hedef) <= dusman_gorus_yaricap:

            if dusman.mesafe_hedef(hedef) >= 2:
                dusman.move_hedef_a_star(hedef, harita, varliklar)

            elif hedef.savasci.can > 0:
                saldiri_sonuclari = dusman.savasci.saldir(hedef)
                sonuclar.extend(saldiri_sonuclari)

        return sonuclar
