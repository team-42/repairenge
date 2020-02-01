import random
from enum import Enum

from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component
import globals
from constants import Resources
from constants import BatchNames


class LaserType(Enum):
    SimpleLaser = 1
    StrongLaser = 2


class ShipComponentLaser(ship_component.ShipComponent):
    def __init__(self, x, y, owner, laser_type, *args, **kwargs):
        super(ShipComponentLaser, self).__init__(10, x, y, owner,
                                                 globals.resources[Resources.Image_Ship_Module_Simple_Phaser],
                                                 batch=globals.sprite_batches[BatchNames.Component_Batch],
                                                 *args, *kwargs)
        self.cd = 1
        self.laser_type = laser_type
        self.speed = 800
        self.angle = 90
        self.ts_check_fire = self.cd  #
        if owner.is_enemy:
            self.ts_check_fire *= random.random()

    def module_initial(self, ship):
        if self.laser_type == LaserType.SimpleLaser:
            self.init_simple_laser()
        elif self.laser_type == LaserType.StrongLaser:
            pass

        self.ts_check_fire = self.cd
        ship.mass += self.mass

    def module_action(self, dt):
        super(ShipComponentLaser, self).module_action(dt)
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()

            # check: is this laser from the player or an enemy?
            direction = -1 if self._owner.is_enemy else 1

            if self.laser_type == LaserType.SimpleLaser:
                projectile = self.get_simple_laser_projectile(self._owner.x + self._local_x,
                                                              self._owner.y + self._local_y, direction)

            if self._owner.is_enemy:
                globals.enemy_projectiles.append(projectile)
            else:
                globals.player_projectiles.append(projectile)

    def init_simple_laser(self):
        self.mass = 10
        self.cd = 1
        self.speed = 800
        self.angle = 90

    def get_simple_laser_projectile(self, x, y, direction):
        return ProjectileLaser(x, y, direction * self.speed, self.angle, direction)
