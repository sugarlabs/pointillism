#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Pointillism
# Copyright (C) 2008, Nirav Patel
# Copyright (C) 2011, 2012, Alan Aguiar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar <alanjas@gmail.com>
# Nirav Patel <sugarlabs@spongezone.net>

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random
try:
    import pygame
    from pygame import camera
except (ImportError, ModuleNotFoundError):
    print('Error in import Pygame. This activity requires Pygame 1.9')

class Puntillism():

    def __init__(self, parent):
        self.parent = parent
        self.file_path = "NULL"

    def poner_radio1(self, radio):
        self.radio1 = radio

    def poner_radio2(self, radio):
        self.radio2 = radio

    def run(self):
        #size = (1200,900)
        pygame.init()
        pygame.camera.init()
        #camera.init()
        self.radio1 = 2
        self.radio2 = 12
        self.camNotFound_holder = False  # create a local variable to check camera not found and in loop

        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        pygame.display.flip()

        x_s, y_s = (1200, 900)
        x_s, y_s = screen.get_size()

        clock = pygame.time.Clock()
        self.running = True
        self.camfound = False
        try:
            cam = camera.Camera("/dev/video0", (640, 480), "RGB")
            cam.start()
            self.camfound = True
        except SystemError:
            self.running = False
            self.camfound = False
            
        try:
            cam.set_controls(hflip=True)
        except SystemError:
            pass

        cap = pygame.surface.Surface((640, 480), 0, screen)
        frames = 0
        
        if self.running:
            screen.fill((0,0,0))
            pygame.display.update()

        while self.running:
            cap = cam.get_image(cap)
            rect = []
            self.create_rect(cap, rect, frames, clock,screen,x_s, y_s)

            #GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            events = pygame.event.get()
            self.read_events(events,screen)

        # define some colors for not cam found
        green0 = (0, 255, 0) 
        white0 = (255, 255, 255) 
        blue0 = (0, 0, 128) 
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Camera not found', True, green0, blue0) 
        textRect = text.get_rect() 
        textRect.center = (x_s // 2, y_s // 2)

        if not self.camfound:
            print("LOG: No /dev/video0 found")
            self.camNotFound_holder = True
        
        # after checking if camera exists, cam is not accepted if /dev/video0 > null
        # Usually null gives a black screen, before initiating the display
        # A black screen is filled 
        screen.fill((0,0,0))
        pygame.display.update()

        if self.camNotFound_holder:
            self.camNotFoundHandler(screen,frames, x_s, y_s, clock, text, textRect)

    def create_rect(self, cad, rect, frames, clock, screen, x_size, y_size):
        for z in range(max(20, int(frames)*10)):
            x = random.random()
            y = random.random()
            if self.radio1 > self.radio2:
                aux = self.radio2
                self.radio2 = self.radio1
                self.radio1 = aux
            elif self.radio1 == self.radio2:
                self.radio2 = self.radio2 + 1
            num = random.randrange(self.radio1, self.radio2, 1)
            
            rect.append(pygame.draw.circle(screen, cad.get_at((int(x * 640), int(y * 480))), (int(x * x_size), int(y * y_size)), num, 0))
        pygame.display.update(rect)
        clock.tick()
        frames = clock.get_fps()
    
    def read_events(self, events, screen):
        for event in events:
            
            if event.type == pygame.QUIT:
                self.running = False
                self.camNotFound_holder = False
                
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.camNotFound_holder = False
    
                elif event.key == pygame.K_s:
                    self.parent.save_image(screen)

            elif event.type == pygame.USEREVENT:

                if hasattr(event,'action'):

                    if event.action == 'savebutton':
                        self.parent.save_image(screen)

                    if event.action == 'openbutton':
                        self.file_path = self.parent.choose_image_from_journal_cb()
                        screen.fill((0,0,0)) 
                        pygame.display.update()
                        self.running = False
                        self.camNotFound_holder = True
                        

    def camNotFoundHandler(self, screen, frames, x_s, y_s, clock, text, textRect):
        while self.camNotFound_holder:
            
            if self.file_path != "NULL":           
                cad = pygame.image.load(self.file_path).convert_alpha()
                cad = pygame.transform.scale(cad, (640,480))
                rect = []
                self.create_rect(cad, rect, frames, clock,screen,x_s, y_s)

            else:
                screen.fill((0,0,0)) 
                screen.blit(text, textRect) 
                pygame.display.update()

            #GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            events = pygame.event.get()
            self.read_events(events, screen)
                        
                        

                            
