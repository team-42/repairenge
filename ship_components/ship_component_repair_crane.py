from constants import Resources, BatchNames
from ship_components import ship_component
import globals


class RepairCrane(ship_component.ShipComponent):
    def __init__(self, x, y, owner, *args, **kwargs):
        super(RepairCrane, self).__init__(x, y, owner,
                                          globals.resources[Resources.Image_Ship_Module_Repair],
                                          batch=globals.sprite_batches[BatchNames.Component_Batch],
                                          *args, *kwargs)
        self.heal = 10
        self.cd = 1
        self.mass = 100
        self.ts_check_heal = 1

    def module_initial(self, ship):
        ship.mass += self.mass
        self.ts_check_heal = self.cd

    def update(self, dt):
        super(RepairCrane, self).update(dt)
        if self._owner is None:
            return

        self.ts_check_heal -= dt
        if self.ts_check_heal <= 0 and self._owner.damage_taken > 0:
            self.ts_check_heal = self.cd
            actual_heal = min(self._owner.damage_taken, self.heal)
            self._owner.damage(-actual_heal)
            print("heal to {}".format(self._owner.get_health()))

