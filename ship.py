import pyglet
import ship_components.ship_component_simple_phaser as smsp
from constants import Controls
from constants import GameObjects


class Ship(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        image = pyglet.resource.image("resources/ship/base.png")

        super(Ship, self).__init__(image, *args, **kwargs)
        self.x = 100.0
        self.y = 100.0

        # Health Segment
        self.base_health = 100
        self.health_multiplier = 1.0
        self.damage_taken = 0
        self.current_health = self.base_health * self.health_multiplier

        # ship movement properties
        self.engine_power = 500.0
        self.mass = 1.0

        # modules
        self.modules = list()
        # just add 5 simple phaser in front of the ship :)
        self.modules.append(smsp.ShipComponentSimplePhaser(16, 0))

        self.modules.append(smsp.ShipComponentSimplePhaser(12, -8))
        self.modules.append(smsp.ShipComponentSimplePhaser(8, -16))
        self.modules.append(smsp.ShipComponentSimplePhaser(4, -24))

        self.modules.append(smsp.ShipComponentSimplePhaser(12, 8))
        self.modules.append(smsp.ShipComponentSimplePhaser(8, 16))
        self.modules.append(smsp.ShipComponentSimplePhaser(4, 24))

    def update(self, dt, game_objects):
        """
        :param dt:
        :return:
        """
        # controls:
        if game_objects[GameObjects.Controls][Controls.Up]:
            self.y += self.engine_power / self.mass * dt
        if game_objects[GameObjects.Controls][Controls.Down]:
            self.y -= self.engine_power / self.mass * dt
        if game_objects[GameObjects.Controls][Controls.Left]:
            self.x -= self.engine_power / self.mass * dt
        if game_objects[GameObjects.Controls][Controls.Right]:
            self.x += self.engine_power / self.mass * dt

        for mod in self.modules:
            mod.module_action(dt, game_objects)


def upgrade(self, sm):
    sm.module_initial()


def get_health(self):
    return (self.base_health * self.health_multiplier) - self.damage_taken


def damage(self, dmg):
    self.damage_taken += dmg
