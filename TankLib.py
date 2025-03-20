"""
The Library file of the game
"""


from dataclasses import dataclass, field
from typing import List, Literal


def is_lower_equal(a: int | float, b: int | float) -> bool:
    """
    The function to check if a is equal or lower than b

    with a precision of 10e-6
    """
    return abs(a - b) < 10e-6 or a < b


def check_collision(obj1: tuple[int | float, int | float, int, int], obj2: tuple[int | float, int | float, int, int]) -> bool:
    """
    The function to check if obj2 is in obj1

    obj: (pos_x, pos_y, size_x, size_y)
    where pos_x and pos_y are the center of the object
    and size_x and size_y are the size of the object (width/2 and height/2)

    for example:
    if you have an object with pos_x = 10, pos_y = 20, size_x = 5, size_y = 11
    the object will be (10, 20, 5, 11)

    if you have an object with pos_x = 10, pos_y = 20, size = 5
    the object will be (10, 20, 5, 5)
    """
    distance_x: int | float = abs(obj1[0] - obj2[0])
    distance_y: int | float = abs(obj1[1] - obj2[1])
    max_x: int = obj1[2] + obj2[2]
    max_y: int = obj1[3] + obj2[3]

    return is_lower_equal(distance_x, max_x) and \
        is_lower_equal(distance_y, max_y)


@dataclass
class Wall:
    """
    The class for the wall
    """
    pos_x: int = 0
    pos_y: int = 0
    size_x: int = 0
    size_y: int = 0

    def is_in_wall(self: "Wall", pos_x: int | float, pos_y: int | float, width: int, height: int) -> bool:
        """
        The function to check if the position is valid
        for this wall
        """
        obj1: tuple[int, int, int, int] = (self.pos_x, self.pos_y, self.size_x, self.size_y)
        obj2: tuple[int | float, int | float, int, int] = (pos_x, pos_y, width, height)

        return check_collision(obj1, obj2)

    def copy(self: "Wall") -> "Wall":
        """
        The function to copy the wall
        """
        return Wall(self.pos_x, self.pos_y, self.size_x, self.size_y)


@dataclass
class Bullet:
    """
    The class for the bullet
    """
    pos_x: int = 0
    pos_y: int = 0
    direction: tuple[int, int] = (0, 0)
    size: int = 0

    def is_in_bullet(self: "Bullet", pos_x: int | float, pos_y: int | float, size_x: int, size_y: int) -> bool:
        """
        The function to check if the position is valid
        for this bullet
        """
        obj1: tuple[int, int, int, int] = (self.pos_x, self.pos_y, self.size, self.size)
        obj2: tuple[int | float, int | float, int, int] = (pos_x, pos_y, size_x, size_y)
        return check_collision(obj1, obj2)

    def copy(self: "Bullet") -> "Bullet":
        """
        The function to copy the bullet
        """
        return Bullet(self.pos_x, self.pos_y, self.direction, self.size)


@dataclass
class Tank:
    """
    The class for the tank
    """
    is_alive: bool = True
    name: str = "Name"
    pos_x: int = 0
    pos_y: int = 0
    size: int = 0
    max_bullets: int = 0
    bullets: List[Bullet] = field(default_factory=list)

    def is_in_tank(self: "Tank", pos_x: int | float, pos_y: int | float, size_x: int, size_y: int) -> bool:
        """
        The function to check if the position is valid
        for this tank
        """
        obj1: tuple[int, int, int, int] = (self.pos_x, self.pos_y, self.size, self.size)
        obj2: tuple[int | float, int | float, int, int] = (pos_x, pos_y, size_x, size_y)
        return check_collision(obj1, obj2)

    def copy(self: "Tank") -> "Tank":
        """
        The function to copy the tank
        """
        new_bullets: List[Bullet] = [a.copy() for a in self.bullets]
        return Tank(self.is_alive, self.name, self.pos_x, self.pos_y, self.size, self.max_bullets, new_bullets)


@dataclass
class TankAction:
    """
    The class for the tank action
    """
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"] = "NONE"
    shoot: bool = False
    shoot_direction: tuple[int, int] = (0, 0)


@dataclass
class StageData:
    """
    The class for the stage data
    """
    walls: List[Wall] = field(default_factory=list)
    enemies: List[Tank] = field(default_factory=list)
    player: Tank = field(default_factory=Tank)
    width: int = 0
    height: int = 0
    current_frame: int = 0
    max_frame: int = 0
    bullet_size: int = 2
    tank_size: int = 9
    bullet_speed: int = 7
    tank_speed: int = 3
    player_max_bullet: int = 5
    enemy_max_bullet: int = 3

    def copy(self: "StageData") -> "StageData":
        """
        The function to copy the stage data
        """
        new_walls: List[Wall] = [a.copy() for a in self.walls]
        new_enemies: List[Tank] = [a.copy() for a in self.enemies]
        new_player: Tank = self.player.copy()
        return StageData(new_walls, new_enemies, new_player, self.width,
                         self.height, self.current_frame, self.max_frame,
                         self.bullet_size, self.tank_size, self.bullet_speed,
                         self.tank_speed, self.player_max_bullet,
                         self.enemy_max_bullet)
