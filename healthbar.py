import pyglet

import globals
from constants import BatchNames
from constants import Resources
from ship import Ship


class Healthbar(pyglet.sprite.Sprite):
    ship: Ship

    def __init__(self, ship: Ship):
        super(Healthbar, self).__init__(globals.resources[Resources.Image_Healthbar][0],
                                        batch=globals.sprite_batches[BatchNames.Health_Bar_Batch])
        self.ship = ship
        if ship.is_enemy:
            self.x = globals.window.width - 10
            self.y = globals.window.height - 10
            self.rotation = 180
        else:
            self.x = 10
            self.y = globals.window.height - 26

    def update(self, x=None, y=None, rotation=None, scale=None, scale_x=None, scale_y=None):
        if self.ship.get_health_percentage() < 4:
            self.image = globals.resources[Resources.Image_Healthbar][0]
        else:
            self.image = globals.resources[Resources.Image_Healthbar][1 +
                                                                      int((self.ship.get_health_percentage() - 5) / 16)]
        super(Healthbar, self).update()
