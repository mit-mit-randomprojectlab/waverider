#!/usr/bin/python

"""
game.py - main in-game scene classes
"""

import os
import pygame
from pygame.locals import *
from gamedirector import *

import random
from math import *

import resources
from common import FadeInOut

import subprocess
from wii_balance_board import Wiiboard, BoardEvent
import Queue

global board

class KeyControl(object):
    def __init__(self):
        self.l = 0
        self.r = 0
    
    def ProcessKeyEvent(self,event):
        if event.type == KEYDOWN:
            if event.key == resources.controlmap["L"]:
                self.l = 1
            elif event.key == resources.controlmap["R"]:
                self.r = 1
        elif event.type == KEYUP:
            if event.key == resources.controlmap["L"]:
                self.l = 0
            elif event.key == resources.controlmap["R"]:
                self.r = 0

class WaveData(object):
    def __init__(self,lvl):
        self.lvl = lvl
        
        if self.lvl == 0:
            self.amplitude1 = 0.2
            self.frequency1 = 0.5
            self.amplitude2 = 0.2
            self.frequency2 = 0.5
            self.par_speed = 0.01
        if self.lvl == 1:
            self.amplitude1 = 0.2
            self.frequency1 = 0.5
            self.amplitude2 = 0.2
            self.frequency2 = 0.7
            self.par_speed = 0.015
        elif self.lvl == 2:
            self.amplitude1 = 0.2
            self.frequency1 = 1.0
            self.amplitude2 = 0.3
            self.frequency2 = 1.5
            self.par_speed = 0.015
        if self.lvl == 3:
            self.amplitude1 = 0.3
            self.frequency1 = 0.5
            self.amplitude2 = 0.2
            self.frequency2 = 0.7
            self.par_speed = 0.018
        elif self.lvl == 4:
            self.amplitude1 = 0.35
            self.frequency1 = 0.5
            self.amplitude2 = 0.2
            self.frequency2 = 1.5
            self.par_speed = 0.016
        elif self.lvl == 5:
            self.amplitude1 = 0.3
            self.frequency1 = 0.5
            self.amplitude2 = 0.1
            self.frequency2 = 1.6
            self.par_speed = 0.018
        
        #self.amplitude1 = 0.2
        #self.frequency1 = 0.5
        #self.amplitude2 = 0.2
        #self.frequency2 = 0.5
        
    def wave_func(self,x):
        #return 0.5 + self.amplitude*sin(self.frequency*(float(x))*(2*pi))
        return 0.5 + self.amplitude1*sin(self.frequency1*(float(x))*(2*pi)) + \
            self.amplitude2*sin(self.frequency2*(float(x))*(2*pi))

