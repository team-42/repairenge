import random
from enum import Enum

import util
from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component
import globals
from constants import Resources, Controls
from constants import BatchNames


class LaserType(Enum):
    SimpleLaser = 1
    AngleLaser = 2
    HeavyLaser = 3
    RailGun = 4


class ShipComponentLaser(ship_component.ShipComponent):
    def __init__(self, x, y, owner, laser_type, *args, **kwargs):
        if laser_type == LaserType.HeavyLaser:
            image = globals.resources[Resources.Image_Ship_Module_Heavy_Laser]
        elif laser_type == LaserType.AngleLaser:
            image = globals.resources[Resources.Image_Ship_Module_Angle_Laser]
        else:
            image = globals.resources[Resources.Image_Ship_Module_Simple_Phaser]
        super(ShipComponentLaser, self).__init__(x, y, owner, image,
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
        super(ShipComponentLaser, self).module_initial(ship)
        if self.laser_type == LaserType.SimpleLaser:
            self.init_simple_laser()
        elif self.laser_type == LaserType.AngleLaser:
            self.init_angle_laser()
        elif self.laser_type == LaserType.HeavyLaser:
            self.init_heavy_laser()
        elif self.laser_type == LaserType.RailGun:
            self.init_rail_gun()

        self.ts_check_fire = self.cd
        ship.mass += self.mass

    def update(self, dt):
        super(ShipComponentLaser, self).update(dt)
        if self._owner is None :
            return

        self.ts_check_fire -= dt
        if (self._owner.is_enemy or
            (not self._owner.is_enemy and
             (globals.controls[Controls.Action_0] or globals.controls[Controls.Action_1]))) and self.ts_check_fire <= 0:

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
            elif self.laser_type == LaserType.RailGun and (globals.controls[Controls.Action_1] or self._owner.is_enemy):
                projectile = self.get_rail_gun(self._owner.x + self._local_x,
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

    def init_rail_gun(self):
        self.mass = 300
        self.dmg = 100
        self.cd = 1
        self.speed = 2000
        self.angle = 90

    def get_rail_gun(self, x, y, direction):
        closest_enemy = None
        closest_dist = 123123123
        if not self._owner.is_enemy:
            for enemy in globals.enemies:
                dist = util.distance((self.x, self.y), (enemy.x, enemy.y))
                if dist < closest_dist:
                    closest_dist = dist
                    closest_enemy = enemy
        else:
            closest_enemy = globals.player_ship

        print("Closest Enemy for Railgun: {}/{}".format(closest_enemy.x, closest_enemy.y))

        #angle = math.degrees(math.atan2(closest_enemy.y - y, closest_enemy.x - x))
        angle = math.degrees(math.atan((closest_enemy.y - y) / (closest_enemy.x - x)))
        #angle = angle if angle >= 0 else angle + 360

        proj = ProjectileLaser(x, y, self.speed, angle, direction, self.dmg)
        proj.scale = 4.0
        return [proj]