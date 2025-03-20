"""
The module for the display of the game
"""


import tkinter as tk
from os import path
from functools import partial
from time import sleep
from typing import List, Dict, Any
from re import Match, Pattern
from re import compile as cmp


WINNER_MSG: str = "WINNER"
GAME_OVER_MSG: str = "GAME OVER"
TIE_MSG: str = "TIE"
TIME_OUT_MSG: str = "TIME OUT"
ERROR_MSG: str = "Error occured"

WINDOW: tk.Tk = tk.Tk()
WINDOW.title("Battle City")
WINDOW.geometry("1200x700")
WINDOW.resizable(False, False)

CANVAS: tk.Canvas = tk.Canvas(WINDOW, width=1200, height=700, bg="black")
CANVAS.place(x=0, y=0, anchor="nw")

RES_WIN: tk.Label = tk.Label(WINDOW, text=f"{WINNER_MSG}: 000", bg="green")
RES_WIN.place(x=850, y=25, anchor="nw")
RES_OVER: tk.Label = tk.Label(WINDOW, text=f"{GAME_OVER_MSG}: 000", bg="red")
RES_OVER.place(x=1037, y=25, anchor="n")
RES_TIE: tk.Label = tk.Label(WINDOW, text=f"{TIE_MSG}: 000", bg="orange")
RES_TIE.place(x=1195, y=25, anchor="ne")

LGD_WIN: tk.Label = tk.Label(WINDOW, text=WINNER_MSG, bg="green")
LGD_WIN.place(x=850, y=660, anchor="sw")
LGD_OVER: tk.Label = tk.Label(WINDOW, text=GAME_OVER_MSG, bg="red")
LGD_OVER.place(x=910, y=660, anchor="sw")
LGD_TIE: tk.Label = tk.Label(WINDOW, text=TIE_MSG, bg="orange")
LGD_TIE.place(x=990, y=660, anchor="sw")
LGD_TIME_OUT: tk.Label = tk.Label(WINDOW, text=TIME_OUT_MSG, bg="blue")
LGD_TIME_OUT.place(x=850, y=690, anchor="sw")
LGD_ERROR: tk.Label = tk.Label(WINDOW, text=ERROR_MSG, bg="purple")
LGD_ERROR.place(x=920, y=690, anchor="sw")

EXIT: tk.Button = tk.Button(WINDOW, text="Quit", command=WINDOW.destroy)
EXIT.place(x=1190, y=690, anchor="se")

GAME: tk.Canvas = tk.Canvas(WINDOW, width=800, height=650, bg="white")
GAME.place(x=25, y=25, anchor="nw")

BUTTONS: List[tk.Button] = []
ACTUAL_STAGE: int = 0
TANK_SIZE: int = 0
BULLET_SIZE: int = 0
FONT: str = "Arial 10"

PATH: str = path.dirname(path.abspath(__file__))


def destroy_object(obj: tk.Misc) -> None:
    """
    Destroy the object
    """
    try:
        obj.destroy()
    except tk.TclError:
        pass


def reset_globals() -> None:
    """
    Reset the global variables
    """
    global WINNER_MSG, GAME_OVER_MSG, TIE_MSG, TIME_OUT_MSG, ERROR_MSG, \
        WINDOW, CANVAS, RES_WIN, RES_OVER, RES_TIE, LGD_WIN, LGD_OVER, \
        LGD_TIE, LGD_TIME_OUT, LGD_ERROR, EXIT, BUTTONS, GAME, ACTUAL_STAGE, \
        TANK_SIZE, BULLET_SIZE, FONT

    WINNER_MSG = "WINNER"
    GAME_OVER_MSG = "GAME OVER"
    TIE_MSG = "TIE"
    TIME_OUT_MSG = "TIME OUT"
    ERROR_MSG = "Error occured"

    obj: tk.Misc

    for obj in [WINDOW, CANVAS, RES_WIN, RES_OVER, RES_TIE, LGD_WIN, LGD_OVER, LGD_TIE, LGD_TIME_OUT, LGD_ERROR, EXIT, GAME]:
        destroy_object(obj)

    for button in BUTTONS:
        destroy_object(button)

    WINDOW = tk.Tk()
    WINDOW.title("Battle City")
    WINDOW.geometry("1200x700")
    WINDOW.resizable(False, False)

    CANVAS = tk.Canvas(WINDOW, width=1200, height=700, bg="black")
    CANVAS.place(x=0, y=0, anchor="nw")

    RES_WIN = tk.Label(WINDOW, text=f"{WINNER_MSG}: 000", bg="green")
    RES_WIN.place(x=850, y=25, anchor="nw")
    RES_OVER = tk.Label(WINDOW, text=f"{GAME_OVER_MSG}: 000", bg="red")
    RES_OVER.place(x=1037, y=25, anchor="n")
    RES_TIE = tk.Label(WINDOW, text=f"{TIE_MSG}: 000", bg="orange")
    RES_TIE.place(x=1195, y=25, anchor="ne")

    LGD_WIN = tk.Label(WINDOW, text=WINNER_MSG, bg="green")
    LGD_WIN.place(x=850, y=660, anchor="sw")
    LGD_OVER = tk.Label(WINDOW, text=GAME_OVER_MSG, bg="red")
    LGD_OVER.place(x=910, y=660, anchor="sw")
    LGD_TIE = tk.Label(WINDOW, text=TIE_MSG, bg="orange")
    LGD_TIE.place(x=990, y=660, anchor="sw")
    LGD_TIME_OUT = tk.Label(WINDOW, text=TIME_OUT_MSG, bg="blue")
    LGD_TIME_OUT.place(x=850, y=690, anchor="sw")
    LGD_ERROR = tk.Label(WINDOW, text=ERROR_MSG, bg="purple")
    LGD_ERROR.place(x=920, y=690, anchor="sw")

    EXIT = tk.Button(WINDOW, text="Quit", command=WINDOW.destroy)
    EXIT.place(x=1190, y=690, anchor="se")

    GAME = tk.Canvas(WINDOW, width=800, height=650, bg="white")
    GAME.place(x=25, y=25, anchor="nw")

    BUTTONS = []
    ACTUAL_STAGE = 0
    TANK_SIZE = 0
    BULLET_SIZE = 0
    FONT = "Arial 10"


