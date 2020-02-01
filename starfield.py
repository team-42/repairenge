import pyglet
import random
from constants import Resources
from constants import BatchNames
import globals


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
        self._stars_dx = random.random() * 10
        self._stars = []
        for i in range(number_stars):
            self._stars.append(
                Star(globals.resources[Resources.Image_Starfield], random.random() * 1000, random.random() * 800,
                     batch=globals.sprite_batches[BatchNames.Star_Batch]))

    def update(self, dt):
        for star in self._stars:
            star.update(dt)
