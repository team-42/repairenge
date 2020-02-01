import pyglet
from constants import GameObjects
import random

from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component


class ShipComponentSimplePhaser(ship_component.ShipComponent):
    def __init__(self, x, y, *args, **kwargs):
        ship_image = pyglet.resource.image("resources/ship/simple_phaser.png")

        super(ShipComponentSimplePhaser, self).__init__(10, x, y, ship_image, *args, *kwargs)
        self.cd = 0.2
        self.ts_check_fire = self.cd

    def module_initial(self, ship):
        ship.mass += self.mass

    def module_action(self, dt, game_objects):
        super(ShipComponentSimplePhaser, self).module_action(dt, game_objects)
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()
            ship_x = game_objects[GameObjects.Ship].x
            ship_y = game_objects[GameObjects.Ship].y
            game_objects[GameObjects.Projectiles].append(
                ProjectileLaser(ship_x + self._local_x, ship_y + self._local_y))
