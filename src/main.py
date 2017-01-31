#!/usr/bin/python

"""
main.py - Main entry point for game
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

import resources
import game

# Start
def main(mainpath):

    # Initialise pygame
    pygame.init()
    pygame.mixer.init()
    pygame.mouse.set_visible(False)
    
    # start up director
    framerate = 30
    screen_res = (850,480)
    window_title = "Waverider"
    dir = GameDirector(window_title, screen_res, framerate)
    
    # Load resources
    resources.init(mainpath,screen_res)
    
    # Load game scenes
    titlescreen = game.TitleScreen(dir, screen_res)
    dir.addscene('titlescreen', titlescreen)
    maingame = game.MainGame(dir, screen_res)
    dir.addscene('maingame', maingame)
    
    # start up director
    dir.change_scene('titlescreen', [])
    #dir.change_scene('maingame', [])
    dir.loop()
    
    # exiting, record framerate
    #print maingame.avgframerate
    #fp = open(os.path.join(mainpath,'framerate.txt'),"w")
    #fp.write("%f\n"%(maingame.avgframerate))
    #fp.close()

