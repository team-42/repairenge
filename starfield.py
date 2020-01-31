import pyglet

class StarField:

    def __init__(self, number_stars):
        self._number_stars = number_stars
        self._star_batch = pyglet.graphics.Batch()
        for i in range(number_stars):
            pass


    def update(self, dt):
        pass

    def draw(self):
        self._star_batch.draw()