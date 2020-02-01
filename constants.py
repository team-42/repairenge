from enum import Enum


class GameObjects(Enum):
    # the players ship
    Ship = "S"
    # the list of projectile on the screen
    Projectiles = "P"
    # the list of enemies (on the screen)
    Enemies = "E"
    # the list of "free" floating components/modules to collect
    Components = "C"
    # the current pressed buttons -> see Controls enum for buttons
    Controls = "X"


class Controls(Enum):
    Up = "u"
    Down = "d"
    Left = "l"
    Right = "r"
    # Key: E or X(Noobstick)
    Action_0 = "0"
