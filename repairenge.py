import random

import pyglet
import ship
from pyglet.text import Label
from pyglet.window import key

import enemies.drone
import globals
import player_ship
import starfield
import util
from constants import BatchNames
from constants import Controls
from constants import Resources
from enemies.boss import Boss
import math

CONDITION_RUNNING = 1
CONDITION_SPAWN_BOSS = 2
CONDITION_BOSS = 3
CONDITION_LOSS = -1
CONDITION_WIN = -2
NUM_ENEMIES_TO_DEFEAT = 3

# raw_names on ps4 controller
controls_to_follow = ["ABS_RX", "ABS_RY", "ABS_X", "ABS_Y", "BTN_TL", "BTN_TR", "BTN_TL2", "BTN_TR2", "BTN_A", "BTN_B",
                      "BTN_Y", "BTN_X"]

# create the window obj
window = pyglet.window.Window(1000, 768)
globals.window = window

# for keyboard input
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

devices = pyglet.input.get_devices()

play = pyglet.media.load('resources/music/complete.wav')
player = pyglet.media.Player()
player.queue(play)
player.loop = True
player.play()

class Repairenge:
    """
    main class with update, draw ...
    """
    victory_label: Label
    game_over_label: Label
    game_condition: int = CONDITION_RUNNING
    boss: Boss

    def __init__(self, window, devices, keyboard):

        # first: load resourcess
        self._load_resources()

        self._window = window
        self._devices = devices
        self._keyboard = keyboard

        # the players ship
        globals.player_ship = player_ship.PlayerShip()

        # the background starfield
        self._starfield = starfield.StarField(100)

        self.game_over_label = pyglet.text.Label('Game Over',
                                                 font_name='Arial',
                                                 font_size=60,
                                                 color=(190, 0, 50, 255),
                                                 x=globals.window.width // 2, y=globals.window.height // 2,
                                                 anchor_x='center', anchor_y='center')
        self.victory_label = pyglet.text.Label('Victory',
                                               font_name='Arial',
                                               font_size=60,
                                               color=(0, 136, 86, 255),
                                               x=globals.window.width // 2, y=globals.window.height // 2,
                                               anchor_x='center', anchor_y='center')

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
        util.center_image(globals.resources[Resources.Image_Starfield])

        globals.resources[Resources.Image_Projectiles_Energy_01] = pyglet.resource.image(
            "resources/projectiles/energy_01.png")
        util.center_image(globals.resources[Resources.Image_Projectiles_Energy_01])

        globals.resources[Resources.Image_Ship_Module_Base] = pyglet.resource.image(
            "resources/ship/ship_body.png")
        globals.resources[Resources.Image_Ship_Module_Base].anchor_x = 32 + 16
        globals.resources[Resources.Image_Ship_Module_Base].anchor_y = 16

        globals.resources[Resources.Image_Ship_Module_Enemy] = pyglet.resource.image(
            "resources/ship/enemy_easy_body.png")
        globals.resources[Resources.Image_Ship_Module_Enemy].anchor_x = 32 + 16
        globals.resources[Resources.Image_Ship_Module_Enemy].anchor_y = 16

        globals.resources[Resources.Image_Ship_Module_Simple_Phaser] = pyglet.resource.image(
            "resources/ship/component_onbase_phaser.png")
        util.center_image(globals.resources[Resources.Image_Ship_Module_Simple_Phaser])

    def draw(self):
        """
        called once per frame to draw everything
        :return:
        """
        for key, batch in globals.sprite_batches.items():
            # print(key)
            batch.draw()
        if self.game_condition == CONDITION_LOSS:
            self.game_over_label.draw()
        if self.game_condition == CONDITION_WIN:
            self.victory_label.draw()

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
                if isinstance(list_of_things[i], ship.Ship):
                    print("Delete thing {}".format(list_of_things[i]))
                    if isinstance(list_of_things[i], Boss):
                        self.game_condition = CONDITION_WIN
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
                dmg_for_a = ship_b.mass * ship_b.engine_power * dt / 1000000
                dmg_for_b = ship_a.mass * ship_a.engine_power * dt / 1000000
                ship_a.damage(dmg_for_a)
                ship_b.damage(dmg_for_b)
                print("dmg for a: {}".format(dmg_for_a))
                print("dmg for b: {}".format(dmg_for_b))

    def check_collision_between_player_and_components(self):
        # dont touch this
        i = 0
        while i < len(globals.components):
            module = globals.components[i]
            # check collision with each slot of player
            for slot in globals.player_ship.grid:
                # calc distance
                distance_x = globals.player_ship.x + (slot[0] * 32) - module.x
                distance_y = globals.player_ship.y + (slot[1] * 32) - module.y
                if distance_x > -32 and distance_x < 32 and distance_y > -32 and distance_y < 32:
                    # calculate slot to attach to
                    x_dir = 0
                    y_dir = 0
                    if abs(distance_x) > abs(distance_y):
                        x_dir = 1 if distance_x < 0 else -1
                    else:
                        y_dir = 1 if distance_y < 0 else -1

                    new_x = slot[0] + x_dir
                    new_y = slot[1] + y_dir

                    module._local_x = new_x
                    module._local_y = new_y
                    module._owner = globals.player_ship
                    globals.player_ship.upgrade(module)
                    if i == len(globals.components) - 1:
                        globals.components.pop()
                    else:
                        globals.components[i] = globals.components.pop()
                    break
            i += 1

    def update(self, dt):
        """
        main update method - called once per frame - for game logic
        :param dt:
        :return:
        """
        if self.game_condition < CONDITION_RUNNING:
            return
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
        self.check_collision_between_player_and_components()

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
            if self.game_condition == CONDITION_RUNNING:
                drone = enemies.drone.Drone(globals.window.width + 50,
                                            random.random() * (globals.window.height / 4) + globals.window.height / 2)
                globals.enemies.append(drone)
            elif self.game_condition == CONDITION_SPAWN_BOSS:
                self.boss = Boss(globals.window.width + 50,
                                 random.random() * (globals.window.height / 4) + globals.window.height / 2)
                globals.enemies.append(self.boss)
                print("Game condition has changed to BOSS")
                self.game_condition = CONDITION_BOSS

        self.update_game_condition()

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
        elif symbol == key.SPACE:
            globals.controls[Controls.Action_0] = True
        elif symbol == key.ENTER:
            globals.controls[Controls.Action_1] = True

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
        elif symbol == key.SPACE:
            globals.controls[Controls.Action_0] = False
        elif symbol == key.ENTER:
            globals.controls[Controls.Action_1] = False

    # Checks for win and loss of the game
    def update_game_condition(self):
        if self.game_condition >= CONDITION_RUNNING:
            loss = globals.player_ship.get_health() <= 0
            boss = globals.defeated_enemies >= NUM_ENEMIES_TO_DEFEAT and self.game_condition == CONDITION_RUNNING
            if loss:
                self.game_condition = CONDITION_LOSS
                player_ship.alive = False
                print("Game condition has changed to LOSS")
            elif boss:
                self.game_condition = CONDITION_SPAWN_BOSS
                print("Game condition has changed to SPAWN_BOSS")


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
            elif control.raw_name == "BTN_B":
                globals.controls[Controls.Action_1] = True

        @control.event
        def on_release():
            if control.raw_name == "BTN_A":
                globals.controls[Controls.Action_0] = False
            elif control.raw_name == "BTN_B":
                globals.controls[Controls.Action_1] = False


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
play.delete()
player.delete()