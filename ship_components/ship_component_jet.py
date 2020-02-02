import globals
from constants import Resources, BatchNames
from ship_components import ship_component


class Jet(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super(Jet, self).__init__(x, y, owner,
                                  globals.resources[Resources.Image_Ship_Module_Jet],
                                  batch=globals.sprite_batches[BatchNames.Component_Batch],
                                  *args, *kwargs)

        self.engine_power = 100000
        self.mass = 50

    def module_initial(self, ship):
        super(Jet, self).module_initial(ship)
        ship.mass += self.mass
        ship.engine_power += self.engine_power

    def update(self, dt):
        super(Jet, self).update(dt)
