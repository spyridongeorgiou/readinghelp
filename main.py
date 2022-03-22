#readinghelp
# Made by Spyridon Georgiou with reference code from
# https://stackoverflow.com/questions/7053971/python-trouble-using-escape-key-to-exit
# https://pythonprogramming.altervista.org/how-to-make-a-fully-transparent-window-with-pg
# https://github.com/ashukla95/traffic-management-using-bluetooth/blob/1a576179d11199136a62c6c811ff583b11935330/frame1.py
# Use freely

# Note: lines starting with ## are code that is not needed for the program to function but may be useful for testing and figuring out bugs


# required imports
from importlib.machinery import ModuleSpec
import pygame as pg
import sys
import os
import win32api
import win32con
import win32gui
import pyautogui

#color tuples
red = (255,0,0)
black = (0,0,0)
fuchsia = (255, 0, 128) # needed for transparency ! DO NOT USE AS A REGULAR COLOR !
dark_red = (139, 0, 0)
blue = (0,0,255)

lineplace = [] # empty list that saves the X * Y coordinates of the mouse after click and apppends them as tuples, 
#                for example: for three clicks, three different values will be saved [(X0,Y0),(X1,Y1),(X2,Y2)]
start = 0 # REMOVE
nth = 3 # REMOVE 

flags = pg.SHOWN | pg.FULLSCREEN #optional flags which determine how the window appears on screen
clock = pg.time.Clock() # Game Clock


# FIX: add get focus to window #
# reminder to self: x _ y | == w _ h |

# beginning of the program
if __name__ == "__main__":
    
    pg.init() # initialize the pg module
    pg.display.init() # initialize the pg display module
    pg.display.set_caption('readinghelp') # set caption of the launched window
    ##guifont = pg.font.Font(None,22) # Fonttype and Size
    ##screeninit = pg.display.get_init()
    #pg and pg display are now initialized

    #optional flag arguments which determine how the window appears on screen. these are passed to the screen variable below
    #for borderless, use pg.NOFRAME
    current_w = pg.display.Info().current_w #current width of the screen aka X coordinate
    current_h = pg.display.Info().current_h #current height of the screen aka Y coordinate
    #screen initializer (the pygame main screen): 
    screen = pg.display.set_mode((current_w, current_h),flags) # set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
    # surface initializer:
    surface = pg.Surface((current_w,current_h))

    hwnd = pg.display.get_wm_info()["window"] # create layered window 
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY) # set window transparency color
    
    def keyevent(): # subprogram which checks within ev: if the ESC key was pressed, if so, it quits pygame and exits the program successfully
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    return
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                        mouseposfreeze = list(pyautogui.position())
                        lineplace.append((mouseposfreeze[0],mouseposfreeze[1]))
                        for i in lineplace:
                            print(lineplace)
                            print (i[1])
                            pg.draw.aaline(screen,blue,(0,i[1]),(current_w,i[1]))
                            pg.display.flip()
                        return
                    #return
    while True:
        ev = pg.event.get()
        for event in ev:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            keyevent()
        pg.display.flip()

        #pg.display.update() # refresh the display to make changes visible
        pg.mouse.set_visible(True) # make the mouse visible
        pg.time.wait(25)
        screen.fill(fuchsia) # this is required in order to make the screen transparent

        ##pg.draw.rect(screen, dark_red, pg.Rect(30, 30, 60, 60)) # draws a small rectangle in the top left corner of the screen, currently not needed for transaprency
        ##line = pg.draw.aaline(screen,red,(0,540),(1920,540))
        #mousepos = pg.mouse.get_pos()

        mousepos = list(pyautogui.position()) # turn the current W * H / X * Y coordinates of the mouse into a simple list [w,h]
        line = pg.draw.aaline(screen,red,(0,mousepos[1]),(current_w,mousepos[1])) # draw a straight anti-aliased line on the current Y height of the mouse on screen, while the X width stays the same as the screens current_w
        
        
        ##print (mousepos) # print current W * H / X * Y coordinates
        pg.display.update() # refresh the display to make changes visible
        clock.tick(60)
##        mouseevent()
