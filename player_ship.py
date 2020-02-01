import ship
import globals
import ship_components.ship_component_simple_phaser as smsp
from constants import Controls


class PlayerShip(ship.Ship):
    def __init__(self):
        super(PlayerShip, self).__init__()

        # just add 5 simple phaser in front of the ship :)
        self.modules.append(smsp.ShipComponentSimplePhaser(16, 0))

        self.modules.append(smsp.ShipComponentSimplePhaser(12, -8))
        self.modules.append(smsp.ShipComponentSimplePhaser(8, -16))
        self.modules.append(smsp.ShipComponentSimplePhaser(4, -24))

        self.modules.append(smsp.ShipComponentSimplePhaser(12, 8))
        self.modules.append(smsp.ShipComponentSimplePhaser(8, 16))
        self.modules.append(smsp.ShipComponentSimplePhaser(4, 24))

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        # first superclass.update
        super(PlayerShip, self).update(dt)

        # controls:
        if globals.controls[Controls.Up]:
            self.y += self.engine_power / self.mass * dt
        if globals.controls[Controls.Down]:
            self.y -= self.engine_power / self.mass * dt
        if globals.controls[Controls.Left]:
            self.x -= self.engine_power / self.mass * dt
        if globals.controls[Controls.Right]:
            self.x += self.engine_power / self.mass * dt
