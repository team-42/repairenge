from ship_modules import ShipModule


class ShipModuleSimplePhaser(ShipModule.ShipModule):
    def __init__(self, x, y):
        super(ShipModuleSimplePhaser, self).__init__(10, x, y)
        self.cd = 1
        self.ts_check_fire = self.cd

    def module_initial(self, ship):
        ship.mass += self.mass

    def module_action(self, dt):
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            pass  # fire