class MainGame(GameScene):
    def __init__(self, director, window_size):
        super(MainGame, self).__init__(director)
        self.window_size = window_size
        
        # frame rate recording
        self.avgframerate = -1
        self.frsamples = 0
        
        # fade in/out
        self.fade = FadeInOut(15)
        
        # Music
        self.current_music = 'none'
        
        # Background
        self.background = pygame.Surface(window_size)
        self.background.fill((0,0,0))
        self.background.convert()
        
        # Wavesurface
        self.course_len = 10
        self.wavesurface = pygame.Surface(((self.course_len+1)*window_size[0],window_size[1]))
        self.wavesurface.fill((0,0,0))
        self.wavesurface.convert()
        self.wavesurface.set_colorkey((255,0,255))
        
        self.wavebackground = pygame.Surface(window_size)
        self.wavebackground.fill((255,0,0))
        self.wavebackground.convert()
        
        # Player control
        self.control = KeyControl()
        
        self.last_event = BoardEvent(1.0, 1.0, 1.0, 1.0, 0, 0)
    
    def on_switchto(self, switchtoargs):
        
        self.lvl = switchtoargs[0]
        self.exiting = False
        self.victory = False
        
        self.countin = 30
        self.stepped_on = False
        
        # player data
        self.player_angle = 0.0
        self.player_pos = float(self.course_len)
        self.player_velocity = 0.0
        self.circle_size = 16
        
        self.par_position = float(self.course_len)
        
        # Wave Data
        self.wave = WaveData(self.lvl)
        self.wave_colour = (255,255,255)
        
        # Draw wave
        self.wavesurface.fill((0,0,0))
        #step = 8.0/self.window_size[0]
        step = 1.0/self.window_size[0]
        x = 0.0
        for xi in xrange(self.course_len*self.window_size[0]/1):
            y = self.wave.wave_func(x)
            x += step
            self.wavesurface.blit(resources.kernal_gfx,(self.window_size[0]*(x+0.5)-8,self.window_size[1]*y-8))
        y0 = self.wave.wave_func(0.0)
        self.wavesurface.blit(resources.kernal_end_gfx,(self.window_size[0]*(0.5)-16,self.window_size[1]*y0-16))
        yend = self.wave.wave_func(self.course_len)
        self.wavesurface.blit(resources.kernal_end_gfx,(self.window_size[0]*(self.course_len+0.5)-16,self.window_size[1]*yend-16))
        
        # Fade in game
        self.background.fill((0,0,0))
        self.fade.FadeIn()
    
    def on_update(self):
        
        global board
        
        # framerate tracking
        self.frsamples += 1
        if self.frsamples == 1:
            self.avgframerate = self.director.framerate
        else:
            self.avgframerate = self.avgframerate + (self.director.framerate - self.avgframerate)/(self.frsamples)
        
        if self.countin > 0:
            self.countin -= 1
            
        else:
            
            if self.countin > -30:
                self.countin -= 1
            
            # Update player angle and position
            if not self.exiting:
                
                """
                # change player angle (keys for now)
                rate = 0.1
                limit = 2.0
                if self.control.l == 1:
                    self.player_angle -= rate
                    if self.player_angle < -limit:
                        self.player_angle = -limit
                elif self.control.r == 1:
                    self.player_angle += rate
                    if self.player_angle > limit:
                        self.player_angle = limit
                """
                
                # Read wii balance board
                try:
                    event = board.EventQueue.get_nowait()
                    qsize = board.EventQueue.qsize()
                    for j in xrange(qsize):
                        event2 = board.EventQueue.get()
                    self.last_event = event
                    if event.totalWeight > 20.0:
                        self.stepped_on = True
                    
                except Queue.Empty:
                    event = self.last_event
                
                # convert to player angle
                left = 0.5*(event.topLeft+event.bottomLeft)
                right = 0.5*(event.topRight+event.bottomRight)
                
                self.player_angle = 5.0*(right-left)/(right+left)
                
                # determine slope
                y1 = self.wave.wave_func(self.player_pos)
                y2 = self.wave.wave_func(self.player_pos+0.01)
                slope = (y2-y1)/0.01
                
                diverge = fabs(slope-self.player_angle)
                if slope > 0 and self.player_angle > slope: # set to zero if going right direction
                    diverge = 0
                if slope < 0 and self.player_angle < slope: # set to zero if going right direction
                    diverge = 0
                
                #print slope, self.player_angle, diverge
                
                flow = exp(-1*diverge)
                if event.totalWeight < 20.0:
                    flow = 0.0
                self.wave_colour = (255*(1-flow),255*flow,0)
                
                #speed = 0.02*flow
                accel = 0.005
                drag = 10.0
                self.player_velocity = self.player_velocity - drag*self.player_velocity*self.player_velocity + accel*flow
                if self.player_velocity < 0:
                    self.player_velocity = 0
                
                self.par_position -= self.wave.par_speed
                if self.par_position <= 0:
                    self.exiting = True
                    self.victory = False
                    self.wave_colour = (255,0,0)
                self.player_pos -= self.player_velocity
                if self.player_pos <= 0:
                    self.player_pos = 0
                    self.exiting = True
                    self.victory = True
                    self.wave_colour = (0,255,0)
                    resources.soundfx['magical_1_0'].play()
        
        # Control fade in/out, look for end game cues
        self.fade.Update()
        if self.exiting and self.fade.direction == 'in':
            self.fade.FadeOut(False)
        if self.fade.finished_out:
            if self.victory:
                next_lvl = self.lvl+1
            else:
                next_lvl = self.lvl
            if next_lvl < 6 and self.stepped_on:
                self.director.change_scene('maingame', [next_lvl])
            else:
                self.director.change_scene('titlescreen', [True])
        
    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene(None, [])
            if event.type == KEYDOWN or event.type == KEYUP:
                self.control.ProcessKeyEvent(event)
    
    def draw(self, screen):
        self.wavebackground.fill(self.wave_colour)
        screen.blit(self.wavebackground, (0, 0))
        tilecoords = (self.window_size[0]*(self.player_pos),0,self.window_size[0],self.window_size[1])
        screen.blit(self.wavesurface, (0, 0), area=tilecoords)
        
        par_pos = (self.window_size[0]/2-self.window_size[0]*(self.player_pos-self.par_position), self.window_size[1]*self.wave.wave_func(self.par_position))
        pygame.draw.circle(screen, (255,255,255), (int(par_pos[0]),int(par_pos[1])), 16, 0)
        
        player_pos = (self.window_size[0]/2, self.window_size[1]*self.wave.wave_func(self.player_pos))
        if self.exiting:
            self.circle_size += 32
        pygame.draw.circle(screen, self.wave_colour, (int(player_pos[0]),int(player_pos[1])), self.circle_size, 0)
        if self.exiting:
            if self.victory:
                screen.blit(resources.victory_gfx, (self.window_size[0]/2-85, self.window_size[1]/2-28))
            else:
                screen.blit(resources.defeat_gfx, (self.window_size[0]/2-85, self.window_size[1]/2-28))
        if self.countin < 0 and self.countin > -30:
            screen.blit(resources.go_gfx, (self.window_size[0]/2-85, self.window_size[1]/2-28-200))
    
    def on_draw(self, screen):
        self.draw(screen)
        self.background.set_alpha(self.fade.alpha)
        screen.blit(self.background, (0, 0))

