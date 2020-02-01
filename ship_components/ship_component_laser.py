import random
from enum import Enum

from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component
import globals
from constants import Resources
from constants import BatchNames


class LaserType(Enum):
    SimpleLaser = 1
    AngleLaser = 2
    HeavyLaser = 3


class ShipComponentLaser(ship_component.ShipComponent):
    def __init__(self, x, y, owner, laser_type, *args, **kwargs):
        super(ShipComponentLaser, self).__init__(x, y, owner,
                                                 globals.resources[Resources.Image_Ship_Module_Simple_Phaser],
                                                 batch=globals.sprite_batches[BatchNames.Component_Batch],
                                                 *args, *kwargs)
        self.cd = 1
        self.laser_type = laser_type
        self.speed = 800
        self.angle = 90
        self.dmg = 0
        self.ts_check_fire = self.cd  #
        if owner.is_enemy:
            self.ts_check_fire *= random.random()

    def module_initial(self, ship):
        if self.laser_type == LaserType.SimpleLaser:
            self.init_simple_laser()
        elif self.laser_type == LaserType.AngleLaser:
            self.init_angle_laser()
        elif self.laser_type == LaserType.HeavyLaser:
            self.init_heavy_laser()

        self.ts_check_fire = self.cd
        ship.mass += self.mass

    def update(self, dt):
        super(ShipComponentLaser, self).update(dt)
        if self._owner is None:
            return

        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()

            # check: is this laser from the player or an enemy?
            direction = -1 if self._owner.is_enemy else 1

            if self.laser_type == LaserType.SimpleLaser:
                projectile = self.get_simple_laser_projectile(self._owner.x + self._local_x,
                                                              self._owner.y + self._local_y, direction)
            elif self.laser_type == LaserType.AngleLaser:
                projectile = self.get_angle_laser(self._owner.x + self._local_x,
                                                  self._owner.y + self._local_y, direction)
            elif self.laser_type == LaserType.HeavyLaser:
                projectile = self.get_heavy_laser(self._owner.x + self._local_x,
                                                  self._owner.y + self._local_y, direction)

            if self._owner.is_enemy:
                for proj in projectile:
                    globals.enemy_projectiles.append(proj)
            else:
                for proj in projectile:
                    globals.player_projectiles.append(proj)


    def init_simple_laser(self):
        self.mass = 10
        self.dmg = 10
        self.cd = 1
        self.speed = 800
        self.angle = 90

    def get_simple_laser_projectile(self, x, y, direction):
        return [ProjectileLaser(x, y, direction * self.speed, self.angle, direction, self.dmg)]

    def init_angle_laser(self):
        self.mass = 15
        self.dmg = 10
        self.cd = 1
        self.speed = 800
        # since two projectiles are created the diff between 90 and angle is taken and added to 90 for the other one
        self.angle = 70

    def get_angle_laser(self, x, y, direction):
        return [ProjectileLaser(x, y, direction * self.speed, self.angle, direction, self.dmg),
                ProjectileLaser(x, y, direction * self.speed, (90 - self.angle) + 90, direction, self.dmg)]

    def init_heavy_laser(self):
        self.mass = 50
        self.dmg = 30
        self.cd = 3
        self.speed = 1000
        self.angle = 90

    def get_heavy_laser(self, x, y, direction):
        proj = ProjectileLaser(x, y, direction * self.speed, self.angle, direction, self.dmg)
        proj.scale = 2.0
        return [proj]
