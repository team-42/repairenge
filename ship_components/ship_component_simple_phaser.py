import random
from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component
import globals
from constants import Resources
from constants import BatchNames


class ShipComponentSimplePhaser(ship_component.ShipComponent):
    def __init__(self, x, y, *args, **kwargs):
        super(ShipComponentSimplePhaser, self).__init__(10, x, y,
                                                        globals.resources[Resources.Image_Ship_Module_Simple_Phaser],
                                                        batch=globals.sprite_batches[BatchNames.Component_Batch],
                                                        *args, *kwargs)
        self.cd = 0.2
        self.ts_check_fire = self.cd

    def module_initial(self, ship):
        ship.mass += self.mass

    def module_action(self, dt):
        super(ShipComponentSimplePhaser, self).module_action(dt)
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()
            globals.projectiles.append(
                ProjectileLaser(globals.player_ship.x + self._local_x, globals.player_ship.y + self._local_y)
            )
