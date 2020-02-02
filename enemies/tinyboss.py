import math
import random

from enemies.enemy import StoryEnemy
import globals
import ship_components.ship_component_laser as smsp
from constants import Resources
from healthbar import Healthbar
from ship_components.ship_component_heavy_hull import HeavyHull
from ship_components.ship_component_jet import Jet
from ship_components.ship_component_repair_crane import RepairCrane


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
