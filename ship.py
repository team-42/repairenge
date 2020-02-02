import random

import pyglet

import globals
from constants import BatchNames
from collections import deque


class Ship(pyglet.sprite.Sprite):
    base_shield: int

    drop_rate = 0.8

    def __init__(self, is_enemy, resource, *args, **kwargs):
        if is_enemy:
            batch = globals.sprite_batches[BatchNames.Enemy_Batch]
        else:
            batch = globals.sprite_batches[BatchNames.Player_Ship_Batch]
        base_resource = resource

        super(Ship, self).__init__(globals.resources[base_resource],
                                   batch=batch, *args, **kwargs)

        self.x = globals.window.width * 0.2
        self.y = globals.window.height * 0.5

        # set this to true if this is an enemy ship
        self.is_enemy = is_enemy
        self.alive = True

        # component grid:
        # uses 2-tuples as indices
        # value == 1 -> reserved for base model
        self.grid = {
            (0, 0): 1,
            (-1, 0): 1
        }

        # Health Segment
        self.base_health = 200
        self.health_multiplier = 1.0
        self.damage_taken = 0
        self.base_shield = 0
        self.shield_damage_taken = 0
        self.current_health = self.base_health * self.health_multiplier

        # ship movement properties
        self.engine_power = 500000.0
        self.mass = 1000.0

        # modules
        self.modules = list()

        pyglet.clock.schedule_interval(self.regenerate_shields, 0.2)

    def regenerate_shields(self, dt):
        self.shield_damage_taken -= min(self.shield_damage_taken, int(self.base_shield / 10))

    def update(self, dt):
        """
        :param dt:
        :return:
        """
        for mod in self.modules:
            mod.update(dt)

        if self.is_enemy:
            if self.get_health() <= 0:
                globals.defeated_enemies += 1
                print("enemy killed ({})".format(globals.defeated_enemies))
                self.alive = False
                # drop components
                for module in self.modules:
                    count_on_player_ship = globals.player_ship.get_count_of_component_type(module)
                    print("Count of {} on player ship is {}".format(type(module), count_on_player_ship))
                    if random.random() < pow(self.drop_rate, 1 + count_on_player_ship):
                        module._local_x = 0
                        module._local_y = 0
                        module._owner = None
                        globals.components.append(module)
                self.modules = None

    def _add_to_queue(self, open_list, closed_dict, slot):
        if slot not in closed_dict:
            open_list.append(slot)
            closed_dict[slot] = 1

    def _add_neighbours(self, open_list, closed_dict, slot):
        next_slot = (slot[0], slot[1] - 1)
        self._add_to_queue(open_list, closed_dict, next_slot)
        next_slot = (slot[0] - 1, slot[1])
        self._add_to_queue(open_list, closed_dict, next_slot)
        next_slot = (slot[0], slot[1] + 1)
        self._add_to_queue(open_list, closed_dict, next_slot)
        next_slot = (slot[0] + 1, slot[1])
        self._add_to_queue(open_list, closed_dict, next_slot)

    def _get_next_free_slot(self, slot):
        """
        determine the next free slot from the given one
         if the given one is free: use it
         else: search with 4-neighbourhood, in following order: bottom, left, top, right
        :param slot:
        :return: the free slot
        """
        open_list = deque()
        closed_dict = self.grid.copy()
        # first add this slot
        self._add_to_queue(open_list,closed_dict, slot)
        while len(open_list) > 0:
            # get next slot to check
            slot_to_check = open_list.popleft()
            if slot_to_check not in self.grid:
                return slot
            else:
                # add neighbours to queue
                self._add_neighbours(open_list,closed_dict, slot_to_check)
        # default return an invalid slot
        return (0,0)

    def upgrade(self, sm):
        # add module to the ship at the next free slot
        slot = (int(sm._local_x), int(sm._local_y))
        slot = self._get_next_free_slot(slot)
        print("selected slot: {}".format(slot))
        if slot not in self.grid:
            print("slot was free")
            # calculate the local coordinates for the slot
            sm._local_x *= 32
            sm._local_y *= 32
            self.grid[slot] = 1
            sm.module_initial(self)
            self.modules.append(sm)
        else:
            print("slot was not free")

    def get_count_of_component_type(self, component_type):
        result: int = 0
        for module in self.modules:
            if module.image == component_type.image:
                result += 1
        return result

    def get_health(self):
        return self.get_max_health() - self.damage_taken

    def get_max_health(self):
        return self.base_health * self.health_multiplier

    def get_health_percentage(self):
        return self.get_health() * 100 / self.get_max_health()

    def get_shield_percentage(self):
        if self.base_shield == 0:
            return 0
        else:
            return (self.base_shield - self.shield_damage_taken) * 100 / self.base_shield

    def damage(self, dmg):
        if dmg > 0 and self.base_shield - self.shield_damage_taken > 0:
            absorbed_by_shield = min(dmg, self.base_shield - self.shield_damage_taken)
            self.shield_damage_taken += absorbed_by_shield
            dmg -= absorbed_by_shield
        self.damage_taken += dmg
        if self.get_health() <= 0:
            self.alive = False
