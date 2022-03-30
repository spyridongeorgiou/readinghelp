# readinghelp
# Made by Spyridon Georgiou 
# https://github.com/spyridongeorgiou/readinghelp
# http://timgolden.me.uk/pywin32-docs/contents.html
# https://www.pygame.org/docs/
# https://pipenv.pypa.io/en/latest/

# NOTE: lines starting with ## are code that is not needed for the program to function but may be useful for testing and figuring out bugs

# required imports
import pygame as pg
import sys
import win32api
import win32con
import win32gui
import pyautogui
import logging
##import re

#regular color tuples
red = (255,0,0)
##green = (0,255,0)
##blue = (0,0,255)
black = (0,0,0)
R,G,B = 0,0,0 # RED GREEN BLUE set to 0 initially
cmod = 62 #color value modifier for RGB
t = 2 #thickness of the line drawn/placed on screen

#special color tuple 
fuchsia = (255, 0, 128) # needed for transparency
# NOTE: DO NOT USE THIS AS A REGULAR COLOR !

lineplace = [] # empty list that saves the X * Y coordinates of the mouse after click and apppends them as tuples, 
#                for example: for three clicks, three different values will be saved [(X0,Y0),(X1,Y1),(X2,Y2)]
i = [] # list which contains latest Y coordinate of lineplace list after a click has happened

flags = pg.SHOWN | pg.FULLSCREEN | pg.DOUBLEBUF #optional flags which determine how the window appears on screen
clock = pg.time.Clock() # game clock initialized

# reminder to self: x _ y | == w _ h |

#https://stackoverflow.com/a/2091530/14253816
##class WindowMgr:
##    """Encapsulates some calls to the winapi for window management"""
##    def __init__ (self):
##        """Constructor"""
##        self._handle = None
##    def find_window(self, class_name, window_name=None):
##        """find a window by its class_name"""
##       self._handle = win32gui.FindWindow(class_name, window_name)
##    def _window_enum_callback(self, hwnd, wildcard):
##        """Pass to win32gui.EnumWindows() to check all the opened windows"""
##        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
##            self._handle = hwnd
##    def find_window_wildcard(self, wildcard):
##        """find a window whose title matches the wildcard regex"""
##        self._handle = None
##        win32gui.EnumWindows(self._window_enum_callback, wildcard)
##    def set_foreground(self):
##        """put the window in the foreground"""
##        win32gui.SetForegroundWindow(self._handle)
##w = WindowMgr()   

# beginning of the program 
if __name__ == "__main__":
    pg.init() # initialize the pg module
    pg.display.set_caption('readinghelp') # set caption of the launched window
    pg.font.init() #initialize the font. this is normally already called in pg.init()
    pg.event.set_grab(True) # limit input to only the pygame window, to avoid accidentally  
    pg.font.SysFont("Calibri",18) # Fonttype and Size
    pg.key.set_repeat(150) # control how held keys are repeated upon being held down
    ##screeninit = pg.display.get_init()
    #pg and pg display are now initialized

    #optional flag arguments which determine how the window appears on screen. these are passed to the screen variable below
    #for borderless, use pg.NOFRAME
    current_w = pg.display.Info().current_w #current width of the screen aka X coordinate
    current_h = pg.display.Info().current_h #current height of the screen aka Y coordinate
    #screen (the pygame main screen): 
    screen = pg.display.set_mode((current_w, current_h),flags,16) # set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
    # surface i.e. layer on top of screen:
    surface = pg.Surface((current_w,current_h)) # surface for blitting images

    hwnd = pg.display.get_wm_info()["window"] # create layered window 
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY) # every pixel that matches the color fuchsia (255,0,128) is set as transparent
    
    focus = win32gui.SetFocus(hwnd) 
    totop = win32gui.BringWindowToTop(hwnd) # Set Window to top

    def keyevent(): # subprogram which checks within ev: if the ESC key was pressed, if so, it quits pygame and exits the program successfully
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseposfreeze = list(pyautogui.position())
                lineplace.append((mouseposfreeze[0],mouseposfreeze[1]))
                return


    # mainloop for pygame
    while 1:
        pg.display.init() # initialize the pg display module
        clock.tick(75)
        screen.fill(fuchsia) # this is required in order to make the screen transparent
        ev = pg.event.get() # get events from queue for processing
        for event in ev: # event handler
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): # if the ESC button is pressed, the program is exited 
                    pg.quit() # quit pygame NOTE: technically this should be enough
                    sys.exit() # exit program NOTE: however this is to ensure the program stops running
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1: # if pressed key was 1
                    R = R + cmod
                    if R > 255:
                        R = R - R
                if event.key == pg.K_2: # 2 key
                    G = G + cmod
                    if G > 255:
                        G = G - G
                if event.key == pg.K_3: # 2 key
                    B = B + cmod
                    if B > 255:
                        B = B - B
            color = [R,G,B]
            keyevent()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    t = t + 1
                    if t > 50:
                        t = t - t + 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: # upon pressing spacebar
                    lineplace.clear()  # clear lineplace list i.e. remove all of the persistent lines spawned by left-clicking
                    R = R - R # set R to 0
                    G = G - G # set G to 0 
                    B = B - B # set B to 0
                    t = t - t + 2 # set t back to 2

        pg.mouse.set_visible(True) # make the mouse visible     
        mousepos = list(pyautogui.position()) # turn the current X * Y (NOTE: relative to top left corner of DISPLAY not PYGAME WINDOW) coordinates of the mouse into a simple list [x,y]
        line = pg.draw.line(screen,color,(0,mousepos[1]),(current_w,mousepos[1]),width=t) # draw a straight anti-aliased line on the current Y height of the mouse on screen, while the X width stays the same as the screens current_w
        for i in lineplace: #for each (X,Y) tuple in i, place a line of the latest (X,Y) tuple using the Y [1] coordinate
            pg.draw.line(screen,color,(0,i[1]),(current_w,i[1]),width=t)
        pg.display.update() # refresh the display to make changes visible    
        totop # bring window to top NOTE: Currently not fully working as intended
        focus # set focus to window NOTE: Currently not fully working as intended
