import pyglet
import globals


class ShipComponent(pyglet.sprite.Sprite):
    def __init__(self, mass, x, y, *args, **kwargs):
        super(ShipComponent, self).__init__(*args, **kwargs)
        self.mass = mass
        self._local_x = x
        self._local_y = y

    # module actions are executed each frame
    def module_action(self, dt):
        ship_x = globals.player_ship.x
        ship_y = globals.player_ship.y
        self.x = ship_x + self._local_x
        self.y = ship_y + self._local_y

    def module_initial(self, ship):
        pass

    def get_mass(self):
        return self.mass
