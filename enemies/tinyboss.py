import random

import ship_components.ship_component_laser as smsp
from constants import Resources
from enemies.enemy import StoryEnemy


class TinyBoss(StoryEnemy):
    def __init__(self, x, y):
        super(TinyBoss, self).__init__(True, Resources.Image_Ship_Module_Enemy)
        self.x = x
        self.y = y
        self.engine_power = self.engine_power / 2.0
        self.time = random.random() * 2.0 * 3.1415
        self.base_health = 100

        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(1, 0, self, smsp.LaserType.SimpleLaser))
