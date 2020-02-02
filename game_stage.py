import random

import enemies.behemoth
import enemies.drone
import enemies.frigate
import enemies.reaper
import globals
from enemies.boss import Boss
from enemies.tinyboss import TinyBoss


class GameStage:
    def get_boss(self, x, y):
        pass

    def get_enemy(self, x, y):
        pass

    def get_num_enemies_to_defeat(self):
        pass


class StageOne(GameStage):
    def get_boss(self, x, y):
        return TinyBoss(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        return enemies.drone.Drone(enemy_x, enemy_y)

    def get_num_enemies_to_defeat(self):
        return 10


class StageTwo(GameStage):
    def get_boss(self, x, y):
        return Boss(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        enemy_type = random.randint(0, 100)
        if enemy_type < globals.defeated_enemies / 2:
            # behemoth
            enemy = enemies.behemoth.Behemoth(enemy_x, enemy_y)
        elif enemy_type < globals.defeated_enemies:
            # reaper
            enemy = enemies.reaper.Reaper(enemy_x, enemy_y)
        elif enemy_type < globals.defeated_enemies * 2.5:
            # frigate
            enemy = enemies.frigate.Frigate(enemy_x, enemy_y)
        else:
            enemy = enemies.drone.Drone(enemy_x, enemy_y)
        return enemy

    def get_num_enemies_to_defeat(self):
        return 30
