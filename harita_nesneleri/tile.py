class Tile:

    def __init__(self, engel, gorus_engel=None):
        self.engel = engel

        if gorus_engel is None:
            gorus_engel = engel

        self.gorus_engel = gorus_engel

        self.kesfedildi = False
