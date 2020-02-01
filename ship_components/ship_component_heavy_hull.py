from constants import Resources, BatchNames
from ship_components import ship_component
import globals


class HeavyHull(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super().__init__(x, y, owner,
                         globals.resources[Resources.Image_Ship_Module_Base],
                         batch=globals.sprite_batches[BatchNames.Component_Batch], *args, **kwargs)

    def module_initial(self, ship):
        ship.mass += 200
        ship.base_health += 50
        ship.health_multiplier += 0.2

    def update(self, dt):
        super(HeavyHull, self).update(dt)
        if self._owner is None:
            return
