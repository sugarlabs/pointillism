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
from sugar3 import mime
from sugar3.graphics.objectchooser import ObjectChooser
from sugar3.datastore import datastore

try:
    import pygame
    from pygame import camera
except (ImportError, ModuleNotFoundError):
    print('Error in import Pygame. This activity requires Pygame 1.9')

class Puntillism():

    def __init__(self, parent):
        self.parent = parent
        #global file_path
        self.file_path = "NULL"
        #logging.basicConfig()

    def poner_radio1(self, radio):
        self.radio1 = radio

    def poner_radio2(self, radio):
        self.radio2 = radio

    def _choose_image_from_journal_cb(self, button):
        ''' Create a chooser for image objects '''

        self.image_id = None
        chooser = ObjectChooser(what_filter=mime.GENERIC_TYPE_IMAGE)
        result = chooser.run()
        if result == Gtk.ResponseType.ACCEPT:
            jobject = chooser.get_selected_object()
            self.image_id = str(jobject._object_id)
        print(str(jobject.get_file_path()))
        puntillism.Puntillism.file_path = str(jobject.get_file_path())
        return str(jobject.get_file_path())

    def run(self):
        #size = (1200,900)
        pygame.init()
        pygame.camera.init()
        #camera.init()

        self.radio1 = 2
        self.radio2 = 12

        camNotFound_holder = False  # create a local variable to check camera not found and in loop

        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        pygame.display.flip()

        x_s, y_s = (1200, 900)
        x_s, y_s = screen.get_size()

        clock = pygame.time.Clock()
        running = True
        camfound = False
        try:
            cam = camera.Camera("/dev/video0", (640, 480), "RGB")
            cam.start()
            camfound = True
            
        except SystemError:
            running = False
            camfound = False
        try:
            cam.set_controls(hflip=True)
        except SystemError:
            pass

        cap = pygame.surface.Surface((640, 480), 0, screen)
        frames = 0
        
        if not camfound:
            # define some colors for not cam found
            green0 = (0, 255, 0) 
            white0 = (255, 255, 255) 
            blue0 = (0, 0, 128) 
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Camera not found', True, green0, blue0) 
            textRect = text.get_rect() 
            textRect.center = (x_s // 2, y_s // 2)
            print("LOG: No /dev/video0 found")
            camNotFound_holder = True
            screen.fill((0,0,0))
            pygame.display.update() 
        
        while (not camfound) and camNotFound_holder:
            
            if self.file_path != "NULL":
                  
                cad = pygame.image.load(self.file_path).convert_alpha()
                cad = pygame.transform.scale(cad, (640,480))
                rect = []
                self.create_rect(cad, rect)

            else:
                screen.fill((0,0,0)) 
                screen.blit(text, textRect) 
                pygame.display.update()

            #GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            events = pygame.event.get()
            self.read_events(events)

        # after checking if camera exists, cam is not accepted if /dev/video0 > null
        # Usually null gives a black screen, before initiating the display
        # A black screen is filled 

        if running:
            screen.fill((0,0,0))
            pygame.display.update()

        while running:
            cap = cam.get_image(cap)
            rect = []
            self.create_rect(cap, rect)

            #GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            events = pygame.event.get()
            self.read_events(events)

    def create_rect(self, cad, rect)
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
            
            rect.append(pygame.draw.circle(screen, cad.get_at((int(x * 640), int(y * 480))), (int(x * x_s), int(y * y_s)), num, 0))
        pygame.display.update(rect)
        clock.tick()
        frames = clock.get_fps()
    
    def read_events(self, events):
        for event in events:
            
            if event.type == pygame.QUIT:
                camNotFound_holder = False
                
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    camNotFound_holder = False

                elif event.key == pygame.K_s:
                    self.parent.save_image(screen)

            elif event.type == pygame.USEREVENT:

                if hasattr(event,'action'):

                    if event.action == 'savebutton':
                        self.parent.save_image(screen)

                    if event.action == 'openbutton':
                        self.file_path = self.parent.choose_image_from_journal_cb()
                        screen.fill((0,0,0)) 
