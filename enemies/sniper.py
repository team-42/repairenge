import enemies.enemy
import ship_components.ship_component_laser as smsp
from constants import Resources
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet


class Sniper(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Sniper, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_RailGun)

        self.base_health = 30

        self.upgrade(smsp.ShipComponentLaser(1, 0, self, smsp.LaserType.RailGun))
        self.upgrade(HeavyHull(1, 1, self))
        self.upgrade(HeavyHull(1, -1, self))
        self.upgrade(Jet(2, 0, self))
