import enemies.enemy
import ship_components.ship_component_laser as smsp
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from constants import Resources


class Behemoth(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Behemoth, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Large)

        self.base_health = 150

        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.HeavyLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.HeavyLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.HeavyLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, -2, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, 2, self, smsp.LaserType.AngleLaser))

        self.upgrade(HeavyHull(-1, -2, self))
        self.upgrade(HeavyHull(0, -2, self))
        self.upgrade(HeavyHull(-2, -1, self))
        self.upgrade(HeavyHull(-2, 1, self))
        self.upgrade(HeavyHull(-1, 2, self))
        self.upgrade(HeavyHull(0, 2, self))

        self.upgrade(Jet(0, -1, self))
        self.upgrade(Jet(0, 1, self))
