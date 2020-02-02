import enemies.enemy
from constants import Resources
from ship import Ship
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_ram import Ram


class Hammerhead(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Hammerhead, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Large)

        self.base_health = 50
        self.upgrade(Ram(-0, -2, self))
        self.upgrade(Ram(-1, -1, self))
        self.upgrade(Ram(-2, 0, self))
        self.upgrade(Ram(-1, 1, self))
        self.upgrade(Ram(-0, 2, self))

        self.upgrade(HeavyHull(-1, -1, self))
        self.upgrade(HeavyHull(0, -1, self))
        self.upgrade(HeavyHull(-1, 1, self))
        self.upgrade(HeavyHull(0, 1, self))

        self.upgrade(Jet(3, -2, self))
        self.upgrade(Jet(2, -2, self))
        self.upgrade(Jet(2, -1, self))
        self.upgrade(Jet(1, -2, self))
        self.upgrade(Jet(1, -1, self))
        self.upgrade(Jet(1, 0, self))
        self.upgrade(Jet(1, 1, self))
        self.upgrade(Jet(1, 2, self))
        self.upgrade(Jet(2, 1, self))
        self.upgrade(Jet(2, 2, self))
        self.upgrade(Jet(3, 2, self))

    def update(self, dt):
        self.time += dt
        # fly to the left
        self.x -= 0.5 * self.engine_power / self.mass * dt

        Ship.update(self, dt)

        # kill the drone if its out of screen
        if self.x < -50:
            self.alive = False