class TitleScreen(GameScene):
    def __init__(self, director, window_size):
        super(TitleScreen, self).__init__(director)
        self.window_size = window_size
        self.screen = director.screen
        
        # frame rate recording
        self.avgframerate = -1
        self.frsamples = 0
        
        # fade in/out
        self.fade = FadeInOut(15)
        
        # Music
        pygame.mixer.music.load(resources.musicpaths['electrodoodle'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        # Background
        self.background = pygame.Surface(window_size)
        self.background.fill((0,0,0))
        self.background.convert()
        
        self.last_event = BoardEvent(1.0, 1.0, 1.0, 1.0, 0, 0)
    
    def on_switchto(self, switchtoargs):
        
        global board
        
        if len(switchtoargs) == 0: # starting game, connect to board
            
            self.synch = False
            self.weight_on = False
            self.exiting = False
            
            self.screen.blit(resources.title_gfx[0], (self.window_size[0]/2-320, 0))
            pygame.display.flip()
            
            # connect to balance board
            board = Wiiboard()
            #print "Discovering board..."
            address = board.discover()
            
            try:
                # Disconnect already-connected devices.
                # This is basically Linux black magic just to get the thing to work.
                subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
                subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
            except:
                pass
            
            #print "Trying to connect..."
            board.connect(address)  # The wii board must be in sync mode at this time
            board.wait(200)
            # Flash the LED so we know we can step on.
            board.setLight(False)
            board.wait(500)
            board.setLight(True)
            
            if not board.status == "Connected":
                self.director.change_scene(None, [])
                self.background.fill((0,0,0))
                self.fade.FadeIn()
                return
            
            # start providing measurements
            board.start_service()
        
        self.screen.blit(resources.title_gfx[1], (self.window_size[0]/2-320, 0))
        pygame.display.flip()
        
        # wait for player to step on board
        stepped_on = False
        good_count = 0
        while not stepped_on:
            try:
                event = board.EventQueue.get_nowait()
                qsize = board.EventQueue.qsize()
                for j in xrange(qsize):
                    event2 = board.EventQueue.get()
                self.last_event = event
                if event.totalWeight > 20.0:
                    good_count += 1
                
            except Queue.Empty:
                event = self.last_event
            
            if good_count > 10:
                stepped_on = True
        
        self.displaytype = 2
        self.exiting = True
        
        # Fade in game
        self.background.fill((0,0,0))
        self.fade.FadeIn()
    
    def on_update(self):
        
        # framerate tracking
        self.frsamples += 1
        if self.frsamples == 1:
            self.avgframerate = self.director.framerate
        else:
            self.avgframerate = self.avgframerate + (self.director.framerate - self.avgframerate)/(self.frsamples)
        
        # Control fade in/out, look for end game cues
        self.fade.Update()
        if self.exiting and self.fade.direction == 'in':
            self.fade.FadeOut(False)
        if self.fade.finished_out:
            self.director.change_scene('maingame', [0]) # go to level 0
        
    def on_event(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.director.change_scene(None, [])
            if event.type == KEYDOWN:
                if not self.synch:
                    self.synch = True
                    return
                elif not self.weight_on:
                    self.weight_on = True
                    return
    
    def draw(self, screen):
        screen.blit(resources.title_gfx[self.displaytype], (self.window_size[0]/2-320, 0))
    
    def on_draw(self, screen):
        self.draw(screen)
        self.background.set_alpha(self.fade.alpha)
        screen.blit(self.background, (0, 0))

