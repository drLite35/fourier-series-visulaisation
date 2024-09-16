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
        (160, 0, 200),
        (135, 206, 235),
        (220, 225, 30),
        (200, 100, 100),
        (100, 200, 100),
        (100, 100, 200),
        (100, 200, 200),
        (200, 100, 200),
        (200, 200, 100),
        (150, 200, 150),
    ]
    MAX_RADIUS = vw(10)
    STROKE_WIDTH = 2
    SPEED = 1 / 100

    num_circles = 6

    total_radius = 0
    for i in range(num_circles):
        n = 2 * i + 1
        radius_contribution = MAX_RADIUS * (4 / (n * pi))
        total_radius += radius_contribution
    total_radius = int(total_radius)

    CENTER_X = total_radius + 32
    CENTER_Y = vh(60)
    LINE_X = CENTER_X * 2
    LINE_W = vw(100) - LINE_X - 20

    step = 0

    wave = []

    def draw():
        x = CENTER_X
        y = CENTER_Y
        prev_x = x
        prev_y = y

        for i in range(num_circles):
            n = 2 * i + 1

            x += int(MAX_RADIUS * (4 / (n * pi) * cos(n * -step)))
            y += int(MAX_RADIUS * (4 / (n * pi) * sin(n * -step)))

            rad = int(sqrt((prev_x - x) ** 2 + (prev_y - y) ** 2))

            clr = CIRCLE_COLORS[i % len(CIRCLE_COLORS)]

            pygame.draw.circle(screen, CIRCLE_COLOR, (prev_x, prev_y), rad, STROKE_WIDTH + 1)
            pygame.draw.circle(screen, CIRCLE_COLOR, (prev_x, prev_y), rad + 1, STROKE_WIDTH)
            pygame.draw.circle(screen, clr, (prev_x, prev_y), rad, STROKE_WIDTH)
            pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 3)

            prev_x = x
            prev_y = y

        wave.insert(0, y)
        pygame.draw.line(screen, (200, 200, 220), (x + 3, y), (LINE_X, y), 3)

        if len(wave) >= 3:
            utils.draw_catmull_rom_spline(screen, wave, LINE_X, CIRCLE_COLOR, 5)


    def update():
        nonlocal step
        step += SPEED

        if len(wave) > LINE_W:
            wave.pop()

        draw()

    game.update_function = update
