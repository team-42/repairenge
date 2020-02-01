from constants import Controls

"""
defines a dict holding game relevant variables accessible from everywhere
example:
import globals

print(len(globals.projectiles))
"""

# list of projectiles
player_projectiles = []  # fired by the player, can only hit enemies
enemy_projectiles = []  # fired by enemies, can only hit the player
# list of enemies
enemies = []
# list of free floating components
components = []
# inputs: up, down, left, right, action button
# 0 -> no button pressed
# 1 -> button is pressed
controls = {Controls.Up: False, Controls.Down: False, Controls.Left: False, Controls.Right: False,
            Controls.Action_0: False, Controls.Action_1: False}
# the players ship
player_ship = None  # ship.Ship()
defeated_enemies: int = 0

# resources
resources = {}

# sprite batches
sprite_batches = {}

window = None
