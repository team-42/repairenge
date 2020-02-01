import pyglet


class ShipComponent(pyglet.sprite.Sprite):
    def __init__(self, mass, x, y, *args, **kwargs):
        super(ShipComponent, self).__init__(*args, **kwargs)
        self.mass = mass
        self.x = x
        self.y = y

    # module actions are executed each frame
    def module_action(self, dt, game_objects):
        pass

    def module_initial(self, ship):
        pass

    def get_mass(self):
        return self.mass
