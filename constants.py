from enum import Enum
from enum import IntEnum


class Controls(Enum):
    Up = "u"
    Down = "d"
    Left = "l"
    Right = "r"
    # Key: E or X(Noobstick)
    Action_0 = "0"
    # Key: Q or O on noobstick
    Action_1 = "1"


class Resources(Enum):
    Image_Starfield = 0
    Image_Projectiles_Energy_01 = 100
    Image_Ship_Module_Base = 200
    Image_Ship_Module_Simple_Phaser = 201
    Image_Ship_Module_Angle_Laser = 202
    Image_Ship_Module_Heavy_Laser = 203
    Image_Ship_Module_Hull = 210
    Image_Ship_Module_Repair = 211
    Image_Ship_Module_Jet = 220
    Image_Ship_Module_Enemy = 300
    Image_Ship_Module_Enemy_Medium = 301
    Image_Ship_Module_Enemy_Medium2 = 302
    Image_Ship_Module_Enemy_Large = 303
    Image_Ship_Module_Enemy_Boss = 304
    Image_Healthbar = 400


class BatchNames(Enum):
    Star_Batch = 0
    Enemy_Batch = 1
    Projectile_Batch = 2
    Player_Ship_Batch = 3
    Component_Batch = 4
    Health_Bar_Batch = 5


class LaserColors(Enum):
    Player_Ship = (80, 80, 255)
    Enemy_Ship = (255, 122, 65)
