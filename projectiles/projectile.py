import pyglet


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, x, y, speed, dmg, *args, **kwargs):
        super(Projectile, self).__init__(x, y, *args, **kwargs)
        self.speed = speed
        self.damage = dmg

    def update(self, dt):
        self.x = self.x + self.speed * dt
