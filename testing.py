#!/usr/bin/env python3
from ev3dev2.display import Display
from time import sleep

disp = Display()
disp.text_grid("Hi :)")
disp.update()
sleep(10)