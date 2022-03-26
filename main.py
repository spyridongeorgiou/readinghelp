#pygame relative mouse position test

import pygame as pg
import sys
import win32con
import win32gui
import win32api
import pyautogui
import logging 
import os

pos_x = 0
pos_y = 0

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG) # logging

pg.init()
pg.display.init()

white = (255,255,255)
black = (0,0,0)
blue = (0,0,128)
red = (255,0,0)
fuchsia = (255,0,128)
green = (0,255,0)

lineplace = []
i = []
flags = pg.SHOWN | pg.RESIZABLE 
clock = pg.time.Clock()
pg.display.set_caption("readinghelp")
#current_w = pg.display.Info().current_w
#current_h = pg.display.Info().current_h
width = pg.display.Info().current_w
height = pg.display.Info().current_h

windowbar = 49 # height of the windowbar in pixels
screen = pg.display.set_mode((width,height - windowbar),flags)
surface = pg.Surface((width, height))
rectanglew = 100
rectangleh = 100
#s = pg.Surface((1000,750))  # the size of your rect
#s.set_alpha(128)                # alpha level
#s.fill((255,255,255))           # this fills the entire surface
#windowSurface.blit(s, (0,0))

mousepos = pg.mouse.get_pos()
hwnd = pg.display.get_wm_info()["window"] # create layered window 
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY) # set window transparency color
#def find_window_movetop(cls):
#    hwnd = win32gui.FindWindow(None, cls.processname)
#    win32gui.ShowWindow(hwnd,5)
#    win32gui.SetForegroundWindow(hwnd)
#    rect = win32gui.GetWindowRect(hwnd)
#    return rect 

def focus():
    try:
        win32gui.UpdateLayeredWindow(hwnd)
        win32gui.ShowWindow(hwnd,5)
        win32gui.SetFocus(hwnd) 
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
#        find_window_movetop("readinghelp")
    except:
        return

def keyevent(): # subprogram which checks within ev: if the ESC key was pressed, if so, it quits pygame and exits the program successfully
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: # upon pressing spacebar
                lineplace.clear()  # clear lineplace list i.e. remove all of the persistent lines spawned by left-clicking
                return
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                    mouseposfreeze = list(pg.mouse.get_pos())
                    lineplace.append((mouseposfreeze[0],mouseposfreeze[1]))
                    #return
while 1:
    ##hwndMain = win32gui.FindWindow("readinghelp", None)
    dynamic_w = pg.display.Info().current_w
    dynamic_h = pg.display.Info().current_h
    clock.tick(76)
    ev = pg.event.get()
    for event in ev:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        keyevent()
    ##print (ev)
    ##pg.event.set_grab(True)
    pg.mouse.set_visible(True)
    screen.fill(fuchsia)
    mousepos = list(pg.mouse.get_pos())
    mouseposrect = list(pyautogui.position())
    mouseposdiff = [dynamic_w - mouseposrect[0],dynamic_h - mouseposrect[1]]

    logging.debug("mouse position " + str(mousepos) + "window width " + str(mouseposrect) + "diff " + str(mouseposdiff)) #logging

    rect = pg.draw.rect(screen,(green),pg.Rect(mouseposdiff[0] - rectangleh/2,mouseposdiff[1] - 50-rectangleh/2,rectanglew,rectangleh))
    line = pg.draw.aaline(screen,red,(0,mousepos[1]),(width,mousepos[1])) 
    #surface.fill((0,1,0,0))

    #screen.blit(surface,(width,height),special_flags=pg.BLEND_RGB_ADD)
    for i in lineplace: #for each (X,Y) tuple in i, place a line of the latest (X,Y) tuple using the Y [1] coordinate
            ##print(lineplace)
            ##print (i[1])
        pg.draw.aaline(screen,blue,(0,i[1]),(width,i[1]))
    pg.event.pump()
    pg.display.update()
    focus()
    #mouseposdiff.clear()
