import math

from projectiles.projectile import Projectile
import globals
from constants import Resources
from constants import BatchNames
from constants import LaserColors


class ProjectileLaser(Projectile):
    def __init__(self, x, y, speed, angle, direction, dmg, *args, **kwargs):
        super(ProjectileLaser, self).__init__(x, y, speed, dmg,
                                              globals.resources[Resources.Image_Projectiles_Energy_01],
                                              batch=globals.sprite_batches[BatchNames.Projectile_Batch],
                                              *args, *kwargs)
        if direction == -1:
            self.color = LaserColors.Player_Ship.value
        else:
            self.color = LaserColors.Enemy_Ship.value
        self.scale = 1
        self.angle = angle

    def update(self, dt):
        rad = self.angle * math.pi / 180
        self.x += self.speed * math.sin(rad) * dt
        self.y += self.speed * math.cos(rad) * dt

        # check if this is outside the screen
        if self.x > 1050 or self.x < -50 or self.y < -50 or self.y > 850:
            self.alive = False
