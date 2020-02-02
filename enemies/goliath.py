import math

import globals
import ship_components.ship_component_laser as smsp
from constants import Resources
from enemies.enemy import StoryEnemy
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_ram import Ram
from ship_components.ship_component_repair_crane import RepairCrane


class Goliath(StoryEnemy):
    def __init__(self, x, y):
        super(Goliath, self).__init__(True, Resources.Image_Ship_Module_Enemy_Boss)
        self.x = x
        self.y = globals.window.height / 2 - 32 * 5 - 16
        self.engine_power = self.engine_power / 2
        self.time = 0
        self.base_health = 300

        self.upgrade(RepairCrane(1, -5, self))
        self.upgrade(RepairCrane(1, -2, self))
        self.upgrade(RepairCrane(1, 0, self))
        self.upgrade(RepairCrane(1, 2, self))
        self.upgrade(RepairCrane(1, 5, self))

        for y in range(-5, 6):
            if y % 2 == 0:
                self.upgrade(smsp.ShipComponentLaser(-1, y, self, smsp.LaserType.HeavyLaser))
                self.upgrade(HeavyHull(2, y, self))
            else:
                self.upgrade(HeavyHull(-1, y, self))
                self.upgrade(smsp.ShipComponentLaser(2, y, self, smsp.LaserType.HeavyLaser))

            self.upgrade(HeavyHull(0, y, self))
            self.upgrade(HeavyHull(1, y, self))

        for y in range(-4, 5):
            self.upgrade(smsp.ShipComponentLaser(-2, y, self, smsp.LaserType.SimpleLaser))
            self.upgrade(smsp.ShipComponentLaser(3, y, self, smsp.LaserType.SimpleLaser))

        for y in range(-3, 4):
            self.upgrade(Ram(-3, y, self))
            self.upgrade(Jet(4, y, self))

    def update(self, dt):
        self._healthbar.update()
        self._shieldbar.update()
        self.time += dt / (1_550_000 / self.engine_power)
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        if self.x > globals.window.width * 0.85:
            self.x -= 0.5 * self.engine_power / self.mass * dt

        super(StoryEnemy, self).update(dt)
