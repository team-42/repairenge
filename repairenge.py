import pyglet
from pyglet.window import key
import player_ship
import starfield
from constants import Controls
from constants import Resources
from constants import BatchNames
import globals
import enemies.drone
import random
import util

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

        # first: load resources
        self._load_resources()

        self._window = window
        self._devices = devices
        self._keyboard = keyboard

        # the players ship
        globals.player_ship = player_ship.PlayerShip()

        # the background starfield
        self._starfield = starfield.StarField(100)

    def _load_resources(self):
        """
        initially load all needed resources for the game
        :return:
        """
        # define the sprite batches, the order defines the rendering order of rendering
        globals.sprite_batches[BatchNames.Star_Batch] = pyglet.graphics.Batch()
        globals.sprite_batches[BatchNames.Enemy_Batch] = pyglet.graphics.Batch()
        globals.sprite_batches[BatchNames.Projectile_Batch] = pyglet.graphics.Batch()
        globals.sprite_batches[BatchNames.Player_Ship_Batch] = pyglet.graphics.Batch()
        globals.sprite_batches[BatchNames.Component_Batch] = pyglet.graphics.Batch()

        # load the images
        globals.resources[Resources.Image_Starfield] = pyglet.resource.image(
            "resources/environment/star.png")
        globals.resources[Resources.Image_Projectiles_Energy_01] = pyglet.resource.image(
            "resources/projectiles/energy_01.png")
        globals.resources[Resources.Image_Ship_Module_Base] = pyglet.resource.image(
            "resources/ship/base.png")
        globals.resources[Resources.Image_Ship_Module_Simple_Phaser] = pyglet.resource.image(
            "resources/ship/simple_phaser.png")

    def draw(self):
        """
        called once per frame to draw everything
        :return:
        """
        for key, batch in globals.sprite_batches.items():
            # print(key)
            batch.draw()

    def _update_and_delete(self, list_of_things, dt):
        """
        update all things and delete them if they are not alive
        :param list_of_things:
        :param dt:
        :return:
        """
        i = 0
        while i < len(list_of_things):
            list_of_things[i].update(dt)
            if not list_of_things[i].alive:
                # delete the sprite and vertices from the batch
                list_of_things[i].delete()
                if hasattr(list_of_things[i], 'modules'):
                    if list_of_things[i].modules is not None:
                        for module in list_of_things[i].modules:
                            module.delete()
                if i == len(list_of_things) - 1:
                    list_of_things.pop()
                else:
                    list_of_things[i] = list_of_things.pop()
            else:
                i += 1

    def check_collisions_with_projectiles(self, ship, projectiles):
        for projectile in projectiles:
            if projectile.alive:
                hit = False
                if util.is_colliding(projectile, ship):
                    hit = True
                if not hit:
                    for component in ship.modules:
                        if util.is_colliding(projectile, component):
                            hit = True
                            break
                if hit:
                    projectile.alive = False
                    ship.damage(projectile.damage)
                    print("ship.health = {}".format(ship.get_health()))

    def check_collision_between_ships(self, ship_a, ship_b, dt):
        if ship_a.alive and ship_b.alive:
            if util.is_colliding(ship_a, ship_b):
                dmg_for_a = ship_b.mass * ship_b.engine_power * dt
                dmg_for_b = ship_a.mass * ship_a.engine_power * dt
                ship_a.damage(dmg_for_a)
                ship_b.damage(dmg_for_b)
                print("dmg for a: {}".format(dmg_for_a))
                print("dmg for b: {}".format(dmg_for_b))

    def update(self, dt):
        """
        main update method - called once per frame - for game logic
        :param dt:
        :return:
        """
        # print(self.controls)
        self._starfield.update(dt)

        # do collision detection
        # 1: player_ship vs enemy_projectiles
        self.check_collisions_with_projectiles(globals.player_ship, globals.enemy_projectiles)

        # 2: enemies vs player_projectiles
        for enemy in globals.enemies:
            self.check_collisions_with_projectiles(enemy, globals.player_projectiles)

        # 3: player_ship vs enemies
        for enemy in globals.enemies:
            self.check_collision_between_ships(globals.player_ship, enemy, dt)

        # 4: player_ship vs free components
        for module in globals.components:
            if util.is_colliding(module, globals.player_ship):
                module._local_x = module.x - globals.player_ship.x
                module._local_y = module.y - globals.player_ship.y
                module._owner = globals.player_ship
                module.alive = False

        globals.player_ship.update(dt)

        # update all projectiles and delete them if they are not alive
        self._update_and_delete(globals.player_projectiles, dt)
        self._update_and_delete(globals.enemy_projectiles, dt)

        # update all enemies and delete them if they are not alive
        self._update_and_delete(globals.enemies, dt)

        # update all "free" components and delete them if they are not alive
        self._update_and_delete(globals.components, dt)

        # randomly add enemies:
        if random.random() < dt * 0.5:
            drone = enemies.drone.Drone(1010, random.random() * 200 + 400)
            globals.enemies.append(drone)

    def on_key_press(self, symbol, modifiers):
        """
        for keyboard presses
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.W:
            globals.controls[Controls.Up] = True
        elif symbol == key.S:
            globals.controls[Controls.Down] = True
        elif symbol == key.A:
            globals.controls[Controls.Left] = True
        elif symbol == key.D:
            globals.controls[Controls.Right] = True
        elif symbol == key.E:
            globals.controls[Controls.Action_0] = True

    def on_key_release(self, symbol, modifiers):
        """
        for keyboard releases
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == key.W:
            globals.controls[Controls.Up] = False
        elif symbol == key.S:
            globals.controls[Controls.Down] = False
        elif symbol == key.A:
            globals.controls[Controls.Left] = False
        elif symbol == key.D:
            globals.controls[Controls.Right] = False
        elif symbol == key.E:
            globals.controls[Controls.Action_0] = False


repairenge = Repairenge(window, devices, keyboard)
window.push_handlers(repairenge)


def watch_control(device, control):
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
                globals.controls[Controls.Left] = True
                globals.controls[Controls.Right] = False
            elif value > 140:
                globals.controls[Controls.Right] = True
                globals.controls[Controls.Left] = False
            else:
                globals.controls[Controls.Right] = False
                globals.controls[Controls.Left] = False

        if control.raw_name == "ABS_Y":
            if value < 110:
                globals.controls[Controls.Up] = True
                globals.controls[Controls.Down] = False
            elif value > 140:
                globals.controls[Controls.Down] = True
                globals.controls[Controls.Up] = False
            else:
                globals.controls[Controls.Down] = False
                globals.controls[Controls.Up] = False

    if isinstance(control, pyglet.input.base.Button):
        @control.event
        def on_press():
            if control.raw_name == "BTN_A":
                globals.controls[Controls.Action_0] = True

        @control.event
        def on_release():
            if control.raw_name == "BTN_A":
                globals.controls[Controls.Action_0] = False


# search for ps4 controller (or other things with controller in its name)
# only tested with ps4 dualshock controller
# print('Devices:')
for device in devices:
    if "Controller" in device.name:
        try:
            device.open(window=window)
            for control in device.get_controls():
                if control.name in controls_to_follow or control.raw_name in controls_to_follow:
                    watch_control(device, control)

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
