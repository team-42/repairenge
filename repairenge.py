import pyglet
from pyglet.window import key
import Ship
import starfield

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

        # inputs: up, down, left, right, action button
        # 0 -> no button pressed
        # 1 -> button is pressed
        self.controls = {"up": False, "down": False, "left": False, "right": False, "action_0": False}

        self._ship = Ship.Ship()
        self._starfield = starfield.StarField(100)
        self._shipmodules = []

    def draw(self):

        self._starfield.draw()
        # self._ship.draw()
        # self._shipmodules.draw()

    def update(self, dt):
        # print(self.controls)
        self._starfield.update(dt)
        self._ship.update(dt)
        for shipmodule in self._shipmodules:
            shipmodule.update(dt)

    def on_key_press(self, symbol, modifiers):
        """
        for keyboard presses
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.UP:
            self.controls['up'] = True
        elif symbol == key.DOWN:
            self.controls['down'] = True
        elif symbol == key.LEFT:
            self.controls['left'] = True
        elif symbol == key.RIGHT:
            self.controls['right'] = True
        elif symbol == key.E:
            self.controls['action_0'] = True

    def on_key_release(self, symbol, modifiers):
        """
        for keyboard releases
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.UP:
            self.controls['up'] = False
        elif symbol == key.DOWN:
            self.controls['down'] = False
        elif symbol == key.LEFT:
            self.controls['left'] = False
        elif symbol == key.RIGHT:
            self.controls['right'] = False
        elif symbol == key.E:
            self.controls['action_0'] = False


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
            if value < 120:
                repairenge.controls["left"] = True
                repairenge.controls["right"] = False
            elif value > 130:
                repairenge.controls["right"] = True
                repairenge.controls["left"] = False
            else:
                repairenge.controls["right"] = False
                repairenge.controls["left"] = False

        if control.raw_name == "ABS_Y":
            if value < 120:
                repairenge.controls["up"] = True
                repairenge.controls["down"] = False
            elif value > 130:
                repairenge.controls["down"] = True
                repairenge.controls["up"] = False
            else:
                repairenge.controls["down"] = False
                repairenge.controls["up"] = False

    if isinstance(control, pyglet.input.base.Button):
        @control.event
        def on_press():
            if control.raw_name == "BTN_A":
                repairenge.controls["action_0"] = True

        @control.event
        def on_release():
            if control.raw_name == "BTN_A":
                repairenge.controls["action_0"] = False


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


pyglet.clock.schedule_interval(update, 1.0 / 60.0)
pyglet.app.run()
