import random

import enemies.behemoth
import enemies.drone
import enemies.freighter
import enemies.frigate
import enemies.hammerhead
import enemies.reaper
import globals
from enemies.boss import Boss
from enemies.goliath import Goliath
from enemies.ramboss import RamBoss
from enemies.tinyboss import TinyBoss
from enemies.sniper import Sniper


class GameStage:
    def get_boss(self, x, y):
        pass

    def get_enemy(self, x, y):
        pass

    def get_num_enemies_to_defeat(self):
        pass

    def get_enemy_density(self):
        return 0.5


class StageOne(GameStage):
    def get_boss(self, x, y):
        return TinyBoss(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        return enemies.drone.Drone(enemy_x, enemy_y)

    def get_num_enemies_to_defeat(self):
        return 10

    def get_enemy_density(self):
        return 0.3


class StageTwo(GameStage):
    def get_boss(self, x, y):
        return RamBoss(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        enemy_type = random.randint(0, 100)
        if enemy_type < 50:
            # drone
            enemy = enemies.drone.Drone(enemy_x, enemy_y)
        elif enemy_type < 92:
            # hammerhead
            enemy = enemies.hammerhead.Hammerhead(enemy_x, enemy_y)
        else:
            # frigate
            enemy = enemies.frigate.Frigate(enemy_x, enemy_y)
        return enemy

    def get_num_enemies_to_defeat(self):
        return 10

    def get_enemy_density(self):
        return 0.4


class StageThree(GameStage):
    def get_boss(self, x, y):
        return Boss(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        enemy_type = random.randint(0, 100)
        if enemy_type < globals.defeated_enemies / 2:
            # sniper
            enemy = enemies.sniper.Sniper(enemy_x, enemy_y)
        elif enemy_type < globals.defeated_enemies:
            # reaper
            enemy = enemies.reaper.Reaper(enemy_x, enemy_y)
        elif enemy_type < globals.defeated_enemies * 2.5:
            # frigate
            enemy = enemies.frigate.Frigate(enemy_x, enemy_y)
        elif enemy_type > 80:
            # freighter
            enemy = enemies.freighter.Freighter(enemy_x, enemy_y)
        else:
            enemy = enemies.drone.Drone(enemy_x, enemy_y)
        return enemy

    def get_num_enemies_to_defeat(self):
        return 30

    def get_enemy_density(self):
        return 0.4


class StageFour(GameStage):
    def get_boss(self, x, y):
        return Goliath(x, y)

    def get_enemy(self, enemy_x, enemy_y):
        enemy_type = random.randint(0, 100)
        if enemy_type < 30:
            # behemoth
            enemy = enemies.behemoth.Behemoth(enemy_x, enemy_y)
        elif enemy_type < 50:
            # reaper
            enemy = enemies.reaper.Reaper(enemy_x, enemy_y)
        elif enemy_type < 70:
            # hammerhead
            enemy = enemies.hammerhead.Hammerhead(enemy_x, enemy_y)
        else:
            # frigate
            enemy = enemies.frigate.Frigate(enemy_x, enemy_y)
        return enemy

    def get_num_enemies_to_defeat(self):
        return 30

    def get_enemy_density(self):
        return 0.5
