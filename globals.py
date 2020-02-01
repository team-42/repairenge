from constants import Controls

"""
defines a dict holding game relevant variables accessible from everywhere
example:
import globals

print(len(globals.projectiles))
"""

# list of projectiles
projectiles = []
# list of enemies
enemies = []
# list of components
components = []
# inputs: up, down, left, right, action button
# 0 -> no button pressed
# 1 -> button is pressed
controls = {Controls.Up: False, Controls.Down: False, Controls.Left: False, Controls.Right: False,
            Controls.Action_0: False}
# the players ship
player_ship = None  # ship.Ship()

# resources
resources = {}

# sprite batches
sprite_batches = {}