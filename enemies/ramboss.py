import math
import random

import globals
from constants import Resources
from enemies.enemy import StoryEnemy
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_ram import Ram
from ship_components.ship_component_shield import Shield

RAM_IDLE = 0
RAM_FORWARD = 1
RAM_RETURN = 2
RAMMING_SPEED = 4
RAM_PROBABILITY = 0.01


class RamBoss(StoryEnemy):
    ram_attack = RAM_IDLE

    def __init__(self, x, y):
        super(RamBoss, self).__init__(True, Resources.Image_Ship_Module_Enemy_Large)
        self.x = x
        self.y = 112
        self.engine_power = self.engine_power / 1.5
        self.time = 0
        self.base_health = 200
        self.drop_rate = 0.2

        self.upgrade(Ram(1, -3, self))
        self.upgrade(Ram(-0, -2, self))
        self.upgrade(Ram(-1, -1, self))
        self.upgrade(Ram(-2, 0, self))
        self.upgrade(Ram(-1, 1, self))
        self.upgrade(Ram(-0, 2, self))
        self.upgrade(Ram(1, 3, self))

        self.upgrade(HeavyHull(-1, -1, self))
        self.upgrade(HeavyHull(-1, 1, self))
        self.upgrade(HeavyHull(1, -2, self))
        self.upgrade(HeavyHull(1, 2, self))
        self.upgrade(Shield(0, -1, self))
        self.upgrade(Shield(0, 1, self))

        self.upgrade(Jet(3, -2, self))
        self.upgrade(Jet(2, -2, self))
        self.upgrade(Jet(2, -1, self))
        self.upgrade(Jet(1, -1, self))
        self.upgrade(Jet(1, 0, self))
        self.upgrade(Jet(1, 1, self))
        self.upgrade(Jet(2, 1, self))
        self.upgrade(Jet(2, 2, self))
        self.upgrade(Jet(3, 2, self))

    def update(self, dt):
        if self.ram_attack == RAM_FORWARD:
            # fly to the left
            self.x -= 0.5 * self.engine_power / self.mass * dt
            if self.x <= 50:
                self.ram_attack = RAM_RETURN
        elif self.ram_attack == RAM_RETURN:
            # fly to the right
            self.x += 0.5 * self.engine_power / self.mass * dt
            if self.x > globals.window.width * 0.85:
                self.ram_attack = RAM_IDLE
                self.engine_power /= RAMMING_SPEED
        elif self.time > 5 and random.random() < RAM_PROBABILITY + (
                RAM_PROBABILITY - RAM_PROBABILITY * self.get_health_percentage() / 100):
            self.ram_attack = RAM_FORWARD
            self.engine_power *= RAMMING_SPEED
        else:
            self.time += dt
            # fly up and down
            self.y += math.sin(self.time) * self.engine_power * dt / (self.mass * 2.4)
            # fly to the left
            if self.x > globals.window.width * 0.85:
                self.x -= 0.5 * self.engine_power / self.mass * dt

        self._healthbar.update()
        self._shieldbar.update()
        super(StoryEnemy, self).update(dt)
