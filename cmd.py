import sys, sched, time
#import schedule
from pynput.mouse import Button, Controller
from pynput import mouse
import random
from utilities import calculateWH
from collector import GetFrame
from constants import Winfo
from utilities import WithinWinowFrame
from collector import GetFrame
ctrl = Controller()
scheduler = sched.scheduler(time.time, time.sleep)

GAME_ANNOUNCEMENT = "GA"
SPLASH_SCREEN = "SC"
YARD = "YD"
BACK_YARD = "BY"
PET_PLAYGROUND = "PP"
WORLD_MAP = "WM"
LEVEL = "LV"

# button ids
TO = "_TO_"
GA2SC = GAME_ANNOUNCEMENT + TO + SPLASH_SCREEN

# A stage includes following fields:
# stage / level id
# stage links, a list of stage id that current stage can link to
# a list of buttons the stage has
# stage description
stage = {
    GAME_ANNOUNCEMENT : ([SPLASH_SCREEN], [GA2SC], "Game Announcement, The first screen"),
    SPLASH_SCREEN :     ([SPLASH_SCREEN], [], "The splash screen, click to enter the game"),
    YARD :              ([BACK_YARD, WORLD_MAP, BACK_YARD], [], "The yard"),
    WORLD_MAP:          (["LV27"], [], "All levels, Local challenge and World challenge")
}

# A button includes following fields:
# stage / level id
# button id
# button area
# button function description
button = {
    GA2SC : (calculateWH([680, 70, 700, 90]), "Go to the splash screen")
}


# input 6 numbers, x, y, x1, y1, w and h
def generateClickPoint(area):
    if len(area) == 6:
        offsetW = random.uniform(0.0, 1.0)
        offsetH = random.uniform(0.0, 1.0)
        return [area[0] + int(area[4] * offsetW), area[1] + int(area[5] * offsetH)]
    else:
        return None

# generate random point within a button area
def generateButtonClick(buttonId):
    return generateClickPoint(button[buttonId][0])

def generateClickDelay():
    pass

def initalizeCmd(shape):
    #python 37 issue in conda
    APP_START_TS = time.monotonic_ns() * 1000

    print('The current pointer position is {} The App x,y:{}, {} : {}, {}'.format(str(ctrl.position), Winfo.x0, Winfo.y0, Winfo.w, Winfo.h))
    ctrl.position = (Winfo.x0, Winfo.y0)
    print(APP_START_TS)
    return

def CursorClickAt(x, y):
    print("origin {}, {}", Winfo.x0, Winfo.y0)
    ctrl.position = (Winfo.x0 + x, Winfo.y0 + y)
    ctrl.press(Button.left)
    ctrl.release(Button.left)
def HeartbeatMain():
    print("main thread r u n n i n g ...")

def Go():
    trigger_time = 3
    for trigger_time in range (trigger_time):
        scheduler.enter(float(trigger_time), 0, actionMouseMove)
    
    pos = generateButtonClick(GA2SC)
    print("pos---->{}".format(str(pos)))

    trigger_time = trigger_time + 1
    scheduler.enter(trigger_time, 0, lambda: CursorClickAt(pos[0], pos[1]))
    scheduler.run()

    #schedule.every(3).seconds.do(HeartbeatMain)
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)

def actionMouseMove():
    ctrl.move(5, 30)
    return

def onMouseMoving(x, y):
    #print('Pointer moved to {0}'.format((x, y)))
    return

def onMouseClicking(x, y, button, pressed):
    if WithinWinowFrame(x,y) and Button.right == button:
        GetFrame()
        print('Right button released {} action {} at {}'.format(str(button), str(pressed), (x, y)))

def onMouseScrolling(x, y, dx, dy):
    pass

# Collecting events until released

def StartMouseListener():
    with mouse.Listener(
            #on_move=onMouseMoving,
            on_click=onMouseClicking,
            on_scroll=onMouseScrolling) as listener:
        listener.join()