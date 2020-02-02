import enemies.enemy
import ship_components.ship_component_laser as smsp
from constants import Resources
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet


class Sniper(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Sniper, self).__init__(x, y, Resources.Image_Ship_Module_Railgun)

        self.base_health = 50

        self.upgrade(smsp.ShipComponentLaser(0, -2, self, smsp.LaserType.RailGun))
        self.upgrade(HeavyHull(0, 1, self))
        self.upgrade(Jet(1, 0, self))