# Copyright (C) 2024 Spandan Barve
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


import pygame
from gi.repository import Gtk
from config import Config
from views import simulation
from font import Font

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class FourierSim:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.config = Config()

        self.gameDisplay = None
        self.info = None
        self.update_function = None
        self.events = []        
        self.font = Font()


    def vw(self, x):
        return (x * self.display_rect.width) // 100

    def vh(self, y):
        return (y * self.display_rect.height) // 100

    def blit_centred(self, surf, x, y):
        rect = surf.get_rect()
        centered_coords = (x - rect.width // 2, y - rect.height // 2)
        self.gameDisplay.blit(surf, centered_coords)

    def stop(self):
        self.running = False

    def set_screen(self, view):
        view(self)

    def show_help(self):
        self.help_popup.show()

    def hide_help(self):
        self.help_popup.hide()

    def run(self):
        self.gameDisplay = pygame.display.get_surface()
        self.info = pygame.display.Info()
        self.display_rect = self.gameDisplay.get_rect()

        self.font.intialize("./Geist.ttf")
        self.set_screen(simulation.view)

        if not self.gameDisplay:
            self.gameDisplay = pygame.display.set_mode(
                (self.info.current_w, self.info.current_h))
            pygame.display.set_caption("Fourier Series Visualisation")
        
        while self.running:
            self.gameDisplay.fill(BLACK if self.config.dark else WHITE)

            if self.update_function is not None:
                self.update_function()

            while Gtk.events_pending():
                Gtk.main_iteration()

            self.events = []
            for event in pygame.event.get():
                self.events.append(event)
                if event.type == pygame.QUIT:
                    break

            pygame.display.update()
            self.clock.tick(self.config.fps)

        return


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    fourier = FourierSim()
    fourier.run()
