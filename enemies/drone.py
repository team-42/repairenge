import ship
import ship_components.ship_component_simple_phaser as smsp
import math
import random


class Drone(ship.Ship):
    def __init__(self, x, y):
        super(Drone, self).__init__(True)

        self.x = x
        self.y = y
        self.engine_power = self.engine_power / 2.0
        self.time = random.random() * 2.0 * 3.1415
        self.base_health = 30

        # just add 1 simple phaser in front of the ship :)
        phaser = smsp.ShipComponentSimplePhaser(-16, 0, self)
        self.modules.append(phaser)

    def update(self, dt):
        super(Drone, self).update(dt)

        self.time += dt
        # fly up and down
        self.y += math.sin(self.time) * self.engine_power / self.mass * dt
        # fly to the left
        self.x -= 0.5 * self.engine_power / self.mass * dt

        # kill the drone if its out of screen
        if self.x < -50:
            self.alive = False
