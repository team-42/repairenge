import globals
import ship
import ship_components.ship_component_laser as smsp
from constants import Controls, Resources
from healthbar import Healthbar
from shieldbar import Shieldbar


class PlayerShip(ship.Ship):
    def __init__(self):
        super(PlayerShip, self).__init__(False, Resources.Image_Ship_Module_Base)

        self.upgrade(smsp.ShipComponentLaser(1, 0, self, smsp.LaserType.AngleLaser))
        self._healthbar = Healthbar(self)
        self._shieldbar = Shieldbar(self)
        # self.upgrade(smsp.ShipComponentLaser(0, -2, self, smsp.LaserType.HeavyLaser))
        # self.upgrade(smsp.ShipComponentLaser(0, 2, self, smsp.LaserType.HeavyLaser))
        # self.upgrade(smsp.ShipComponentLaser(1, -1, self, smsp.LaserType.SimpleLaser))
        # self.upgrade(smsp.ShipComponentLaser(1, 1, self, smsp.LaserType.SimpleLaser))
        # self.upgrade(HeavyHull(0, 1, self))
        # self.upgrade(HeavyHull(0, -1, self))
        # self.upgrade(HeavyHull(-1, 2, self))
        # self.upgrade(HeavyHull(-1, -2, self))
        # self.upgrade(RepairCrane(-1, 1, self))
        # self.upgrade(RepairCrane(-1, -1, self))
        # self.upgrade(Jet(-2, -1, self))
        # self.upgrade(Jet(-2, 0, self))
        # self.upgrade(Jet(-2, 1, self))

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        self._healthbar.update()
        self._shieldbar.update()
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
