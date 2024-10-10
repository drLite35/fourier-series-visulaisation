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
    font = game.font

    width = vw(100)
    height = vh(100)

    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (140, 140, 140)

    BTN_W = vw(6)
    BTN_H = vh(5)

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
    PLUS = font.lg.render(f"+", True, TEXT_COLOR)
    MINUS = font.lg.render(f"-", True, TEXT_COLOR)

    SPEED_STEP = 1 / 800
    speed = 1 / 100
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

    CTRLS_Y = vh(5)

    freq_dec_rect = pygame.Rect((vw(5), CTRLS_Y), (BTN_W, BTN_H))
    freq_label = font.lg.render(f"Frequency", True, TEXT_COLOR)
    freq_inc_rect = pygame.Rect((vw(5) + BTN_W + 4, CTRLS_Y), (BTN_W, BTN_H))

    circles_dec_rect = pygame.Rect((vw(5), CTRLS_Y), (BTN_W, BTN_H))
    circles_label = font.lg.render(f"Circles / Accuracy", True, TEXT_COLOR)
    circles_inc_rect = pygame.Rect((vw(5) + BTN_W + 4, CTRLS_Y), (BTN_W, BTN_H))

    def draw_controls():
        pygame.draw.rect(screen, BUTTON_COLOR, freq_dec_rect)
        game.blit_centred(MINUS, freq_dec_rect.center)
        pygame.Surface.blit(screen, freq_label, (freq_dec_rect.x, CTRLS_Y - 26), area=None, special_flags = 0)
        pygame.draw.rect(screen, BUTTON_COLOR, freq_inc_rect)
        game.blit_centred(PLUS, freq_inc_rect.center)

    def handle_controls():
        nonlocal speed
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if freq_dec_rect.collidepoint(mouse_pos):
                    speed = max(1 / 1000,speed  - SPEED_STEP)
                if freq_inc_rect.collidepoint(mouse_pos):
                    speed = min(1 / 5, speed + SPEED_STEP)

    def draw():
        x = CENTER_X
        y = CENTER_Y
        prev_x = x
        prev_y = y

        draw_controls()

        for i in range(num_circles):
            n = 2 * i + 1

            x += int(MAX_RADIUS * (4 / (n * pi) * cos(n * -step)))
            y += int(MAX_RADIUS * (4 / (n * pi) * sin(n * -step)))

            rad = int(sqrt((prev_x - x) ** 2 + (prev_y - y) ** 2))

            clr = CIRCLE_COLORS[i % len(CIRCLE_COLORS)]

            pygame.draw.line(screen, CIRCLE_COLOR, (prev_x, prev_y), (x, y), 1)

            pygame.draw.circle(screen, CIRCLE_COLOR, (prev_x, prev_y), rad, STROKE_WIDTH + 1)
            pygame.draw.circle(screen, CIRCLE_COLOR, (prev_x, prev_y), rad + 1, STROKE_WIDTH)
            pygame.draw.circle(screen, clr, (prev_x, prev_y), rad, STROKE_WIDTH)

            pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 3)

            prev_x = x
            prev_y = y

        wave.insert(0, y)
        if len(wave) >= 3:
            utils.draw_catmull_rom_spline(screen, wave, LINE_X, CIRCLE_COLOR, 5)

        pygame.draw.line(screen, (200, 200, 220), (x + 3, y), (LINE_X, y), 3)
        pygame.draw.circle(screen, (200, 200, 223), (LINE_X, y), 8)


    def update():
        nonlocal step
        step += speed

        if len(wave) > LINE_W:
            wave.pop()

        handle_controls()
        draw()

    game.update_function = update
