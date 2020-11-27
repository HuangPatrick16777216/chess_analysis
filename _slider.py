#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
from _constants import *


class Slider:
    def __init__(self, rect_color=GRAY, circle_color=WHITE, val_range=(0, 100), init_val = 20):
        self.rect_col = rect_color
        self.circle_color = circle_color
        self.val_range = val_range
        self.val_diff = val_range[1] - val_range[0]
        self.value = init_val

        self.dragging = False

    def draw(self, window, events, loc, rect_size, circle_size):
        circle_loc = (loc[0] + (rect_size[0])/self.val_diff*(self.value-self.val_range[0]), loc[1] + (rect_size[1]) / 2)
        pygame.draw.rect(window, self.rect_col, loc+rect_size)
        pygame.draw.circle(window, self.circle_color, circle_loc, circle_size/2)

        mouse_click = False
        mouse_hold = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        if self.dragging:
            if not mouse_hold:
                self.dragging = False
            else:
                value = (mouse_pos[0]-loc[0]) / rect_size[0] * self.val_diff + self.val_range[0]
                value = round(value)
                value = max(min(value, self.val_range[1]), self.val_range[0])
                self.value = value
        
        else:
            if mouse_click:
                self.dragging = True