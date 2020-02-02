import math
import random
import globals
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

    def update(self, dt):
        self._healthbar.update()
        self._shieldbar.update()
        self.time += dt
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        if self.x > globals.window.width * 0.75:
            self.x -= 0.5 * self.engine_power / self.mass * dt

        super(StoryEnemy, self).update(dt)
