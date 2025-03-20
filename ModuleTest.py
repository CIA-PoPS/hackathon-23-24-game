"""
The module for the participant
"""


from typing import Literal, List, Dict
from random import choice
from math import sqrt
from TankLib import Bullet, Tank, Wall, TankAction, StageData


def get_coordinates(bullet: Bullet, stage: StageData) -> List[tuple[float, float]]:
    """
    Return the coordinates of the bullet for direction during the frame
    """
    coords: List[tuple[float, float]] = []
    x: float = 0
    y: float = 0

    divider: float = sqrt(bullet.direction[0]**2 + bullet.direction[1]**2)
    unit_vector: tuple[float, float] = (bullet.direction[0] / divider, bullet.direction[1] / divider)

    while x**2 + y**2 < stage.bullet_speed**2:
        coords.append((bullet.pos_x + x, bullet.pos_y + y))

        x += unit_vector[0]
        y += unit_vector[1]

    return coords


def bullet_collision(is_player: bool, bullet: Bullet, coord: tuple[float, float], stage: StageData) -> Bullet | Tank | Wall | None:
    """
    Return what the bullet collide with if it's a tank or a bullet
    """
    for wall in stage.walls:
        if wall.is_in_wall(coord[0], coord[1], bullet.size, bullet.size):
            return wall

    if is_player:
        for enemy in stage.enemies:
            if enemy.is_in_tank(coord[0], coord[1], bullet.size, bullet.size) and enemy.is_alive:
                return enemy
            for enemy_bullet in enemy.bullets:
                if enemy_bullet.is_in_bullet(coord[0], coord[1], bullet.size, bullet.size):
                    return enemy_bullet
    else:
        if stage.player.is_in_tank(coord[0], coord[1], bullet.size, bullet.size):
            return stage.player
        for player_bullet in stage.player.bullets:
            if player_bullet.is_in_bullet(coord[0], coord[1], bullet.size, bullet.size):
                return player_bullet

    return None


