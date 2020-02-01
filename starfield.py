import pyglet
import random


class Star(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Star, self).__init__(*args, **kwargs)

        # In addition to position, we have velocity
        self.velocity_x = random.random() * 100
        self.scale = self.velocity_x * 0.02

    def update(self, dt):
        self.x = self.x - dt * self.velocity_x
        if self.x < -50:
            self.x = 1000
            self.velocity_x = random.random() * 100
            self.scale = self.velocity_x * 0.02


class StarField:

    def __init__(self, number_stars):
        self._number_stars = number_stars
        self._star_batch = pyglet.graphics.Batch()
        star_image = pyglet.resource.image("resources/environment/star.png")
        self._stars_dx = random.random() * 10
        self._stars = []
        for i in range(number_stars):
            self._stars.append(Star(star_image, random.random() * 1000, random.random() * 800,
                                    batch=self._star_batch))

    def update(self, dt):
        for star in self._stars:
            star.update(dt)

    def draw(self):
        self._star_batch.draw()
