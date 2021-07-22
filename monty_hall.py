import numpy as np

from door import Door
from prompt import prompt

class Monty():
    def __init__(self, options):
        self.total_games = 0
        self.total_wins = 0
        self.always_switch = options["always_switch"] if options["always_switch"] else False
        self.always_stick = options["always_stick"] if options["always_stick"] else False
        self.switch_prompt = True if not self.always_switch and not self.always_stick else False
        self.max_games = options["max_games"] if options["max_games"] else 15
        self.is_random_door = options["is_random_door"] if options["is_random_door"] else False

    def restart_game(self):
        self.doors = [
            Door(),
            Door(),
            Door()
        ]
        self.lucky_door_index = np.random.randint(3)
        self.user_door_index = None
        self.open_door_index = None
        self.doors[self.lucky_door_index].is_lucky = True

    def play(self):
        while self.total_games < self.max_games:
            self.total_games += 1
            self.restart_game()
            self.user_choose_door()
            self.print_doors()
            self.open_one_empty_door()
            self.print_doors()
            if self.switch_prompt:
                is_switch = prompt("Switch?")
            if self.always_switch or (not self.always_stick and is_switch):
                self.switch()
            self.open_all()
            self.print_doors()
            self.record_win_loss()
        self.print_statistics()

    def user_choose_door(self):
        if not self.is_random_door:
            try:
                self.user_door_index = int(input("Choose door (1-3): "))
            except:
                raise ValueError("Invalid door number.")
            if self.user_door_index < 1 or self.user_door_index > 3:
                raise ValueError("Invalid door number.")
        else:
            self.user_door_index = np.random.randint(3)
        self.doors[self.user_door_index].is_user_choice = True

    def open_one_empty_door(self):
        doors_to_open = list(range(3))
        doors_to_open.remove(self.lucky_door_index)
        if self.user_door_index in doors_to_open:
            doors_to_open.remove(self.user_door_index)
        index_to_open = np.random.choice(doors_to_open)
        self.doors[index_to_open].is_open = True
        self.open_door_index = index_to_open

    def open_all(self):
        for door in self.doors:
            door.is_open = True

    def print_doors(self):
        for door in self.doors:
            if door.is_open:
                door_string = "🥳" if door.is_lucky else "😢"
                door_string = "\033[4m" + door_string + "\033[0m" if door.is_user_choice else door_string
                print(door_string, end=" ")
            else:
                door_string = "❓"
                door_string = "\033[4m" + door_string + "\033[0m" if door.is_user_choice else door_string
                print(door_string, end=" ")
        print("\n")

    def switch(self):
        index_to_switch_to = 3 - self.user_door_index - self.open_door_index
        self.doors[index_to_switch_to].is_user_choice = True
        self.doors[self.user_door_index].is_user_choice = False
        self.user_door_index = index_to_switch_to

    def print_statistics(self):
        probability = self.total_wins / self.total_games
        print("%.2f%% win probability\n" % (probability * 100))

    def record_win_loss(self):
        for door in self.doors:
            if door.is_lucky and door.is_user_choice:
                print("YOU WIN :)", end="\n\n")
                self.total_wins += 1
                return True
        print("YOU LOSE :(", end="\n\n")
        return False
