import pyglet

import globals
from constants import BatchNames
from constants import Resources
from ship import Ship


class Shieldbar(pyglet.sprite.Sprite):
    ship: Ship

    def __init__(self, ship: Ship):
        super(Shieldbar, self).__init__(globals.resources[Resources.Image_Shieldbar][0],
                                        batch=globals.sprite_batches[BatchNames.Health_Bar_Batch])
        self.ship = ship
        if ship.is_enemy:
            self.x = globals.window.width - 10
            self.y = globals.window.height - 27
            self.rotation = 180
        else:
            self.x = 10
            self.y = globals.window.height - 35

    def update(self, x=None, y=None, rotation=None, scale=None, scale_x=None, scale_y=None):
        if self.ship.get_shield_percentage() < 4:
            self.image = globals.resources[Resources.Image_Shieldbar][0]
        else:
            self.image = globals.resources[Resources.Image_Shieldbar][1 +
                                                                      int((self.ship.get_shield_percentage() - 5) / 16)]
        super(Shieldbar, self).update()
