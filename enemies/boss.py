import math

import globals
import ship_components.ship_component_laser as smsp
from constants import Resources
from enemies.enemy import StoryEnemy
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_repair_crane import RepairCrane
from ship_components.ship_component_shield import Shield


class Boss(StoryEnemy):
    def __init__(self, x, y):
        super(Boss, self).__init__(True, Resources.Image_Ship_Module_Enemy_Boss)
        self.x = x
        self.y = 3 * 32 + 16
        self.engine_power = self.engine_power / 8.0
        self.time = 0
        self.base_health = 300

        self.upgrade(smsp.ShipComponentLaser(-2, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, -1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-3, 0, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, -2, self, smsp.LaserType.HeavyLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 2, self, smsp.LaserType.HeavyLaser))
        self.upgrade(smsp.ShipComponentLaser(1, 0, self, smsp.LaserType.RailGun))

        self.upgrade(HeavyHull(0, -2, self))
        self.upgrade(HeavyHull(1, -2, self))
        self.upgrade(HeavyHull(0, 2, self))
        self.upgrade(HeavyHull(1, 2, self))
        self.upgrade(Shield(-2, 0, self))

        self.upgrade(RepairCrane(0, -1, self))
        self.upgrade(RepairCrane(0, 1, self))

        self.upgrade(Jet(1, -1, self))
        self.upgrade(Jet(2, 0, self))
        self.upgrade(Jet(1, 1, self))

    def update(self, dt):
        self._healthbar.update()
        self._shieldbar.update()
        self.time += dt / (290 * self.mass / self.engine_power)
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        if self.x > globals.window.width * 0.85:
            self.x -= 0.5 * self.engine_power / self.mass * dt

        super(StoryEnemy, self).update(dt)
