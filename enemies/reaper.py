import enemies.enemy
import ship_components.ship_component_laser as smsp
from constants import Resources
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet


class Reaper(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Reaper, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Medium)

        self.base_health = 80

        self.upgrade(smsp.ShipComponentLaser(0, -2, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(0, 2, self, smsp.LaserType.SimpleLaser))

        self.upgrade(HeavyHull(0, -1, self))
        self.upgrade(HeavyHull(0, 1, self))
        self.upgrade(Jet(1, 0, self))
