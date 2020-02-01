import pyglet

from projectiles.projectile_laser import ProjectileLaser
from ship_components import ship_component


class ShipComponentSimplePhaser(ship_component.ShipComponent):
    def __init__(self, x, y, *args, **kwargs):
        ship_image = pyglet.resource.image("resources/ship/base.png")

        super(ShipComponentSimplePhaser, self).__init__(10, x, y, ship_image, *args, *kwargs)
        self.cd = 1
        self.ts_check_fire = self.cd

    def module_initial(self, ship):
        ship.mass += self.mass

    def module_action(self, dt, game_objects):
        self.ts_check_fire -= dt
        if self.ts_check_fire <= 0:
            self.ts_check_fire = self.cd
            game_objects["projectile_list"].append(ProjectileLaser(self.x, self.y))
