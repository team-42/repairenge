import pyglet
from constants import GameObjects


class ShipComponent(pyglet.sprite.Sprite):
    def __init__(self, mass, x, y, *args, **kwargs):
        super(ShipComponent, self).__init__(*args, **kwargs)
        self.mass = mass
        self._local_x = x
        self._local_y = y

    # module actions are executed each frame
    def module_action(self, dt, game_objects):
        ship_x = game_objects[GameObjects.Ship].x
        ship_y = game_objects[GameObjects.Ship].y
        self.x = ship_x + self._local_x
        self.y = ship_y + self._local_y

    def module_initial(self, ship):
        pass

    def get_mass(self):
        return self.mass
