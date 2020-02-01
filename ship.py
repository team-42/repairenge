import pyglet
import ship_components.ship_component_simple_phaser as smsp


class Ship(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Ship, self).__init__(*args, **kwargs)
        self.x = 100.0
        self.y = 100.0

        # Health Segment
        self.base_health = 100
        self.health_multiplier = 1.0
        self.damage_taken = 0
        self.current_health = self.base_health * self.health_multiplier

        # ship movement properties
        self.engine_power = 1000.0
        self.mass = 1.0

        # modules
        self.modules = [smsp.ShipModuleSimplePhaser(0, 0)]


    def update(self, dt, controls):
        """
        :param dt:
        :return:
        """
        for mod in self.modules:
            mod.module_action(dt)

        # controls:
        if controls["up"]:
            self.y += self.engine_power / self.mass * dt
        if controls["down"]:
            self.y -= self.engine_power / self.mass * dt
        if controls["left"]:
            self.x -= self.engine_power / self.mass * dt
        if controls["right"]:
            self.x += self.engine_power / self.mass * dt



    def upgrade(self, sm):
        sm.module_initial()

    def get_health(self):
        return (self.base_health * self.health_multiplier) - self.damage_taken

    def damage(self, dmg):
        self.damage_taken += dmg
