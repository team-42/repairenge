import math
import random

import globals
import ship
from healthbar import Healthbar
from shieldbar import Shieldbar


class Enemy(ship.Ship):
    def __init__(self, x, y, resource):
        super(Enemy, self).__init__(True, resource)

        self.x = x
        self.y = y
        self.engine_power = self.engine_power / 2.0
        self.time = random.random() * 2.0 * 3.1415

    def update(self, dt):
        self.time += dt
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        self.x -= 0.5 * self.engine_power / self.mass * dt

        super(Enemy, self).update(dt)

        # kill the drone if its out of screen
        if self.x < -50:
            self.alive = False


class StoryEnemy(ship.Ship):
    def __init__(self, is_enemy, resource, *args, **kwargs):
        super().__init__(is_enemy, resource, *args, **kwargs)
        self._healthbar = Healthbar(self)
        self._shieldbar = Shieldbar(self)

    def update(self, dt):
        self._healthbar.update()
        self._shieldbar.update()
        self.time += dt
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        if self.x > globals.window.width * 0.75:
            self.x -= 0.5 * self.engine_power / self.mass * dt

        super(StoryEnemy, self).update(dt)

        # kill the drone if its out of screen
        if self.x < -50:
            self.alive = False
