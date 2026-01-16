import time
import random
import itertools

def show_creator():
    print("""
Abram Jindal is the creator of this code.
He created it because whenever he would
make a python game, he always manually
made the code for printing text in
different ways. This was tiring, so
after he learned to create his own
libraries he decided to make one that
prints text in different ways so next
time he is making a python game, he
doesn't need to manually make the code.
I hope you found this module useful to you.
""")    

def typewriter(text, speed=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()

def boxed(text):
    length = len(text) + 2
    print("+" + "-" * length + "+")
    print("| " + text + " |")
    print("+" + "-" * length + "+")

def rainbow(text, speed=0.03):
    colors = {
        "red": "\033[31m",
        "orange": "\033[93m",
        "yellow": "\033[33m",
        "green": "\033[32m",
        "cyan": "\033[36m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "pink": "\033[95m"
    }
    reset = "\033[0m"
    codes = list(colors.values())
    random_list = []
    temp_codes = codes.copy()
    for i in range(len(codes)):
        choice = random.choice(temp_codes)
        random_list.append(choice)
        temp_codes.remove(choice)
    
    color_cycle = itertools.cycle(random_list)
    for char in text:
        if char == " ":
            print(char, end="")
            continue
        color = next(color_cycle)
        print(f"{color}{char}{reset}", end="", flush=True)
        time.sleep(speed)
    print()