import math
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
        elif laser_type == LaserType.RailGun:
            image = globals.resources[Resources.Image_Ship_Module_Railgun]
        else:
            image = globals.resources[Resources.Image_Ship_Module_Simple_Phaser]
        super(ShipComponentLaser, self).__init__(x, y, owner, image,
                                                 batch=globals.sprite_batches[BatchNames.Component_Batch],
                                                 *args, *kwargs)
        self.cd = 1
        self.laser_type = laser_type
        self.speed = 800
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
        if self._owner is None:
            return

        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            # check: is this laser from the player or an enemy?
            is_player = False if self._owner.is_enemy else True
            if not is_player:  # enemy
                projectile = self.get_std_projectile(is_player)
                if not projectile and self.laser_type == LaserType.RailGun:
                    projectile = self.get_rail_gun(self._owner.x + self._local_x, self._owner.y + self._local_y,
                                                   is_player)

                self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()
                for proj in projectile:
                    globals.enemy_projectiles.append(proj)
            else:  # player
                if globals.controls[Controls.Action_0]:
                    projectile = self.get_std_projectile(is_player)
                    self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()
                    for proj in projectile:
                        globals.player_projectiles.append(proj)
                elif globals.controls[Controls.Action_1] and LaserType.RailGun == self.laser_type:
                    projectile = self.get_rail_gun(self._owner.x + self._local_x, self._owner.y + self._local_y,
                                                   is_player)
                    self.ts_check_fire = self.cd - 0.01 + 0.02 * random.random()
                    for proj in projectile:
                        globals.player_projectiles.append(proj)

    def get_std_projectile(self, is_player):
        projectile = []
        if self.laser_type == LaserType.SimpleLaser:
            projectile = self.get_simple_laser_projectile(self._owner.x + self._local_x, self._owner.y + self._local_y,
                                                          is_player)
        elif self.laser_type == LaserType.AngleLaser:
            projectile = self.get_angle_laser(self._owner.x + self._local_x, self._owner.y + self._local_y, is_player)
        elif self.laser_type == LaserType.HeavyLaser:
            projectile = self.get_heavy_laser(self._owner.x + self._local_x, self._owner.y + self._local_y, is_player)

        return projectile

    def init_simple_laser(self):
        self.mass = 10
        self.dmg = 10
        self.cd = 1
        self.speed = 800
        self.dir_vec = [1, 0]

    def get_simple_laser_projectile(self, x, y, is_player):
        projectile = ProjectileLaser(x, y, self.speed, self.dir_vec, is_player, self.dmg)
        array = []
        array.append(projectile)
        return array

    def init_angle_laser(self):
        self.mass = 15
        self.dmg = 10
        self.cd = 1
        self.speed = 800
        # since two projectiles are created the diff between 90 and angle is taken and added to 90 for the other one
        self.dir_vec = [1.0, 0.5]
        length = util.get_vector_length(self.dir_vec)
        self.dir_vec = [self.dir_vec[0] / length, self.dir_vec[1] / length]

    def get_angle_laser(self, x, y, is_player):
        return [ProjectileLaser(x, y, self.speed, self.dir_vec, is_player, self.dmg),
                ProjectileLaser(x, y, self.speed, [self.dir_vec[0], -self.dir_vec[1]], is_player, self.dmg)]

    def init_heavy_laser(self):
        self.mass = 50
        self.dmg = 30
        self.cd = 2
        self.speed = 1000
        self.dir_vec = [1, 0]

    def get_heavy_laser(self, x, y, is_player):
        proj = ProjectileLaser(x, y, self.speed, self.dir_vec, is_player, self.dmg)
        proj.scale = 2.0
        return [proj]

    def init_rail_gun(self):
        self.mass = 300
        self.dmg = 80
        self.cd = 3
        self.speed = 1800
        self.dir_vec = [1, 0]

    def get_rail_gun(self, x, y, is_player):
        closest_enemy = None
        closest_dist = 123123123
        if is_player:
            for enemy in globals.enemies:
                dist = util.distance((self.x, self.y), (enemy.x, enemy.y))
                if dist < closest_dist:
                    closest_dist = dist
                    closest_enemy = enemy
        else:
            closest_enemy = globals.player_ship

        if closest_enemy is None:
            return []

        target_vec = [0, 0]
        target_vec[0] = closest_enemy.x - self.x
        target_vec[1] = closest_enemy.y - self.y
        length = util.get_vector_length(target_vec)
        target_vec[0] /= length
        target_vec[1] /= length

        # black magic
        if not is_player:
            target_vec[0] = -1 * target_vec[0]

        proj = ProjectileLaser(x, y, self.speed, target_vec, is_player, self.dmg)
        proj.scale = 4.0
        return [proj]
