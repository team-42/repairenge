import ship
import ship_components.ship_component_laser as smsp
import math
import random
import globals


class Boss(ship.Ship):
    def __init__(self, x, y):
        super(Boss, self).__init__(True)

        self.x = x
        self.y = y
        self.engine_power = self.engine_power / 2.0
        self.time = random.random() * 2.0 * 3.1415
        self.base_health = 100

        # just add 1 simple phaser in front of the ship :)
        self.upgrade(smsp.ShipComponentLaser(-2, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(-2, -1, self, smsp.LaserType.SimpleLaser))

        self.upgrade(smsp.ShipComponentLaser(-1, -2, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, -1, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-3, 0, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 1, self, smsp.LaserType.AngleLaser))
        self.upgrade(smsp.ShipComponentLaser(-1, 2, self, smsp.LaserType.AngleLaser))

    def update(self, dt):
        self.time += dt
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        if self.x > globals.window.width * 0.75:
            self.x -= 0.5 * self.engine_power / self.mass * dt

        super(Boss, self).update(dt)

        # kill the drone if its out of screen
        if self.x < -50:
            self.alive = False
