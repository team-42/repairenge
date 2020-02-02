import enemies.enemy
import ship_components.ship_component_laser as smsp
from constants import Resources


class Behemoth(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Behemoth, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Large)

        self.base_health = 150

        # just add 1 simple phaser in front of the ship :)
        laser = smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.SimpleLaser)
        self.upgrade(laser)
