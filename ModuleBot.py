"""
The module for the participant
"""


from typing import List, Literal
from random import choice, randint
from math import sqrt
from TankLib import Bullet, Tank, TankAction, StageData


# TODO : Change bots for lvl 9 and 10 (same as lvl 8) and improve others
LAST_MOVE: List[Literal["UP", "DOWN", "LEFT", "RIGHT"]] = []
COUNTER: List[int] = []


def choose_rand_direction(tank: Tank, stage: StageData) -> Literal["UP", "DOWN", "LEFT", "RIGHT"]:
    """
    The function for the direction
    """
    ind: int = stage.enemies.index(tank)

    if len(LAST_MOVE) <= ind:
        LAST_MOVE.append("UP")
        COUNTER.append(0)

    COUNTER[ind] += 1
    if COUNTER[ind] == 20:
        LAST_MOVE[ind] = choice(["UP", "DOWN", "LEFT", "RIGHT"])
        COUNTER[ind] = 0

    return LAST_MOVE[ind]


def get_fastest(tank: Tank, stage: StageData) -> Literal["UP", "DOWN", "LEFT", "RIGHT"]:
    """
    The function to get the fastest way to go to player
    """
    max_dist: tuple[int, int] = (abs(tank.pos_x - stage.player.pos_x), abs(tank.pos_y - stage.player.pos_y))

    if max_dist[0] > max_dist[1]:
        if tank.pos_x < stage.player.pos_x:
            return "RIGHT"
        return "LEFT"

    if tank.pos_y < stage.player.pos_y:
        return "DOWN"

    return "UP"


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


def choose_shooting_direction(tank: Tank, stage: StageData) -> tuple[int, int]:
    """
    The function for the shooting direction
    """
    direction: tuple[int, int] = (stage.player.pos_x - tank.pos_x, stage.player.pos_y - tank.pos_y)

    test: bool = get_walls_colide(Bullet(tank.pos_x, tank.pos_y, direction, stage.bullet_size), (stage.player.pos_x, stage.player.pos_y), stage)

    if not test:
        return direction

    return (0, 0)


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


def destroy_player_bullet(tank: Tank, stage: StageData) -> tuple[int, int]:
    """
    The function to destroy the player's bullet that are near the tank
    """
    player: Tank = stage.player
    shoot_direction: tuple[int, int] = (0, 0)

    direction: tuple[int, int]
    dist: int
    min_dist: int = 100

    for bullet in player.bullets:
        dist = (bullet.pos_x - tank.pos_x)**2 + (bullet.pos_y - tank.pos_y)**2

        if dist < min_dist:
            direction = (bullet.pos_x - tank.pos_x, bullet.pos_y - tank.pos_y)
            if get_tank_collision(bullet, tank, stage):
                min_dist = dist
                shoot_direction = direction

    return shoot_direction


def bot_move_1(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 1 Bot
    """
    action: TankAction = TankAction()
    action.direction = choose_rand_direction(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = (choice([randint(-10, -1), randint(1, 10)]), choice([randint(-10, -1), randint(1, 10)]))
    return action


def bot_move_2(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 2 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = (choice([randint(-10, -1), randint(1, 10)]), choice([randint(-10, -1), randint(1, 10)]))
    return action


def bot_move_3(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 3 Bot
    """
    action: TankAction = TankAction()
    action.direction = choose_rand_direction(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    return action


def bot_move_4(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 4 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    return action


def bot_move_5(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 5 Bot
    """
    action: TankAction = TankAction()
    action.direction = choose_rand_direction(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    return action


def bot_move_6(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 6 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    return action


def bot_move_7(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 7 Bot
    """
    action: TankAction = TankAction()
    action.direction = choose_rand_direction(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets - 1
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    else:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction != (0, 0):
            action.shoot = True
    return action


def bot_move_8(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 8 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets - 1
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    else:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction != (0, 0):
            action.shoot = True
    return action


def bot_move_9(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 9 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets - 1
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    else:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction != (0, 0):
            action.shoot = True
    return action


def bot_move_10(stage: StageData, tank: Tank) -> TankAction:
    """
    Level 10 Bot
    """
    action: TankAction = TankAction()
    action.direction = get_fastest(tank, stage)
    action.shoot = len(tank.bullets) < tank.max_bullets - 1
    if action.shoot:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot_direction = choose_shooting_direction(tank, stage)
        if action.shoot_direction == (0, 0):
            action.shoot = False
    else:
        action.shoot_direction = destroy_player_bullet(tank, stage)
        if action.shoot_direction != (0, 0):
            action.shoot = True
    return action


def bot_move(stage: StageData, tank: Tank, bot: int) -> TankAction:
    """
    The function for the movement
    Need to return a tuple who specify action to do for player's tank
    """
    player_action: TankAction = TankAction()

    match bot:
        case 1:
            player_action = bot_move_1(stage, tank)
        case 2:
            player_action = bot_move_2(stage, tank)
        case 3:
            player_action = bot_move_3(stage, tank)
        case 4:
            player_action = bot_move_4(stage, tank)
        case 5:
            player_action = bot_move_5(stage, tank)
        case 6:
            player_action = bot_move_6(stage, tank)
        case 7:
            player_action = bot_move_7(stage, tank)
        case 8:
            player_action = bot_move_8(stage, tank)
        case 9:
            player_action = bot_move_9(stage, tank)
        case 10:
            player_action = bot_move_10(stage, tank)

    return player_action
