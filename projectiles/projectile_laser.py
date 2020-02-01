import pyglet
from projectiles.projectile import Projectile


class ProjectileLaser(Projectile):
    def __init__(self, x, y, *args, **kwargs):
        self._laser_image = pyglet.resource.image("resources/projectiles/energy_01.png")

        super(ProjectileLaser, self).__init__(x, y, 800, 10, self._laser_image, *args, *kwargs)
        self.color = (255, 122, 65)
        self.scale = 1

    def update(self, dt, game_objects):
        super(ProjectileLaser, self).update(dt, game_objects)
