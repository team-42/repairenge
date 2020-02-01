import random
from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component
import globals
from constants import Resources
from constants import BatchNames


class ShipComponentSimplePhaser(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super(ShipComponentSimplePhaser, self).__init__(10, x, y, owner,
                                                        globals.resources[Resources.Image_Ship_Module_Simple_Phaser],
                                                        batch=globals.sprite_batches[BatchNames.Component_Batch],
                                                        *args, *kwargs)
        self.cd = 1
        self.ts_check_fire = self.cd  #
        if owner.is_enemy:
            self.ts_check_fire *= random.random()

    def module_initial(self, ship):
        ship.mass += self.mass

    def update(self, dt):
        super(ShipComponentSimplePhaser, self).update(dt)
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()

            # check: is this phaser from the player or an enemy?
            if self._owner is not None:
                if self._owner.is_enemy:
                    globals.enemy_projectiles.append(
                        ProjectileLaser(self._owner.x + self._local_x, self._owner.y + self._local_y, -1)
                    )
                else:
                    globals.player_projectiles.append(
                        ProjectileLaser(self._owner.x + self._local_x, self._owner.y + self._local_y, 1)
                    )
