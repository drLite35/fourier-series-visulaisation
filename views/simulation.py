# Copyright (C) 2024 Spandan Barve

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see .

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
    
    # Colors - now dependent on theme
    def update_colors():
        nonlocal TEXT_COLOR, BUTTON_COLOR, CIRCLE_COLOR, BG_COLOR, WAVE_COLOR, HIGHLIGHT_COLOR
        if game.config.dark:
            TEXT_COLOR = (255, 255, 255)
            BUTTON_COLOR = (80, 80, 80)
            CIRCLE_COLOR = (255, 255, 255)
            BG_COLOR = (20, 20, 30)
            WAVE_COLOR = (200, 200, 220)
            HIGHLIGHT_COLOR = (100, 100, 150)
        else:
            TEXT_COLOR = (0, 0, 0)
            BUTTON_COLOR = (140, 140, 140)
            CIRCLE_COLOR = (0, 0, 0)
            BG_COLOR = (240, 240, 245)
            WAVE_COLOR = (100, 100, 120)
            HIGHLIGHT_COLOR = (180, 180, 220)
    
    # Initial color setup
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (140, 140, 140)
    CIRCLE_COLOR = (0, 0, 0)
    BG_COLOR = (240, 240, 245)
    WAVE_COLOR = (100, 100, 120)
    HIGHLIGHT_COLOR = (180, 180, 220)
    update_colors()
    
    BTN_W = vw(6)
    BTN_H = vh(5)
    
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
    
    # State variables
    speed = 1 / 100
    num_circles = 6
    step = 0
    wave = []
    drawing_mode = False
    user_drawn_wave = []
    animation_speed = 1.0
    show_explanation = False
    selected_circle = None
    quality_level = 1  # Medium by default
    quality_options = ["Low", "Medium", "High"]
    spline_segments = [3, 5, 10][quality_level]
    show_coefficients = True
    
    # Calculate total radius for proper positioning
    def calculate_total_radius():
        total = 0
        for i in range(num_circles):
            n = 2 * i + 1
            radius_contribution = MAX_RADIUS * (4 / (n * pi))
            total += radius_contribution
        return int(total)
    
    total_radius = calculate_total_radius()
    CENTER_X = total_radius + 32
    CENTER_Y = vh(60)
    LINE_X = CENTER_X * 2
    LINE_W = vw(100) - LINE_X - 20
    
    # Control positions
    CTRLS_Y = vh(5)
    
    # Basic controls
    freq_dec_rect = pygame.Rect((vw(5), CTRLS_Y), (BTN_W, BTN_H))
    freq_label = font.lg.render(f"Frequency", True, TEXT_COLOR)
    freq_inc_rect = pygame.Rect((vw(5) + BTN_W + 4, CTRLS_Y), (BTN_W, BTN_H))
    
    circles_dec_rect = pygame.Rect((vw(20), CTRLS_Y), (BTN_W, BTN_H))
    circles_label = font.lg.render(f"Circles / Accuracy", True, TEXT_COLOR)
    circles_inc_rect = pygame.Rect((vw(20) + BTN_W + 4, CTRLS_Y), (BTN_W, BTN_H))
    
    # New controls
    theme_toggle_rect = pygame.Rect((vw(35), CTRLS_Y), (BTN_W*1.5, BTN_H))
    theme_label = font.md.render(f"Theme", True, TEXT_COLOR)
    
    # Preset buttons
    preset_y = CTRLS_Y + BTN_H + vh(8)
    square_btn = pygame.Rect((vw(5), preset_y), (BTN_W*1.5, BTN_H))
    sawtooth_btn = pygame.Rect((vw(15), preset_y), (BTN_W*1.5, BTN_H))
    triangle_btn = pygame.Rect((vw(25), preset_y), (BTN_W*1.5, BTN_H))
    
    # Animation speed control
    speed_slider_rect = pygame.Rect((vw(45), CTRLS_Y), (vw(15), vh(2)))
    speed_handle_rect = pygame.Rect((vw(45) + (animation_speed * vw(15)), CTRLS_Y - vh(1)), (vw(2), vh(4)))
    speed_label = font.md.render(f"Animation Speed", True, TEXT_COLOR)
    
    # Drawing mode toggle
    drawing_btn = pygame.Rect((vw(65), CTRLS_Y), (BTN_W*1.8, BTN_H))
    
    # Help/explanation toggle
    help_btn = pygame.Rect((vw(75), CTRLS_Y), (BTN_W*1.5, BTN_H))
    
    # Quality selector
    quality_btn = pygame.Rect((vw(35), preset_y), (BTN_W*1.5, BTN_H))
    
    # Coefficient display toggle
    coef_btn = pygame.Rect((vw(45), preset_y), (BTN_W*2, BTN_H))
    
    # Explanation text
    explanation_text = [
        "The Fourier series represents periodic functions as sums of sines and cosines.",
        "More circles (higher n) create more accurate approximations.",
        "Each circle represents a term in the series: a_n*cos(nx) + b_n*sin(nx).",
        "The square wave is approximated by: 4/π * (sin(x) + sin(3x)/3 + sin(5x)/5 + ...)",
        "The sawtooth wave is approximated by: 2/π * (sin(x) - sin(2x)/2 + sin(3x)/3 - ...)",
        "The triangle wave is approximated by: 8/π² * (sin(x) - sin(3x)/9 + sin(5x)/25 - ...)"
    ]
    
    # Preset wave coefficients
    def set_square_wave():
        nonlocal num_circles, wave
        num_circles = min(10, num_circles)  # Limit for performance
        wave = []  # Reset wave
    
    def set_sawtooth_wave():
        nonlocal num_circles, wave
        num_circles = min(10, num_circles)  # Limit for performance
        wave = []  # Reset wave
    
    def set_triangle_wave():
        nonlocal num_circles, wave
        num_circles = min(10, num_circles)  # Limit for performance
        wave = []  # Reset wave
    
    def toggle_theme():
        game.config.dark = not game.config.dark
        update_colors()
    
    def draw_controls():
        # Update text colors based on theme
        freq_label_surf = font.lg.render(f"Frequency", True, TEXT_COLOR)
        circles_label_surf = font.lg.render(f"Circles / Accuracy", True, TEXT_COLOR)
        theme_label_surf = font.md.render(f"Theme: {'Dark' if game.config.dark else 'Light'}", True, TEXT_COLOR)
        speed_label_surf = font.md.render(f"Animation Speed", True, TEXT_COLOR)
        drawing_label = font.md.render(f"{'✏️ Drawing Mode' if drawing_mode else '📊 Wave Mode'}", True, TEXT_COLOR)
        help_label = font.md.render(f"{'Hide Help' if show_explanation else 'Show Help'}", True, TEXT_COLOR)
        quality_label = font.md.render(f"Quality: {quality_options[quality_level]}", True, TEXT_COLOR)
        coef_label = font.md.render(f"{'Hide' if show_coefficients else 'Show'} Coefficients", True, TEXT_COLOR)
        
        # Basic controls
        pygame.draw.rect(screen, BUTTON_COLOR, freq_dec_rect)
        game.blit_centred(MINUS, freq_dec_rect.center)
        pygame.Surface.blit(screen, freq_label_surf, (freq_dec_rect.x, CTRLS_Y - 26), area=None, special_flags=0)
        pygame.draw.rect(screen, BUTTON_COLOR, freq_inc_rect)
        game.blit_centred(PLUS, freq_inc_rect.center)
        
        pygame.draw.rect(screen, BUTTON_COLOR, circles_dec_rect)
        game.blit_centred(MINUS, circles_dec_rect.center)
        pygame.Surface.blit(screen, circles_label_surf, (circles_dec_rect.x, CTRLS_Y - 26), area=None, special_flags=0)
        pygame.draw.rect(screen, BUTTON_COLOR, circles_inc_rect)
        game.blit_centred(PLUS, circles_inc_rect.center)
        
        # Theme toggle
        pygame.draw.rect(screen, BUTTON_COLOR, theme_toggle_rect)
        game.blit_centred(theme_label_surf, theme_toggle_rect.center)
        
        # Preset buttons
        pygame.draw.rect(screen, BUTTON_COLOR, square_btn)
        square_label = font.md.render("Square Wave", True, TEXT_COLOR)
        game.blit_centred(square_label, square_btn.center)
        
        pygame.draw.rect(screen, BUTTON_COLOR, sawtooth_btn)
        sawtooth_label = font.md.render("Sawtooth Wave", True, TEXT_COLOR)
        game.blit_centred(sawtooth_label, sawtooth_btn.center)
        
        pygame.draw.rect(screen, BUTTON_COLOR, triangle_btn)
        triangle_label = font.md.render("Triangle Wave", True, TEXT_COLOR)
        game.blit_centred(triangle_label, triangle_btn.center)
        
        # Animation speed control
        pygame.draw.rect(screen, BUTTON_COLOR, speed_slider_rect)
        pygame.Surface.blit(screen, speed_label_surf, (speed_slider_rect.x, CTRLS_Y - 26), area=None, special_flags=0)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, speed_handle_rect)
        
        # Drawing mode toggle
        pygame.draw.rect(screen, BUTTON_COLOR, drawing_btn)
        game.blit_centred(drawing_label, drawing_btn.center)
        
        # Help button
        pygame.draw.rect(screen, BUTTON_COLOR, help_btn)
        game.blit_centred(help_label, help_btn.center)
        
        # Quality selector
        pygame.draw.rect(screen, BUTTON_COLOR, quality_btn)
        game.blit_centred(quality_label, quality_btn.center)
        
        # Coefficient display toggle
        pygame.draw.rect(screen, BUTTON_COLOR, coef_btn)
        game.blit_centred(coef_label, coef_btn.center)
    
    def display_equation():
        eq_text = "f(x) = "
        
        # Different equations based on preset type
        if num_circles > 0:
            for i in range(min(3, num_circles)):
                n = 2 * i + 1
                coef = f"{4/(n*pi):.2f}"
                if i > 0:
                    eq_text += " + "
                eq_text += f"{coef}sin({n}x)"
            
            if num_circles > 3:
                eq_text += " + ..."
        
        eq_surface = font.md.render(eq_text, True, TEXT_COLOR)
        screen.blit(eq_surface, (vw(5), vh(15)))
    
    def draw_coefficients():
        if not show_coefficients:
            return
            
        bar_width = vw(2)
        max_height = vh(15)
        x_start = vw(5)
        y_base = vh(40)
        
        # Draw coefficient bars
        for i in range(num_circles):
            n = 2 * i + 1
            coefficient = 4 / (n * pi)
            bar_height = coefficient * max_height
            
            # Draw bar
            pygame.draw.rect(screen, CIRCLE_COLORS[i % len(CIRCLE_COLORS)], 
                            (x_start + i*bar_width*2, y_base - bar_height, bar_width, bar_height))
            
            # Draw coefficient value
            coef_text = font.sm.render(f"{coefficient:.2f}", True, TEXT_COLOR)
            screen.blit(coef_text, (x_start + i*bar_width*2, y_base + 5))
            
            # Draw n value
            n_text = font.sm.render(f"n={n}", True, TEXT_COLOR)
            screen.blit(n_text, (x_start + i*bar_width*2, y_base + 20))
    
    def display_help():
        if not show_explanation:
            return
            
        # Semi-transparent background for explanation panel
        help_surface = pygame.Surface((vw(90), vh(30)))
        help_surface.set_alpha(200)
        help_surface.fill((30, 30, 40) if game.config.dark else (240, 240, 240))
        screen.blit(help_surface, (vw(5), vh(70)))
        
        # Display explanation text
        y_pos = vh(72)
        for line in explanation_text:
            text_surf = font.md.render(line, True, TEXT_COLOR)
            screen.blit(text_surf, (vw(7), y_pos))
            y_pos += vh(4)
    
    def handle_controls():
        nonlocal speed, num_circles, drawing_mode, animation_speed, show_explanation
        nonlocal quality_level, spline_segments, show_coefficients
        nonlocal selected_circle, total_radius, CENTER_X, LINE_X, LINE_W
        
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                
                # Basic controls
                if freq_dec_rect.collidepoint(mouse_pos):
                    speed = max(1 / 1000, speed - SPEED_STEP)
                
                if freq_inc_rect.collidepoint(mouse_pos):
                    speed = min(1 / 5, speed + SPEED_STEP)
                
                if circles_dec_rect.collidepoint(mouse_pos):
                    num_circles = max(1, num_circles - 1)
                    total_radius = calculate_total_radius()
                    CENTER_X = total_radius + 32
                    LINE_X = CENTER_X * 2
                    LINE_W = vw(100) - LINE_X - 20
                    wave = []  # Reset wave when changing circles
                
                if circles_inc_rect.collidepoint(mouse_pos):
                    num_circles = min(15, num_circles + 1)
                    total_radius = calculate_total_radius()
                    CENTER_X = total_radius + 32
                    LINE_X = CENTER_X * 2
                    LINE_W = vw(100) - LINE_X - 20
                    wave = []  # Reset wave when changing circles
                
                # Theme toggle
                if theme_toggle_rect.collidepoint(mouse_pos):
                    toggle_theme()
                
                # Preset buttons
                if square_btn.collidepoint(mouse_pos):
                    set_square_wave()
                
                if sawtooth_btn.collidepoint(mouse_pos):
                    set_sawtooth_wave()
                
                if triangle_btn.collidepoint(mouse_pos):
                    set_triangle_wave()
                
                # Drawing mode toggle
                if drawing_btn.collidepoint(mouse_pos):
                    drawing_mode = not drawing_mode
                    if drawing_mode:
                        user_drawn_wave = []
                    else:
                        wave = []  # Reset wave when switching modes
                
                # Help button
                if help_btn.collidepoint(mouse_pos):
                    show_explanation = not show_explanation
                
                # Quality selector
                if quality_btn.collidepoint(mouse_pos):
                    quality_level = (quality_level + 1) % len(quality_options)
                    spline_segments = [3, 5, 10][quality_level]
                
                # Coefficient display toggle
                if coef_btn.collidepoint(mouse_pos):
                    show_coefficients = not show_coefficients
            
            # Handle speed slider
            if event.type == pygame.MOUSEBUTTONDOWN:
                if speed_slider_rect.collidepoint(event.pos):
                    animation_speed = (event.pos[0] - speed_slider_rect.x) / speed_slider_rect.width
                    animation_speed = max(0.1, min(1.0, animation_speed))
                    speed_handle_rect.x = speed_slider_rect.x + (animation_speed * speed_slider_rect.width) - speed_handle_rect.width/2
            
            # Handle drawing mode
            if drawing_mode and event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if LINE_X <= event.pos[0] <= LINE_X + LINE_W:
                    user_drawn_wave.append(event.pos[1
