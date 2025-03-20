"""
Make stage file
"""


from os import makedirs, path
from random import randint
from typing import List
from math import ceil
from TankLib import Wall, Tank
from ModuleGame import TANK_SIZE


PATH: str = path.dirname(path.abspath(__file__))
STAGE_DIR: str = f"{PATH}/stages"
LIST_NAME: list[str] = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]


def check_wall_in_walls(x: int, y: int, size_x: int, size_y: int, walls: list[Wall]) -> bool:
    """
    Check if a wall collides with walls from a list
    """
    for wall in walls:
        if wall.is_in_wall(x, y, size_x, size_y):
            return True
    return False


def generate_stage(i: int) -> None:
    """
    Generate a stage
    """
    walls: List[Wall] = []
    player: Tank = Tank()
    enemies: List[Tank] = []
    width: int = randint(450, 800)
    height: int = randint(450, 650)
    nb_walls: int = randint(3, 15)
    nb_enemies: int
    x: int
    y: int
    size_x: int
    size_y: int

    nb_enemies = ceil(i % 10 / 2)
    if nb_enemies == 0:
        nb_enemies = 5

    if i == 100:
        width = 800
        height = 650
        nb_walls = 10
        nb_enemies = 7

    while len(walls) < nb_walls:
        size_x = randint(75 // nb_walls, round(width / (nb_walls * 1.5)))
        size_y = randint(75 // nb_walls, round(height / (nb_walls * 1.5)))
        x = randint(size_x, width - size_x)
        y = randint(size_y, height - size_y)
        if size_x * size_y < width * height / (nb_walls * 4):
            if not check_wall_in_walls(x, y, size_x, size_y, walls):
                walls.append(Wall(x, y, size_x, size_y))

    while True:
        x = randint(TANK_SIZE + 1, width - TANK_SIZE - 1)
        y = randint(TANK_SIZE + 1, height - TANK_SIZE - 1)
        if not any(wall.is_in_wall(x, y, TANK_SIZE, TANK_SIZE) for wall in walls):
            player.pos_x = x
            player.pos_y = y
            break

    while len(enemies) < nb_enemies:
        x = randint(TANK_SIZE + 1, width - TANK_SIZE - 1)
        y = randint(TANK_SIZE + 1, height - TANK_SIZE - 1)
        if not any(wall.is_in_wall(x, y, TANK_SIZE, TANK_SIZE) for wall in walls) and not any(enemy.is_in_tank(x, y, TANK_SIZE, TANK_SIZE) for enemy in enemies) and not player.is_in_tank(x, y, TANK_SIZE * 11, TANK_SIZE * 11):
            enemies.append(Tank(LIST_NAME[0], x, y, TANK_SIZE))
            LIST_NAME.append(LIST_NAME.pop(0))

    with open(f"{STAGE_DIR}/stage_{i}.in", "w", encoding="iso8859") as file:
        file.write(f"Dimension: {width} {height}\n")
        file.write(f"Bot: {((i - 1) // 10) + 1}\n")
        for wall in walls:
            file.write(f"Wall: {wall.pos_x} {wall.pos_y} {wall.size_x} {wall.size_y}\n")
        file.write(f"Player: {player.pos_x} {player.pos_y}\n")
        for enemy in enemies:
            file.write(f"Enemy: {enemy.name} {enemy.pos_x} {enemy.pos_y}\n")


if __name__ == "__main__":
    makedirs(STAGE_DIR, exist_ok=True)
    for ind in range(1, 101):
        generate_stage(ind)
