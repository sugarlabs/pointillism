#! /usr/bin/env python
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
except ImportError:
    print 'Error in import Pygame. This activity requires Pygame 1.9'

class Puntillism():

    def __init__(self, parent):
        self.parent = parent
        #logging.basicConfig()

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

        screen = pygame.display.get_surface()
        screen.fill((0,0,0))
        pygame.display.flip()

        x_s, y_s = (1200, 900)
        x_s, y_s = screen.get_size()

        clock = pygame.time.Clock()

        cam = camera.Camera("/dev/video0", (640, 480), "RGB")
        cam.set_controls(True, False)
        cam.start()

        cap = pygame.surface.Surface((640, 480), 0, screen)
        frames = 0
        running = True
        while running:
            cap = cam.get_image(cap)
            rect = []
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
                rect.append(pygame.draw.circle(screen, cap.get_at((int(x * 640), int(y * 480))), (int(x * x_s), int(y * y_s)), num, 0))
            pygame.display.update(rect)

            clock.tick()
            frames = clock.get_fps()

            #GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            events = pygame.event.get()
            for event in events:
                #log.debug( "Event: %s", event )
                if event.type == pygame.QUIT:
                    cam.stop()
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cam.stop()
                        running = False
                    elif event.key == pygame.K_s:
                        self.parent.save_image(screen)
                elif event.type == pygame.USEREVENT:
                    if hasattr(event,'action'):
                        if event.action == 'savebutton':
                            self.parent.save_image(screen)
            #pygame.display.flip()

