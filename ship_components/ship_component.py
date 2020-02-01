import pyglet


class ShipModule(pyglet.sprite.Sprite):
    def __init__(self, mass, x, y, *args, **kwargs):
        super(ShipModule, self).__init__(*args, **kwargs)
        self.mass = mass
        self.x = x
        self.y = y

    # module actions are executed each frame
    def module_action(self, dt):
        pass

    def module_initial(self, ship):
        pass

    def get_mass(self):
        return self.mass
