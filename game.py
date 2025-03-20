"""
The main file of the game
"""


from os import path
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from argparse import ArgumentParser, Namespace
from typing import Dict
from collections import OrderedDict
from time import perf_counter_ns
import ModuleGenerator
import ModuleDisplay


PATH: str = path.dirname(path.abspath(__file__))


def main() -> None:
    """
    The main function for executing all stages of the game
    """
    command: str = f"python3 {PATH}/ModuleGame.py -stage "
    all_logs_file: str = f"{PATH}/logs/all.log"

    processes: Dict[int, Popen] = {}
    results: OrderedDict[int, str] = OrderedDict()
    start: int = perf_counter_ns()

    for index in range(1, 101):
        process = Popen(command + str(index), shell=True, stdout=PIPE, stderr=STDOUT, encoding="iso8859", errors="ignore")
        processes[index] = process

    for key, process in processes.items():
        try:
            process.wait(timeout=45)
            if process.stdout is not None:
                results[key] = process.stdout.read().strip()
        except TimeoutExpired:
            process.kill()
            results[key] = "TIME OUT"

    results = OrderedDict(sorted(results.items(), key=lambda x: x[0]))

    result: str
    res_dict: Dict[str, int] = {"WINNER": 0, "TIE": 0, "GAME OVER": 0, "ERROR": 0}

    for key, result in results.items():
        with open(all_logs_file, "a", encoding="iso8859") as file:
            file.write(f"Stage {key}: {result}\n")
        try:
            res_dict[result] += 1
        except KeyError:
            res_dict["ERROR"] += 1

    print(f"Time: {round((perf_counter_ns() - start) * 10**-9, 3)} seconds")

    with open(all_logs_file, "a", encoding="iso8859") as file:
        for a, b in res_dict.items():
            file.write(f"{a}: {b}\n")


def backup_original_stages() -> None:
    """
    Backup the original stages
    """
    for index in range(1, 101):
        text: str = ""
        with open(f"{PATH}/original_stages.bak/stage_{index}.in", "r", encoding="iso8859") as file:
            text = file.read()
        with open(f"{PATH}/stages/stage_{index}.in", "w", encoding="iso8859") as file:
            file.write(text)


if __name__ == "__main__":
    PARSER: ArgumentParser = ArgumentParser()
    PARSER.add_argument("--original", type=bool, default=False, help="If True, get original stages")
    PARSER.add_argument("--generate", type=bool, default=False, help="If True, generate new stages")
    PARSER.add_argument("--display", type=bool, default=False, help="If True, display games after completion")
    ARGS: Namespace = PARSER.parse_known_args()[0]

    if ARGS.original:
        backup_original_stages()
    elif ARGS.generate:
        for i in range(1, 101):
            ModuleGenerator.generate_stage(i)

    main()

    if ARGS.display:
        ModuleDisplay.main()
