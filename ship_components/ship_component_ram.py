import globals
from constants import Resources, BatchNames
from ship_components import ship_component


class Ram(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super().__init__(x, y, owner,
                         globals.resources[Resources.Image_Ship_Module_Ram],
                         batch=globals.sprite_batches[BatchNames.Component_Batch], *args, **kwargs)

    def module_initial(self, ship):
        super(Ram, self).module_initial(ship)
        self.mass = 50
