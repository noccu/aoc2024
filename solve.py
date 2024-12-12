from sys import argv
from os import chdir
from importlib import import_module

if len(argv) == 3:
    day = argv[1]
    part = argv[2]
    print(f"Result of day {day}, part {part}:")
    day_dir = f"day_{day}"
    chdir(day_dir)
    try:
        import_module(f"{day_dir}.part{part}")
    except ImportError:
        print("That part doesn't exist!")
