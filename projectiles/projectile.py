import pyglet


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, x, y, speed, dmg, img, *args, **kwargs):
        super(Projectile, self).__init__(img, x, y, *args, **kwargs)
        self.speed = speed
        self.damage = dmg
        self.alive = True

    def update(self, dt, game_objects):
        self.x = self.x + self.speed * dt
        if self.x > 1050:
            self.alive = False
