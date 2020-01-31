import ShipModule


class Ship:
    def __init__(self):
        self.pos_x = 0.0
        self.pos_y = 0.0

        # Health Segment
        self.base_health = 100
        self.health_multiplier = 1.0
        self.damage_taken = 0
        self.current_health = self.base_health * self.health_multiplier

        # ship movement properties
        self.engine_power = 1.0
        self.mass = 1000.0

        # modules
        self.modules = []

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        pass

    def upgrade(self, sm):
        sm.module_initial()

    def draw(self):
        pass

    def get_health(self):
        return (self.base_health * self.health_multiplier) - self.damage_taken

    def damage(self, dmg):
        self.damage_taken += dmg
