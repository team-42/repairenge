import pyglet
from pyglet.window import key
import ship
import starfield
from constants import GameObjects
from constants import Controls

controls_to_follow = ["ABS_RX", "ABS_RY", "ABS_X", "ABS_Y", "BTN_TL", "BTN_TR", "BTN_TL2", "BTN_TR2", "BTN_A", "BTN_B",
                      "BTN_Y", "BTN_X"]

# create the window obj
window = pyglet.window.Window(1000, 800)
# window = pyglet.window.Window(fullscreen=True)
# window.set_exclusive_mouse()

# for keyboard input
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

devices = pyglet.input.get_devices()


class Repairenge:
    """
    main class with update, draw ...
    """

    def __init__(self, window, devices, keyboard):
        self._window = window
        self._devices = devices
        self._keyboard = keyboard

        self.game_objects = dict()
        # list of projectiles
        self.game_objects[GameObjects.Projectiles] = []
        # list of enemies
        self.game_objects[GameObjects.Enemies] = []
        # list of components
        self.game_objects[GameObjects.Components] = []
        # inputs: up, down, left, right, action button
        # 0 -> no button pressed
        # 1 -> button is pressed
        self.game_objects[GameObjects.Controls] = {Controls.Up: False, Controls.Down: False, Controls.Left: False,
                                                   Controls.Right: False, Controls.Action_0: False}
        # the players ship
        self.game_objects[GameObjects.Ship] = ship.Ship()

        # the background starfield
        self._starfield = starfield.StarField(100)

    def draw(self):
        """
        called once per frame to draw everything
        :return:
        """

        self._starfield.draw()
        for projectile in self.game_objects[GameObjects.Projectiles]:
            projectile.draw()

        for enemy in self.game_objects[GameObjects.Enemies]:
            enemy.draw()

        # draw ship:
        self.game_objects[GameObjects.Ship].draw()
        # draw its modules:
        for ship_component in self.game_objects[GameObjects.Ship].modules:
            ship_component.draw()

    def _update_and_delete(self, list_of_things, dt):
        # update all things and delete them if they are not alive
        i = 0
        while i < len(list_of_things):
            list_of_things[i].update(dt, self.game_objects)
            if not list_of_things[i].alive:
                if i == len(list_of_things) - 1:
                    list_of_things.pop()
                else:
                    list_of_things[i] = list_of_things.pop()
            else:
                i += 1

    def update(self, dt):
        """
        main update method - called once per frame - for game logic
        :param dt:
        :return:
        """
        # print(self.controls)
        self._starfield.update(dt)

        self.game_objects[GameObjects.Ship].update(dt, self.game_objects)

        # update all projectiles and delete them if they are not alive
        self._update_and_delete(self.game_objects[GameObjects.Projectiles], dt)

        # update all enemies and delete them if they are not alive
        self._update_and_delete(self.game_objects[GameObjects.Enemies], dt)

        # update all "free" components and delete them if they are not alive
        self._update_and_delete(self.game_objects[GameObjects.Components], dt)

    def on_key_press(self, symbol, modifiers):
        """
        for keyboard presses
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.W:
            self.game_objects[GameObjects.Controls][Controls.Up] = True
        elif symbol == key.S:
            self.game_objects[GameObjects.Controls][Controls.Down] = True
        elif symbol == key.A:
            self.game_objects[GameObjects.Controls][Controls.Left] = True
        elif symbol == key.D:
            self.game_objects[GameObjects.Controls][Controls.Right] = True
        elif symbol == key.E:
            self.game_objects[GameObjects.Controls][Controls.Action_0] = True

    def on_key_release(self, symbol, modifiers):
        """
        for keyboard releases
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.W:
            self.game_objects[GameObjects.Controls][Controls.Up] = False
        elif symbol == key.S:
            self.game_objects[GameObjects.Controls][Controls.Down] = False
        elif symbol == key.A:
            self.game_objects[GameObjects.Controls][Controls.Left] = False
        elif symbol == key.D:
            self.game_objects[GameObjects.Controls][Controls.Right] = False
        elif symbol == key.E:
            self.game_objects[GameObjects.Controls][Controls.Action_0] = False


repairenge = Repairenge(window, devices, keyboard)
window.push_handlers(repairenge)


def watch_control(device, control, repairenge):
    """
    method for input device monitoring - noobstick
    :param device:
    :param control:
    :param obj:
    :return:
    """

    @control.event
    def on_change(value):
        if control.raw_name == "ABS_X":
            if value < 110:
                repairenge.game_objects[GameObjects.Controls][Controls.Left] = True
                repairenge.game_objects[GameObjects.Controls][Controls.Right] = False
            elif value > 140:
                repairenge.game_objects[GameObjects.Controls][Controls.Right] = True
                repairenge.game_objects[GameObjects.Controls][Controls.Left] = False
            else:
                repairenge.game_objects[GameObjects.Controls][Controls.Right] = False
                repairenge.game_objects[GameObjects.Controls][Controls.Left] = False

        if control.raw_name == "ABS_Y":
            if value < 110:
                repairenge.game_objects[GameObjects.Controls][Controls.Up] = True
                repairenge.game_objects[GameObjects.Controls][Controls.Down] = False
            elif value > 140:
                repairenge.game_objects[GameObjects.Controls][Controls.Down] = True
                repairenge.game_objects[GameObjects.Controls][Controls.Up] = False
            else:
                repairenge.game_objects[GameObjects.Controls][Controls.Down] = False
                repairenge.game_objects[GameObjects.Controls][Controls.Up] = False

    if isinstance(control, pyglet.input.base.Button):
        @control.event
        def on_press():
            if control.raw_name == "BTN_A":
                repairenge.game_objects[GameObjects.Controls][Controls.Action_0] = True

        @control.event
        def on_release():
            if control.raw_name == "BTN_A":
                repairenge.game_objects[GameObjects.Controls][Controls.Action_0] = False


# search for ps4 controller (or other things with controller in its name)
# print('Devices:')
for device in devices:
    if "Controller" in device.name:
        try:
            device.open(window=window)
            for control in device.get_controls():
                if control.name in controls_to_follow or control.raw_name in controls_to_follow:
                    watch_control(device, control, repairenge)

        except pyglet.input.DeviceException:
            print('Fail')


def update(dt):
    repairenge.update(dt)


@window.event
def on_draw():
    window.clear()
    repairenge.draw()


pyglet.clock.schedule_interval(update, 1.0 / 60)
pyglet.app.run()