def parse_stage_result(stage: int, result: str) -> List[str]:
    """
    Parse the stage result log's file to get the coordinates of the walls,
    dimensions and every mooves
    """
    global TANK_SIZE, BULLET_SIZE

    if result not in [TIE_MSG, GAME_OVER_MSG, WINNER_MSG] or \
       not path.isfile(f"{PATH}/logs/stage_{stage}.log"):
        if ACTUAL_STAGE == stage:
            error_msg: str
            if result == TIME_OUT_MSG:
                error_msg = TIME_OUT_MSG + ", ask an admin"
            else:
                error_msg = f"\n\n{ERROR_MSG}\nAsk an admin for logs\n\nAnd don't forget to give the stage number\nAnd your team name"
            GAME.config(width=775, height=625)
            GAME.create_text(10, 30, text="Result: Error: " + error_msg, fill="purple", font=FONT, anchor="nw")
        return []

    with open(f"{PATH}/logs/stage_{stage}.log", "r", encoding="iso8859") as file:
        text: str = file.read()

    dim: Match[str] | None = cmp(r"Dimension: (?P<width>\d+) (?P<height>\d+)").search(text)

    tank_size: Match[str] | None = cmp(r"TankSize: (?P<size>\d+)").search(text)
    bullet_size: Match[str] | None = cmp(r"BulletSize: (?P<size>\d+)").search(text)

    if tank_size and ACTUAL_STAGE == stage:
        TANK_SIZE = int(tank_size.group("size"))
    if bullet_size and ACTUAL_STAGE == stage:
        BULLET_SIZE = int(bullet_size.group("size"))

    if dim and ACTUAL_STAGE == stage:
        GAME.config(width=int(dim.group("width")), height=int(dim.group("height")))
    elif ACTUAL_STAGE == stage:
        GAME.config(width=775, height=625)

    walls: List[Match[str]] = list(cmp(r"Wall: (?P<x>\d+) (?P<y>\d+) (?P<size_x>\d+) (?P<size_y>\d+)").finditer(text))

    for wall in walls:
        if ACTUAL_STAGE == stage:
            GAME.create_rectangle(int(wall.group("x")) - int(wall.group("size_x")),
                                  int(wall.group("y")) - int(wall.group("size_y")),
                                  int(wall.group("x")) + int(wall.group("size_x")),
                                  int(wall.group("y")) + int(wall.group("size_y")),
                                  fill="green")

    if ACTUAL_STAGE == stage:
        GAME.create_text(10, 30, text=f"Result: {result}", fill="purple", font=FONT, anchor="nw")

    return text.split("\n")


def parse_mooves(frames: List[Dict], lines: List[str]) -> None:
    """
    Parse every mooves of the stage and put them in frames
    """
    i: int = 0

    while i < len(lines):
        line: str = lines[i]

        if line.startswith("Frame:"):
            frame_dict: Dict[str, Any] = {}
            frame_dict["frame"] = int(line.split()[1])
            frame_dict["player"] = []
            frame_dict["enemies"] = []
            frame_dict["player_bullet"] = []
            frame_dict["enemy_bullet"] = []

            i += 1
            try:
                line = lines[i]
            except IndexError:
                break

            while line != "---------------------------------":
                if line.startswith("Player:"):
                    frame_dict["player"] = line.split()[1:]
                elif line.startswith("Enemy:"):
                    frame_dict["enemies"].append(line.split()[1:])
                elif line.startswith("Player_Bullet:"):
                    frame_dict["player_bullet"].append(line.split()[1:])
                elif line.startswith("Enemy_Bullet:"):
                    frame_dict["enemy_bullet"].append(line.split()[1:])

                i += 1
                try:
                    line = lines[i]
                except IndexError:
                    break

            frames.append(frame_dict)

        i += 1