def check_move(direction: Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"], tank: Tank, stage: StageData) -> int:
    """
    Check if the move is valid
    """
    vector: tuple[int, int] = (0, 0)
    new_pos: tuple[int, int]

    match direction:
        case "UP":
            vector = (0, -1)
        case "DOWN":
            vector = (0, 1)
        case "LEFT":
            vector = (-1, 0)
        case "RIGHT":
            vector = (1, 0)

    for i in range(1, stage.tank_speed + 1):
        new_pos = (tank.pos_x + i*vector[0], tank.pos_y + i*vector[1])

        if new_pos[0] - tank.size < 0 or new_pos[0] + tank.size > stage.width:
            return i - 1
        if new_pos[1] - tank.size < 0 or new_pos[1] + tank.size > stage.height:
            return i - 1

        for wall in stage.walls:
            if wall.is_in_wall(new_pos[0], new_pos[1], tank.size, tank.size):
                return i - 1

        for enemy in stage.enemies:
            if enemy.is_alive:
                if enemy.is_in_tank(new_pos[0], new_pos[1], tank.size, tank.size):
                    return i - 1
                for bullet in enemy.bullets:
                    if bullet.is_in_bullet(new_pos[0], new_pos[1],
                                           tank.size, tank.size):
                        return i - 1

    return stage.tank_speed


def make_move(tank: Tank, stage: StageData) -> Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"]:
    """
    Make the move specified in args for tank
    """
    distance: Dict[Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"], int] = {
        "UP": check_move("UP", tank, stage),
        "DOWN": check_move("DOWN", tank, stage),
        "LEFT": check_move("LEFT", tank, stage),
        "RIGHT": check_move("RIGHT", tank, stage),
        "NONE": 1
    }
    maximum: int = 0
    result: Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"] = "NONE"
    for key, value in distance.items():
        if value > maximum:
            result = key
            maximum = value
    return result


def get_walls_colide(bullet: Bullet, final: tuple[int, int], stage: StageData) -> bool:
    """
    Return if the bullet colide with a wall
    """
    x: float = bullet.pos_x
    y: float = bullet.pos_y

    divider: float = sqrt(bullet.direction[0]**2 + bullet.direction[1]**2)
    unit_vector: tuple[float, float] = (bullet.direction[0] / divider, bullet.direction[1] / divider)

    checker_x: bool = final[0] > x if unit_vector[0] > 0 else final[0] < x
    checker_y: bool = final[1] > y if unit_vector[1] > 0 else final[1] < y

    while checker_x or checker_y:
        if any(a_wall.is_in_wall(x, y, bullet.size, bullet.size) for a_wall in stage.walls):
            return True

        if x < 0 or x > stage.width or y < 0 or y > stage.height:
            return True

        x += unit_vector[0]
        y += unit_vector[1]

        checker_x = final[0] > x if unit_vector[0] > 0 else final[0] < x
        checker_y = final[1] > y if unit_vector[1] > 0 else final[1] < y

    return False


def choose_shooting_direction(stage: StageData) -> tuple[int, int]:
    """
    The function for the shooting direction
    """
    pos_x: int = stage.player.pos_x
    pos_y: int = stage.player.pos_y
    min_dist: int = -1
    shoot_direction: tuple[int, int] = (0, 0)

    dist: int
    direction: tuple[int, int]
    test: bool

    for tank in stage.enemies:
        if not tank.is_alive:
            continue
        dist = (tank.pos_x - pos_x) ** 2 + (tank.pos_y - pos_y) ** 2

        if min_dist == -1 or dist < min_dist:
            direction = (tank.pos_x - pos_x, tank.pos_y - pos_y)
            test = get_walls_colide(Bullet(pos_x, pos_y, direction, stage.bullet_size), (tank.pos_x, tank.pos_y), stage)

            if not test:
                min_dist = dist
                shoot_direction = direction

    return shoot_direction


def get_tank_collision(bullet: Bullet, tank: Tank, stage: StageData) -> bool:
    """
    Return if the bullet colide with the tank
    """
    x: float = bullet.pos_x
    y: float = bullet.pos_y

    divider: float = sqrt(bullet.direction[0]**2 + bullet.direction[1]**2)
    unit_vector: tuple[float, float] = (bullet.direction[0] / divider, bullet.direction[1] / divider)

    while True:
        if any(a_wall.is_in_wall(x, y, bullet.size, bullet.size) for a_wall in stage.walls):
            return False

        if x < 0 or x > stage.width or y < 0 or y > stage.height:
            return False

        if tank.is_in_tank(x, y, bullet.size, bullet.size):
            return True

        x += unit_vector[0]
        y += unit_vector[1]


def destroy_bullet(stage: StageData) -> tuple[int, int]:
    """
    The function to destroy the enemy's bullet that are near the tank
    """
    player: Tank = stage.player
    shoot_direction: tuple[int, int] = (0, 0)

    direction: tuple[int, int]
    dist: int
    min_dist: int = 100

    for enemy in stage.enemies:
        for bullet in enemy.bullets:
            dist = (bullet.pos_x - player.pos_x)**2 + (bullet.pos_y - player.pos_y)**2

            if dist < min_dist:
                direction = (bullet.pos_x - player.pos_x, bullet.pos_y - player.pos_y)
                if get_tank_collision(bullet, player, stage):
                    min_dist = dist
                    shoot_direction = direction

    return shoot_direction


def move(stage: StageData) -> TankAction:
    """
    The function for the movement
    Need to return a tuple who specify action to do for player's tank
    """
    player_action: TankAction = TankAction()

    player_action.direction = choice(["UP", "DOWN", "LEFT", "RIGHT", "NONE"])

    player_action.shoot = len(stage.player.bullets) < stage.player.max_bullets - 2

    if player_action.shoot:
        player_action.shoot_direction = destroy_bullet(stage)
        if player_action.shoot_direction == (0, 0):
            player_action.shoot_direction = choose_shooting_direction(stage)
        if player_action.shoot_direction == (0, 0):
            player_action.shoot = False
    else:
        player_action.shoot_direction = destroy_bullet(stage)
        if player_action.shoot_direction != (0, 0):
            player_action.shoot = True

    return player_action
