import globals
from constants import Resources, BatchNames
from ship_components import ship_component


class Shield(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super().__init__(x, y, owner,
                         globals.resources[Resources.Image_Ship_Module_Shield],
                         batch=globals.sprite_batches[BatchNames.Component_Batch], *args, **kwargs)

    def module_initial(self, ship):
        super(Shield, self).module_initial(ship)
        ship.base_shield += 10
