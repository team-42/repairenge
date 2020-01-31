import ShipModule


class ShipModuleSimplePhaser(ShipModule.ShipModule):
    def __init__(self):
        super(ShipModule, self).__init__(10, 0, 0)
        self.cd = 1
        self.ts_check_fire = self.cd

    def module_initial(self, ship):
        ship.mass += self.mass

    def module_action(self, dt):
        pass
