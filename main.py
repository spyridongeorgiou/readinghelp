# readinghelp
# Made by Spyridon Georgiou (https://github.com/spyridongeorgiou/readinghelp)
# http://timgolden.me.uk/pywin32-docs/contents.html
# https://www.pygame.org/docs/
# https://pipenv.pypa.io/en/latest/
# Use freely

# Note: lines starting with ## are code that is not needed for the program to function but may be useful for testing and figuring out bugs

# required imports
##from importlib.machinery import ModuleSpec
import pygame as pg
import time
import sys
##import os
import win32api
import win32con
import win32gui
import pyautogui
##import logging
import re

#regular color tuples
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
R,G,B = 0,0,0
## color = [R,G,B]
cmod = 62 #color modifier for RGG

#dark_red = (139, 0, 0)

#special color tuple, DO NOT USE AS A REGULAR COLOR !
fuchsia = (255, 0, 128) # needed for transparency

lineplace = [] # empty list that saves the X * Y coordinates of the mouse after click and apppends them as tuples, 
#                for example: for three clicks, three different values will be saved [(X0,Y0),(X1,Y1),(X2,Y2)]
i = [] # list which contains latest Y coordinate of lineplace list after a click has happened

flags = pg.SHOWN | pg.FULLSCREEN | pg.DOUBLEBUF #optional flags which determine how the window appears on screen
clock = pg.time.Clock() # game clock initialized
wait = time.sleep(0.1) # take a breather and wait for 0.1s

# FIX: add get focus to window #
# reminder to self: x _ y | == w _ h |

#Great code from https://stackoverflow.com/a/2091530/14253816
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None
    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)
    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd
    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

# beginning of the program
if __name__ == "__main__":
    
    pg.init() # initialize the pg module
    pg.display.set_caption('readinghelp') # set caption of the launched window
    pg.font.init()
    ##guifont = pg.font.Font(None,22) # Fonttype and Size
    ##screeninit = pg.display.get_init()
    #pg and pg display are now initialized

    #optional flag arguments which determine how the window appears on screen. these are passed to the screen variable below
    #for borderless, use pg.NOFRAME
    current_w = pg.display.Info().current_w #current width of the screen aka X coordinate
    current_h = pg.display.Info().current_h #current height of the screen aka Y coordinate
    #screen initializer (the pygame main screen): 
    screen = pg.display.set_mode((current_w, current_h),flags,16) # set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
    # surface initializer:
    surface = pg.Surface((current_w,current_h))

    hwnd = pg.display.get_wm_info()["window"] # create layered window 
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY) # set window transparency color
    #focus = win32gui.SetFocus(hwnd) 
    totop = win32gui.BringWindowToTop(hwnd) # Set Window to top
    
    def keyevent(): # subprogram which checks within ev: if the ESC key was pressed, if so, it quits pygame and exits the program successfully
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: # upon pressing spacebar
                lineplace.clear()  # clear lineplace list i.e. remove all of the persistent lines spawned by left-clicking
                color.clear()
                #return
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseposfreeze = list(pyautogui.position())
                lineplace.append((mouseposfreeze[0],mouseposfreeze[1]))
                return
    while 1:
        pg.display.init() # initialize the pg display module
        clock.tick(75)
        pg.event.set_grab(True)
        ev = pg.event.get()
        for event in ev:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1: 
                    R = R + cmod
                    if R > 255:
                        R = R - R
                if event.key == pg.K_2:
                    G = G + cmod
                    if G > 255:
                        G = G - G
                if event.key == pg.K_3:
                    B = B + cmod
                    if B > 255:
                        B = B - B
            color = [R,G,B]
            keyevent()
        #pg.display.update() # refresh the display to make changes visible
        pg.mouse.set_visible(True) # make the mouse visible
        
        screen.fill(fuchsia) # this is required in order to make the screen transparent

        ##pg.draw.rect(screen, dark_red, pg.Rect(30, 30, 60, 60)) # draws a small rectangle in the top left corner of the screen, currently not needed for transaprency
        ##line = pg.draw.aaline(screen,red,(0,540),(1920,540))
        mousepos = list(pyautogui.position()) # turn the current W * H / X * Y coordinates of the mouse into a simple list [w,h]
        line = pg.draw.line(screen,color,(0,mousepos[1]),(current_w,mousepos[1]),width=3) # draw a straight anti-aliased line on the current Y height of the mouse on screen, while the X width stays the same as the screens current_w
        ##print (color)
        #print (ev)
        for i in lineplace: #for each (X,Y) tuple in i, place a line of the latest (X,Y) tuple using the Y [1] coordinate
            #print(lineplace)
            #print (i[1])
            pg.draw.line(screen,color,(0,i[1]),(current_w,i[1]),width=3)
        ##print (mousepos) # print current W * H / X * Y coordinates
        pg.event.pump()
        pg.display.update() # refresh the display to make changes visible
        #w = WindowMgr()
        #w.find_window_wildcard(".*readinghelp.*")
        #w.set_foreground()
        #totop
        #focus
