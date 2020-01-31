import pyglet

controls_to_follow = ["ABS_RX", "ABS_RY", "ABS_X", "ABS_Y", "BTN_TL", "BTN_TR", "BTN_TL2", "BTN_TR2", "BTN_A", "BTN_B",
                      "BTN_Y", "BTN_X"]

# create the window obj
window = pyglet.window.Window(1000, 800)
# window = pyglet.window.Window(fullscreen=True)
# window.set_exclusive_mouse()
devices = pyglet.input.get_devices()

the_game_data = {
    "dx": 0.0,
    "dy": 0.0
}


def watch_control(device, control, game_data):
    """
    method for input device monitoring
    :param device:
    :param control:
    :param obj:
    :return:
    """

    @control.event
    def on_change(value):
        if control.raw_name == "ABS_X":
            # print('%r: %r.on_change(%r)' % (device, control, value))
            game_data["dx"] = 2.0 * (value / 255.0 - 0.5)
        if control.raw_name == "ABS_Y":
            # print('%r: %r.on_change(%r)' % (device, control, value))
            game_data["dy"] = -2.0 * (value / 255.0 - 0.5)

    if isinstance(control, pyglet.input.base.Button):
        @control.event
        def on_press():
            print('%r: %r.on_press()' % (device, control))

        @control.event
        def on_release():
            print('%r: %r.on_release()' % (device, control))


# search for ps4 controller (or other things with controller in its name)
# print('Devices:')
for device in devices:
    if "Controller" in device.name:
        try:
            device.open(window=window)
            for control in device.get_controls():
                if control.name in controls_to_follow or control.raw_name in controls_to_follow:
                    watch_control(device, control, the_game_data)

        except pyglet.input.DeviceException:
            print('Fail')


def update(dt):
    pass


@window.event
def on_draw():
    window.clear()
    # game.draw()


pyglet.clock.schedule_interval(update, 1.0 / 60.0)
pyglet.app.run()
