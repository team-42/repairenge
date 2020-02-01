from projectiles.projectile import Projectile
import globals
from constants import Resources
from constants import BatchNames


class ProjectileLaser(Projectile):
    def __init__(self, x, y, direction, *args, **kwargs):
        super(ProjectileLaser, self).__init__(x, y, direction * 800, 10,
                                              globals.resources[Resources.Image_Projectiles_Energy_01],
                                              batch=globals.sprite_batches[BatchNames.Projectile_Batch],
                                              *args, *kwargs)
        if direction == -1:
            self.color = (255, 122, 65)
        else:
            self.color = (80, 80, 255)
        self.scale = 1

    def update(self, dt):
        super(ProjectileLaser, self).update(dt)
