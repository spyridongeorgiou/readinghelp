#Made by Spyridon Georgiou with reference code from
#https://stackoverflow.com/questions/7053971/python-trouble-using-escape-key-to-exit
#https://pythonprogramming.altervista.org/how-to-make-a-fully-transparent-window-with-pg
#https://github.com/ashukla95/traffic-management-using-bluetooth/blob/1a576179d11199136a62c6c811ff583b11935330/frame1.py
#Use freely

from importlib.machinery import ModuleSpec
import pygame as pg
import sys
import os
import win32api
import win32con
import win32gui
import pyautogui
#little safety lock just in case :)
if __name__ == "__main__":
    
    white = (255,255,255)
    fuchsia = (255, 0, 128)
    dark_red = (139, 0, 0)
    
    pg.init() #initialize the pg module
    pg.display.init() #initialize the pg display module
    pg.display.set_caption('ReadingHelp')
    #screeninit = pg.display.get_init()
####pygame and display initialized####
    flags = pg.SHOWN | pg.FULLSCREEN
    
    current_w = pg.display.Info().current_w
    current_h = pg.display.Info().current_h
    #for borderless, use pg.NOFRAME
    #screen initializer
    screen = pg.display.set_mode((current_w, current_h),flags) #set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
    #surface initializer
    surface = pg.Surface((current_w,current_h))
     #color tuples

    
    #create layered window
    hwnd = pg.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    #set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    #make the mouse visible
    pg.mouse.set_visible(True)
    while 1==1:
        #mouseinfo = pg.mouse.get_cursor 
        #print (mouseinfo)
        #FIX: add get focus to window
        # x _ y | equals w _ h |
        pg.time.wait(25)
        screen.fill(fuchsia)  # Transparent background
        #pg.draw.rect(screen, dark_red, pg.Rect(30, 30, 60, 60))
        #whiteline = pg.draw.aaline(screen,white,(0,540),(1920,540))
        #mousepos = pg.mouse.get_pos()
        mousepos = list(pyautogui.position())
        whiteline = pg.draw.aaline(screen,white,(0,mousepos[1]),(current_w,mousepos[1]))
        print (mousepos)
        pg.display.update()
        def keyevent():
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_UP:
                        return
        keyevent()
