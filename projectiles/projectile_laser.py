import pyglet
from projectiles.projectile import Projectile


class ProjectileLaser(Projectile):
    def __init__(self, x, y, *args, **kwargs):
        laser_image = pyglet.resource.image("resources/ship/base.png")

        super(ProjectileLaser, self).__init__(x, y, 200, 10, laser_image, *args, *kwargs)
