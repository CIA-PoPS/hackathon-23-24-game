"""
The Main file of the game
"""


from os import path, makedirs
from typing import List, Literal
from math import sqrt
from TankLib import Wall, Bullet, Tank, TankAction, StageData
import ModuleBot
import ModulePlayer


NB_FRAME: int = 1000
BULLET_SIZE: int = 2
TANK_SIZE: int = 9
BULLET_SPEED: int = 10
TANK_SPEED: int = 3
PLAYER_MAX_BULLET: int = 5
ENEMY_MAX_BULLET: int = 3
BOT: int = 1
PATH: str = path.dirname(path.abspath(__file__))


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
            if enemy != tank and enemy.is_alive and enemy.is_in_tank(new_pos[0], new_pos[1], tank.size, tank.size):
                return i - 1

        if stage.player != tank and stage.player.is_in_tank(new_pos[0], new_pos[1], tank.size, tank.size):
            return i - 1

    return stage.tank_speed


def make_move(direction: Literal["UP", "DOWN", "LEFT", "RIGHT", "NONE"], tank: Tank, stage: StageData) -> None:
    """
    Make the move specified in args for tank
    """
    distance: int = check_move(direction, tank, stage)
    match direction:
        case "UP":
            tank.pos_y -= distance
        case "DOWN":
            tank.pos_y += distance
        case "LEFT":
            tank.pos_x -= distance
        case "RIGHT":
            tank.pos_x += distance


def make_shoot(shoot: bool, direction: tuple[int, int], tank: Tank, stage: StageData) -> None:
    """
    Make the shoot specified in args for tank
    """
    if shoot and len(tank.bullets) < tank.max_bullets and direction != (0, 0):
        bullet: Bullet = Bullet(tank.pos_x, tank.pos_y, direction, stage.bullet_size)
        tank.bullets.append(bullet)


def actualize_tanks(stage: StageData) -> None:
    """
    Actualize the tanks
    """
    action: TankAction

    for enemy in stage.enemies:
        if enemy.is_alive:
            action = ModuleBot.bot_move(stage.copy(), enemy.copy(), BOT)
            make_move(action.direction, enemy, stage)
            make_shoot(action.shoot, action.shoot_direction, enemy, stage)

    if stage.player.is_alive:
        action = ModulePlayer.move(stage.copy())
        make_move(action.direction, stage.player, stage)
        make_shoot(action.shoot, action.shoot_direction, stage.player, stage)


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


def bullet_moves(is_player: bool, bullet: Bullet, stage: StageData) -> Bullet | Tank | Wall | None:
    """
    Return what the bullet collide with
    """
    coords: List[tuple[float, float]] = get_coordinates(bullet, stage)
    collision: Bullet | Tank | Wall | None
    for coord in coords:
        if coord[0] - bullet.size < 0 or \
           coord[0] + bullet.size > stage.width or \
           coord[1] - bullet.size < 0 or \
           coord[1] + bullet.size > stage.height:
            return Wall()

        collision = bullet_collision(is_player, bullet, coord, stage)

        if collision is not None:
            return collision

    bullet.pos_x = round(coords[-1][0])
    bullet.pos_y = round(coords[-1][1])
    return None


def bullet_destruct(bullet: Bullet, tank: Tank, stage: StageData, collision: Bullet | Tank | Wall, special: List[str]) -> None:
    """
    Destruct the bullet
    """
    tank.bullets.remove(bullet)

    if isinstance(collision, Bullet):
        if collision in stage.player.bullets:
            stage.player.bullets.remove(collision)
        else:
            for enemy in stage.enemies:
                if collision in enemy.bullets:
                    enemy.bullets.remove(collision)
                    break

    if isinstance(collision, Tank):
        collision.is_alive = False
        special.append(f"Death: {collision.name}")


def actualize_bullets(stage: StageData, special: List[str]) -> None:
    """
    Actualize the bullets
    """
    collision: Bullet | Tank | Wall | None

    for bullet in stage.player.bullets:
        collision = bullet_moves(True, bullet, stage)

        if collision is not None:
            bullet_destruct(bullet, stage.player, stage, collision, special)

    for enemy in stage.enemies:
        for bullet in enemy.bullets:
            collision = bullet_moves(False, bullet, stage)

            if collision is not None:
                bullet_destruct(bullet, enemy, stage, collision, special)


