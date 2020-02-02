import enemies.enemy
from constants import Resources
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_shield import Shield


class Freighter(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Freighter, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Large)

        self.base_health = 50
        self.upgrade(HeavyHull(0, -2, self))
        self.upgrade(HeavyHull(-1, -1, self))
        self.upgrade(HeavyHull(-2, 0, self))
        self.upgrade(HeavyHull(-1, 1, self))
        self.upgrade(HeavyHull(0, 2, self))

        self.upgrade(Shield(0, -1, self))
        self.upgrade(Shield(0, 1, self))

        self.upgrade(Jet(1, -1, self))
        self.upgrade(Jet(1, 1, self))
        self.upgrade(Jet(1, 0, self))
