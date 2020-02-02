import pyglet
import globals


class ShipComponent(pyglet.sprite.Sprite):
    def __init__(self, x, y, owner, *args, **kwargs):
        super(ShipComponent, self).__init__(*args, **kwargs)
        self.mass = 0
        self._local_x = x
        self._local_y = y
        self._owner = owner
        self.alive = True

    # module actions are executed each frame
    def update(self, dt):
        if self._owner is not None:
            self.x = self._owner.x + self._local_x
            self.y = self._owner.y + self._local_y

    def module_initial(self, ship):
        if ship.is_enemy:
            self.rotation = 180

#    def get_mass(self):
#        return self.mass