def print_log(stage: StageData, log_file: str, special: List[str]) -> None:
    """
    Print the log of the stage
    """
    with open(log_file, "a", encoding="iso8859") as f:
        f.write(f"Frame: {stage.current_frame}\n")

        if stage.player.is_alive:
            f.write(f"Player: {stage.player.pos_x} {stage.player.pos_y}\n")
        else:
            f.write("Player: -100 -100\n")

        for enemy in stage.enemies:
            if enemy.is_alive:
                f.write(f"Enemy: {enemy.name} {enemy.pos_x} {enemy.pos_y}\n")

        for bullet in stage.player.bullets:
            f.write(f"Player_Bullet: {bullet.pos_x} {bullet.pos_y}\n")

        for enemy in stage.enemies:
            for bullet in enemy.bullets:
                f.write(f"Enemy_Bullet: {bullet.pos_x} {bullet.pos_y}\n")

        for spec in special:
            f.write(f"{spec}\n")

        f.write("---------------------------------\n")


def get_stage_data(file: str) -> StageData:
    """
    Get the stage data
    """
    global BOT

    with open(file, "r", encoding="iso8859") as f:
        lines: List[str] = f.readlines()

    stage: StageData = StageData([], [], Tank(), 0, 0, 0, NB_FRAME,
                                 BULLET_SIZE, TANK_SIZE, BULLET_SPEED,
                                 TANK_SPEED, PLAYER_MAX_BULLET,
                                 ENEMY_MAX_BULLET)
    data: List[str]

    for line in lines:
        data = line.split()

        match data[0]:
            case "Dimension:":
                stage.width = int(data[1])
                stage.height = int(data[2])
            case "Wall:":
                stage.walls.append(Wall(int(data[1]), int(data[2]), int(data[3]), int(data[4])))
            case "Player:":
                stage.player.is_alive = True
                stage.player.name = "Player"
                stage.player.pos_x = int(data[1])
                stage.player.pos_y = int(data[2])
                stage.player.size = stage.tank_size
                stage.player.max_bullets = stage.player_max_bullet
                stage.player.bullets = []
            case "Enemy:":
                stage.enemies.append(Tank(True, data[1], int(data[2]), int(data[3]), stage.tank_size, stage.enemy_max_bullet, []))
            case "Bot:":
                BOT = int(data[1])

    return stage


def check_end(stage: StageData) -> bool:
    """
    Check if the game is finished
    """
    if not stage.player.is_alive:
        return True
    if not any(enemy.is_alive for enemy in stage.enemies):
        return True
    if stage.current_frame > stage.max_frame:
        return True
    return False


def main(stage_nb: int) -> str:
    """
    The main function of the game
    """
    stage_dir: str = f"{PATH}/stages"
    stage_file: str = f"{stage_dir}/stage_{stage_nb}.in"
    log_file: str = f"{PATH}/logs/stage_{stage_nb}.log"
    special_action: List[str] = []

    makedirs(f"{PATH}/logs", exist_ok=True)

    if not path.isfile(stage_file):
        return "Stage not found"

    stage_data: StageData = get_stage_data(stage_file)

    with open(log_file, "w", encoding="iso8859") as file:
        file.write(f"Dimension: {stage_data.width} {stage_data.height}\n")
        file.write(f"TankSize: {TANK_SIZE}\n")
        file.write(f"BulletSize: {BULLET_SIZE}\n")
        for wall in stage_data.walls:
            file.write(f"Wall: {wall.pos_x} {wall.pos_y} {wall.size_x} "
                       f"{wall.size_y}\n")
        file.write("---------------------------------\n")

    finished: bool = False

    while not finished:
        for enemy in stage_data.enemies:
            if not enemy.is_alive and not enemy.bullets:
                stage_data.enemies.remove(enemy)
        actualize_tanks(stage_data)
        actualize_bullets(stage_data, special_action)
        print_log(stage_data, log_file, special_action)
        stage_data.current_frame += 1
        special_action.clear()
        finished = check_end(stage_data)

    result: str = "GAME OVER"

    if stage_data.current_frame > stage_data.max_frame:
        result = "TIE"
    elif stage_data.player.is_alive:
        result = "WINNER"

    with open(log_file, "a", encoding="iso8859") as file:
        file.write(f"Result: {result}\n")
    return result


if __name__ == "__main__":
    for STAGE_INDEX in range(1, 101):
        try:
            RESULT = main(STAGE_INDEX)
        except Exception as e:
            RESULT = f"Error: {e}"
        with open(f"{PATH}/logs/all.log", "a", encoding="iso8859") as f:
            f.write(f"Stage {STAGE_INDEX}: {RESULT}\n")
