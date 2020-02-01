import ship
import globals
import ship_components.ship_component_laser as smsp
from constants import Controls


class PlayerShip(ship.Ship):
    def __init__(self):
        super(PlayerShip, self).__init__(False)

        # just add 7 simple phaser in front of the ship :)
        self.upgrade(smsp.ShipComponentLaser(24, 8, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(20, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(20, 16, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(16, -8, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(16, 24, self, smsp.LaserType.SimpleLaser))
        #
        # self.upgrade(smsp.ShipComponentLaser(12, 8, self, smsp.LaserType.SimpleLaser))
        # self.upgrade(smsp.ShipComponentLaser(8, 16, self, smsp.LaserType.SimpleLaser))
        # #self.upgrade(smsp.ShipComponentLaser(4, 24, self, smsp.LaserType.SimpleLaser))
        #
        # self.upgrade(smsp.ShipComponentLaser(4, 24, self, smsp.LaserType.AngleLaser))

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        # controls:
        if globals.controls[Controls.Up]:
            self.y += self.engine_power / self.mass * dt
        if globals.controls[Controls.Down]:
            self.y -= self.engine_power / self.mass * dt
        if globals.controls[Controls.Left]:
            self.x -= self.engine_power / self.mass * dt
        if globals.controls[Controls.Right]:
            self.x += self.engine_power / self.mass * dt

        # first superclass.update
        super(PlayerShip, self).update(dt)