import ship
import globals
import ship_components.ship_component_laser as smsp
import ship_components.ship_component_jet as scj
from constants import Controls


class PlayerShip(ship.Ship):
    def __init__(self):
        super(PlayerShip, self).__init__(False)

        # just add 7 simple phaser in front of the ship :)
        self.upgrade(smsp.ShipComponentLaser(1, 0, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(1, -1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(1, 1, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(1, -2, self, smsp.LaserType.SimpleLaser))
        self.upgrade(smsp.ShipComponentLaser(1, 2, self, smsp.LaserType.SimpleLaser))

        self.upgrade(scj.Jet(2, 2, self))
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

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > globals.window.width:
            self.x = globals.window.width
        if self.y > globals.window.height:
            self.y = globals.window.height

        # first superclass.update
        super(PlayerShip, self).update(dt)
