import math
import random

import ship
import ship_components.ship_component_laser as smsp
from constants import Resources


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
