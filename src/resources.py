#!/usr/bin/python

"""
resources.py - Load all resource data once 
"""

import os, sys
import pygame
from pygame.locals import *

def init(mainpath,screen_res):
    
    # Load kernel
    global kernal_gfx
    kernal_gfx = pygame.image.load(os.path.join(mainpath,'data','gfx','kernel.png')).convert()
    kernal_gfx.set_colorkey((0,0,0))
    
    global kernal_end_gfx
    kernal_end_gfx = pygame.image.load(os.path.join(mainpath,'data','gfx','kernel_end.png')).convert()
    kernal_end_gfx.set_colorkey((0,0,0))
    
    global title_gfx
    title_gfx = []
    title_gfx.append(pygame.image.load(os.path.join(mainpath,'data','gfx','titlescreen_0.png')).convert())
    title_gfx[-1].set_colorkey((0,0,0))
    title_gfx.append(pygame.image.load(os.path.join(mainpath,'data','gfx','titlescreen_1.png')).convert())
    title_gfx[-1].set_colorkey((0,0,0))
    title_gfx.append(pygame.image.load(os.path.join(mainpath,'data','gfx','titlescreen_2.png')).convert())
    title_gfx[-1].set_colorkey((0,0,0))
    
    global go_gfx
    go_gfx = pygame.image.load(os.path.join(mainpath,'data','gfx','go.png')).convert()
    go_gfx.set_colorkey((255,0,255))
    
    global victory_gfx
    victory_gfx = pygame.image.load(os.path.join(mainpath,'data','gfx','victory.png')).convert()
    victory_gfx.set_colorkey((255,0,255))
    
    global defeat_gfx
    defeat_gfx = pygame.image.load(os.path.join(mainpath,'data','gfx','defeat.png')).convert()
    defeat_gfx.set_colorkey((255,0,255))
    
    # Fonts and text
    
    # Sound Data
    global soundfx
    soundfx = {}
    soundfx['magical_1_0'] = pygame.mixer.Sound(os.path.join(mainpath,'data','snd','magical_1_0.ogg'))
    
    # Music Data
    global musicpaths
    musicpaths = {}
    musicpaths['electrodoodle'] = os.path.join(mainpath,'data','music','electrodoodle.ogg')
    
    # pre-sets and controls
    global controlmap
    controlmap = {}
    controlmap['R'] = K_RIGHT
    controlmap['L'] = K_LEFT
    
    
    