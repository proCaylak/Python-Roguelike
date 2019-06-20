class Savasci:
    def __init__(self, can, zirh, guc):
        self.max_can = can
        self.can = can
        self.zirh = zirh
        self.guc = guc

    def take_hasar(self, hasar):
        sonuclar = []

        self.can -= hasar

        if self.can <= 0:
            sonuclar.append({'öldü': self.owner})

        return sonuclar

    def saldir(self, hedef):
        sonuclar = []

        hasar = self.guc - hedef.savasci.zirh

        if hasar > 0:
            hedef.savasci.take_hasar(hasar)
            sonuclar.append({'mesaj': '{0}, şu hedefe saldırdı: {1}\n verilen hasar: {2}'.format(self.owner.isim,
                                                                                                 hedef.isim,
                                                                                                 str(hasar))})
            sonuclar.extend(hedef.savasci.take_hasar(hasar))

        else:
            sonuclar.append({'mesaj': "{0}, şu hedefe saldırdı ancak hasar veremedi: {1}".format(self.owner.isim,
                                                                                                 hedef.isim)})

        return sonuclar
