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
from math import sin, cos, pi, sqrt
import utils

def view(game):
    vw = game.vw
    vh = game.vh
    screen = game.gameDisplay

    CIRCLE_COLOR = (0, 0, 0)
    CIRCLE_COLORS = [
                    (25, 25, 25),    # Very dark gray
                    (34, 32, 52),    # Dark indigo
                    (44, 62, 80),    # Dark blue-gray
                    (52, 73, 94),    # Dark slate blue
                    (46, 49, 49),    # Charcoal
                    (66, 73, 73),    # Dark gray-green
                    (70, 56, 37),    # Dark brown
                    (39, 55, 70),    # Steel blue
                    (51, 51, 51),    # Dark gray
                    (29, 32, 33),    # Gunmetal
                    (54, 54, 54),    # Iron gray
                    (45, 63, 81),    # Midnight blue
                    (60, 60, 60),    # Ash gray
                    (50, 50, 50),    # Granite gray
                    (38, 34, 98),    # Navy
                    (62, 55, 64),    # Dark plum
                    (45, 45, 45),    # Slate gray
                    (55, 42, 42),    # Dark mahogany
                    (31, 44, 53),    # Deep sea blue
                    (34, 47, 62)     # Blue black
                ]
    CENTER_X = vw(23)
    CENTER_Y = vh(50)
    MAX_RADIUS = vw(10)
    STROKE_WIDTH = 2
    SPEED = 1 / 50
    LINE_X = CENTER_X + MAX_RADIUS * 2

    step = 0

    wave = []

    def draw():
        x = CENTER_X
        y = CENTER_Y
        prev_x = x
        prev_y = y

        for i in range(5):
            n = 2 * i + 1

            x += int(MAX_RADIUS * (4 / (n * pi) * cos(n * step)))
            y += int(MAX_RADIUS * (4 / (n * pi) * sin(n * step)))

            rad = int(sqrt((prev_x - x) ** 2 + (prev_y - y) ** 2))

            pygame.draw.circle(screen, CIRCLE_COLOR, (prev_x, prev_y), rad, STROKE_WIDTH)
            pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 3)

            prev_x = x
            prev_y = y

        wave.insert(0, y)
        pygame.draw.line(screen, (150, 150, 180), (x, y), (LINE_X, y), 2)

        for i in range(len(wave)):
            pygame.draw.circle(screen, CIRCLE_COLOR, (LINE_X + i, wave[i]), 2)

        # if len(wave) >= 2:
        #     points = [(LINE_X + i, wave[i]) for i in range(len(wave)) if i % 8 == 0] 
        #     utils.draw_bezier_curve(screen, points)


    def update():
        nonlocal step
        step += SPEED

        if len(wave) > vw(50):
            wave.pop()

        draw()

    game.update_function = update
