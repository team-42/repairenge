import pyglet
import globals
from constants import Resources
from constants import BatchNames


class Ship(pyglet.sprite.Sprite):
    def __init__(self, is_enemy, *args, **kwargs):
        super(Ship, self).__init__(globals.resources[Resources.Image_Ship_Module_Base],
                                   batch=globals.sprite_batches[BatchNames.Player_Ship_Batch], *args, **kwargs)
        self.x = 100.0
        self.y = 100.0

        # set this to true if this is an enemy ship
        self.is_enemy = is_enemy
        self.alive = True

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

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        for mod in self.modules:
            mod.module_action(dt)

    def upgrade(self, sm):
        sm.module_initial()
        self.modules.append(sm)


    def get_health(self):
        return (self.base_health * self.health_multiplier) - self.damage_taken

    def damage(self, dmg):
        self.damage_taken += dmg
