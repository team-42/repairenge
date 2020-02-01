from enum import Enum


class Controls(Enum):
    Up = "u"
    Down = "d"
    Left = "l"
    Right = "r"
    # Key: E or X(Noobstick)
    Action_0 = "0"


class Resources(Enum):
    Image_Starfield = 0
    Image_Projectiles_Energy_01 = 100
    Image_Ship_Module_Base = 200
    Image_Ship_Module_Simple_Phaser = 201
    Image_Ship_Module_Enemy = 300


class BatchNames(Enum):
    Star_Batch = 0
    Enemy_Batch = 1
    Projectile_Batch = 2
    Player_Ship_Batch = 3
    Component_Batch = 4

class LaserColors(Enum):
    Player_Ship = (80, 80, 255)
    Enemy_Ship = (255, 122, 65)
