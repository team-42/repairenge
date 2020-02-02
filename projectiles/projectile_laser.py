import math

from projectiles.projectile import Projectile
import globals
from constants import Resources
from constants import BatchNames
from constants import LaserColors


class ProjectileLaser(Projectile):
    def __init__(self, x, y, speed, dir_vec, is_from_player, dmg, *args, **kwargs):
        super(ProjectileLaser, self).__init__(x, y, speed, dmg,
                                              globals.resources[Resources.Image_Projectiles_Energy_01],
                                              batch=globals.sprite_batches[BatchNames.Projectile_Batch],
                                              *args, *kwargs)
        self.dir_vec = dir_vec.copy()
        if is_from_player:
            self.color = LaserColors.Player_Ship.value
        else:
            self.color = LaserColors.Enemy_Ship.value
            self.dir_vec[0] = -1 * self.dir_vec[0]

        self.scale = 1
        self.is_from_player = is_from_player

    def update(self, dt):
        self.x += self.speed * self.dir_vec[0] * dt
        self.y += self.speed * self.dir_vec[1] * dt

        # check if this is outside the screen
        if self.x > globals.window.width + 50 or self.x < -50 or self.y < -50 or self.y > globals.window.height + 50:
            self.alive = False
