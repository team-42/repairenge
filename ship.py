import pyglet
import globals
from constants import Resources
from constants import BatchNames
import random


class Ship(pyglet.sprite.Sprite):
    def __init__(self, is_enemy, resource, *args, **kwargs):
        if is_enemy:
            batch = globals.sprite_batches[BatchNames.Enemy_Batch]
        else:
            batch = globals.sprite_batches[BatchNames.Player_Ship_Batch]
        base_resource = resource

        super(Ship, self).__init__(globals.resources[base_resource],
                                   batch=batch, *args, **kwargs)

        self.x = globals.window.width * 0.2
        self.y = globals.window.height * 0.5

        # set this to true if this is an enemy ship
        self.is_enemy = is_enemy
        self.alive = True

        # component grid:
        # uses 2-tuples as indices
        # value == 1 -> reserved for base model
        self.grid = {
            (0, 0): 1,
            (-1, 0): 1
        }

        # Health Segment
        self.base_health = 200
        self.health_multiplier = 1.0
        self.damage_taken = 0
        self.current_health = self.base_health * self.health_multiplier

        # ship movement properties
        self.engine_power = 500000.0
        self.mass = 1000.0

        # modules
        self.modules = list()

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        for mod in self.modules:
            mod.update(dt)

        if self.is_enemy:
            if self.get_health() < 0:
                globals.defeated_enemies += 1
                print("enemy killed ({})".format(globals.defeated_enemies))
                self.alive = False
                # drop components
                for module in self.modules:
                    if random.random() < 0.5:
                        module._local_x = 0
                        module._local_y = 0
                        module._owner = None
                        globals.components.append(module)
                self.modules = None

    def upgrade(self, sm):
        # only add it to the ship if the corresponding slot is free
        slot = (int(sm._local_x), int(sm._local_y))
        if slot not in self.grid:
            # calculate the local coordinates for the slot
            sm._local_x *= 32
            sm._local_y *= 32
            self.grid[slot] = 1
            sm.module_initial(self)
            self.modules.append(sm)

    def get_health(self):
        return self.get_max_health() - self.damage_taken

    def get_max_health(self):
        return self.base_health * self.health_multiplier

    def damage(self, dmg):
        self.damage_taken += dmg
        if self.get_health() <= 0:
            self.alive = False
