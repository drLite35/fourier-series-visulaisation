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


def scale_image_maintain_ratio(img, w=None, h=None):
    o_w, o_h = img.get_size()
    m_w, m_h = o_w, o_h

    if w is not None and h is None:
        m_h = w * (o_h / o_w)
        return pygame.transform.scale(img, (int(w), int(m_h)))

    if h is not None and w is None:
        m_w = h * (o_w / o_h)
        return pygame.transform.scale(img, (int(m_w), int(h)))

    if w is None and h is None:
        return img


def array_has_no_none(arr):
    return all(element is not None for element in arr)


def compare_arrays_unordered(*arrays):
    sets = [set(arr) for arr in arrays]
    return all(s == sets[0] for s in sets)


def rotate_by_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect

def lerp(p1, p2, t):
    return (1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1]

def draw_catmull_rom_spline(screen, points, offset = 0, color=(255, 255, 255), num_segments=100,):
    for i in range(1, len(points) - 2):
        x0, x1, x2, x3 = offset + i - 1, offset + i, offset + i + 1, offset + i + 2
        y0, y1, y2, y3 = points[i-1], points[i], points[i+1], points[i+2]
        for t in range(num_segments):
            t /= num_segments
            t2 = t * t
            t3 = t2 * t

            x = 0.5 * (2*x1 + (-x0 + x2)*t + (2*x0 - 5*x1 + 4*x2 - x3)*t2 + (-x0 + 3*x1 - 3*x2 + x3)*t3)
            y = 0.5 * (2*y1 + (-y0 + y2)*t + (2*y0 - 5*y1 + 4*y2 - y3)*t2 + (-y0 + 3*y1 - 3*y2 + y3)*t3)

            pygame.draw.circle(screen, color, (int(x), int(y)), 1)
