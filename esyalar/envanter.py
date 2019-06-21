import tcod as libtcod

from oyun_mesajlari import Mesaj


class Envanter:
    def __init__(self, kapasite):
        self.kapasite = kapasite
        self.esyalar = []

    def add_esya(self, esya):
        sonuclar = []

        if len(self.esyalar) >= self.kapasite:
            sonuclar.append({
                'eklenen_esya': None,
                'mesaj': Mesaj('Envanter dolu, daha fazla esya tasinamiyor.', libtcod.yellow)
            })
        else:
            sonuclar.append({
                'eklenen_esya': esya,
                'mesaj': Mesaj('Envantere {0} eklendi.'.format(esya.isim), libtcod.blue)
            })

            self.esyalar.append(esya)

        return sonuclar

    def kullan(self, esya_varlik, **kwargs):
        sonuclar = []

        esya_esyalar = esya_varlik.esya

        if esya_esyalar.kullanim is None:
            sonuclar.append({'mesaj': Mesaj('{0}, kullanilamaz'.format(esya_varlik.isim), libtcod.yellow)})
        else:
            kwargs = {**esya_esyalar.fonk_kwargs, **kwargs}
            esya_kullanim_sonuclar = esya_esyalar.kullanim(self.owner, **kwargs)

            for esya_kullanim_sonuc in esya_kullanim_sonuclar:
                if esya_kullanim_sonuc.get('harcandi'):
                    self.remove_esya(esya_varlik)

                sonuclar.extend(esya_kullanim_sonuclar)

        return sonuclar

    def birak(self, esya):
        sonuclar = []

        esya.x = self.owner.x
        esya.y = self.owner.y

        self.remove_esya(esya)
        sonuclar.append({'birakilan_esya': esya,
                         'mesaj': Mesaj('Su esya envanterden cikarildi ve yere birakildi: {0}'.format(esya.isim),
                                        libtcod.yellow)})

        return sonuclar

    def remove_esya(self, esya):
        self.esyalar.remove(esya)