def stage_display(stage: int, result: str) -> None:
    """
    Display the stage
    """
    global ACTUAL_STAGE
    ACTUAL_STAGE = stage
    GAME.delete("all")

    splited_text: List[str] = parse_stage_result(stage, result)

    if ACTUAL_STAGE == stage:
        GAME.update()

    frames: List[Dict] = []
    parse_mooves(frames, splited_text)

    all_items: List[int] = []
    for frame in frames:
        if ACTUAL_STAGE != stage:
            break

        for item in all_items:
            GAME.delete(item)

        all_items = []

        if ACTUAL_STAGE == stage:
            all_items.append(GAME.create_text(10, 10, text=f"Time: {frame['frame']/10}s", fill="purple", font=FONT, anchor="nw"))

            all_items.append(GAME.create_rectangle(int(frame["player"][0]) - TANK_SIZE,
                                                   int(frame["player"][1]) - TANK_SIZE,
                                                   int(frame["player"][0]) + TANK_SIZE,
                                                   int(frame["player"][1]) + TANK_SIZE,
                                                   fill="blue"))

        for enemy in frame["enemies"]:
            if ACTUAL_STAGE != stage:
                break
            all_items.append(GAME.create_rectangle(int(enemy[1]) - TANK_SIZE,
                                                   int(enemy[2]) - TANK_SIZE,
                                                   int(enemy[1]) + TANK_SIZE,
                                                   int(enemy[2]) + TANK_SIZE,
                                                   fill="red"))

        for bullet in frame["player_bullet"]:
            if ACTUAL_STAGE != stage:
                break
            all_items.append(GAME.create_rectangle(int(bullet[0]) - BULLET_SIZE,
                                                   int(bullet[1]) - BULLET_SIZE,
                                                   int(bullet[0]) + BULLET_SIZE,
                                                   int(bullet[1]) + BULLET_SIZE,
                                                   fill="blue"))

        for bullet in frame["enemy_bullet"]:
            if ACTUAL_STAGE != stage:
                break
            all_items.append(GAME.create_rectangle(int(bullet[0]) - BULLET_SIZE,
                                                   int(bullet[1]) - BULLET_SIZE,
                                                   int(bullet[0]) + BULLET_SIZE,
                                                   int(bullet[1]) + BULLET_SIZE,
                                                   fill="red"))

        if ACTUAL_STAGE == stage:
            GAME.update()
        sleep(0.1)


def choose_color(result: str) -> str:
    """
    Choose the color of the result
    """
    if result == WINNER_MSG:
        return "green"
    if result == GAME_OVER_MSG:
        return "red"
    if result == TIE_MSG:
        return "orange"
    if result == TIME_OUT_MSG:
        return "blue"
    return "purple"


def main_preset() -> None:
    """
    Set everything up
    """
    try:
        with open(f"{PATH}/logs/all.log", "r", encoding="iso8859") as file:
            stage_res_tmp: List[str] = file.read().split("\n")
    except OSError:
        error_msg: str = "No logs find for your team"
        GAME.config(width=775, height=625)
        GAME.create_text(10, 30, text="Result: Error: " + error_msg, fill="purple", font=FONT, anchor="nw")
        return

    stage_res_mess: List[str] = []
    pattern: Pattern = cmp(r"Stage (?P<nb>\d+): (?P<res>[^\n]*)")
    ind: int = 0
    line: str
    matched: Match[str] | None
    dict_res: Dict[str, str]
    number: int
    res: str

    while ind < len(stage_res_tmp):
        line = stage_res_tmp[ind]
        matched = pattern.search(line)

        if matched:
            dict_res = matched.groupdict()
            number = int(dict_res.get("nb", "0"))
            res = dict_res.get("res", "")

            while len(stage_res_mess) < number + 1:
                stage_res_mess.append("")
            stage_res_mess[number] = res.strip()

        ind += 1

    stage_res_color: List[str] = [choose_color(res) for res in stage_res_mess]

    nb_win: str = str(stage_res_color.count("green"))
    nb_over: str = str(stage_res_color.count("red"))
    nb_tie: str = str(stage_res_color.count("orange"))
    RES_WIN.config(text=f"{WINNER_MSG}: " + "0"*(3-len(str(nb_win))) + nb_win)
    RES_OVER.config(text=f"{GAME_OVER_MSG}: " + "0"*(3-len(str(nb_over))) + nb_over)
    RES_TIE.config(text=f"{TIE_MSG}: " + "0"*(3-len(str(nb_tie))) + nb_tie)

    for ind in range(1, len(stage_res_mess)):
        BUTTONS.append(tk.Button(WINDOW, text=ind, bg=stage_res_color[ind], command=partial(stage_display, ind, stage_res_mess[ind])))

    for ind, button in enumerate(BUTTONS):
        button.place(x=850 + (ind % 10) * 35, y=60 + (ind//10) * 35, anchor="nw")


def main() -> None:
    """
    Main function
    """
    reset_globals()
    main_preset()
    WINDOW.mainloop()


if __name__ == "__main__":
    main()
