from clouds import Clouds
from map import map
from helecopter import helecopter as Heleco
from pynput import keyboard
import time
import os
import json

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDATE = 75
CLOUD_UPDATE = 100
MAP_W, MAP_H = 20,10
tick = 1

MOVES = {'w': (-1,0), 'd': (0,1), 's': (1,0), 'a':(0,-1)}
# f - save, g - load
def process_key(key, injected):
    global helec, tick, clouds, field
    c = key.char.lower()
    if c in MOVES.keys():
        dx,dy = MOVES[c][0],MOVES[c][1]
        helec.move(dx,dy)
    elif c == 'f':
        data = {"helecopter": helec.export_data(),
                "clouds": clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data,lvl)
    elif c == 'g':
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 1
            helec.import_data(data["helecopter"])
            clouds.import_data(data["clouds"])
            field.import_data(data["field"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key
)
listener.start()


field = map(MAP_W,MAP_H)
clouds = Clouds(MAP_W,MAP_H)
helec = Heleco(MAP_W,MAP_H)


while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    # print("TICK", tick)
    field.process_helecopter(helec, clouds)
    helec.print_stats()
    field.print_map(helec, clouds)
    tick +=1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fire()
    if (tick % CLOUD_UPDATE == 0):
        clouds.update()
