import argparse
import numpy as np

from monty_hall import Monty

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-sw', '--switch',      action='store_true', help="always switch")
    parser.add_argument('-st', '--stick',       action='store_true', help="always stick")
    parser.add_argument('-r',  '--random-door', action='store_true', help="pick random door")
    parser.add_argument('-n',  '--number',      type=int,            help="run simulation N times")
    args = parser.parse_args()

    if args.number is not None and args.number <= 0:
        parser.error("Argument --number must be positive")

    monty = Monty({
        "always_switch" : args.switch,
        "always_stick" : args.stick,
        "max_games" : args.number,
        "is_random_door": args.random_door
    })
    monty.play()
