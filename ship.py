import pyglet
import globals
from constants import Resources
from constants import BatchNames


class Ship(pyglet.sprite.Sprite):
    def __init__(self, is_enemy, *args, **kwargs):
        if is_enemy:
            batch = globals.sprite_batches[BatchNames.Enemy_Batch]
            base_resource = Resources.Image_Ship_Module_Enemy
        else:
            batch = globals.sprite_batches[BatchNames.Player_Ship_Batch]
            base_resource = Resources.Image_Ship_Module_Base

        super(Ship, self).__init__(globals.resources[base_resource],
                                   batch=batch, *args, **kwargs)

        self.x = 100.0
        self.y = 100.0

        # set this to true if this is an enemy ship
        self.is_enemy = is_enemy
        self.alive = True

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
                # # drop components
                # for module in self.modules:
                #     module._local_x = 0
                #     module._local_y = 0
                #     # module.x = module._owner.x
                #     # module.y = module._owner.y
                #     module._owner = None
                #     globals.components.append(module)
                # self.modules = None

    def upgrade(self, sm):
        sm.module_initial(self)
        self.modules.append(sm)


    def get_health(self):
        return (self.base_health * self.health_multiplier) - self.damage_taken

    def damage(self, dmg):
        self.damage_taken += dmg
        if self.get_health() < 0:
            self.alive = False
