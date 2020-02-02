import enemies.enemy
import ship_components.ship_component_laser as smsp
from ship_components.ship_component_repair_crane import RepairCrane
from constants import Resources


class Frigate(enemies.enemy.Enemy):
    def __init__(self, x, y):
        super(Frigate, self).__init__(x, y, Resources.Image_Ship_Module_Enemy_Medium)

        self.base_health = 40

        self.upgrade(smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(0, 1, self, smsp.LaserType.AngleLaser))

        self.upgrade(RepairCrane(0, -1, self))
