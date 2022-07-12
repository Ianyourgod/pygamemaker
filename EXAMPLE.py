#keyboard module is needed if you want to get inputs
import keyboard
from game import *


player = obj(0,0,3,3)
wn = window(10,10,clear=True)

running = True
while running:
    if keyboard.is_pressed("w"):
        player.up()
    if keyboard.is_pressed("a"):
        player.left()
    if keyboard.is_pressed("s"):
        player.down()
    if keyboard.is_pressed("d"):
        player.right()
    if keyboard.is_pressed("q"):
        running = False
       wn.update()
