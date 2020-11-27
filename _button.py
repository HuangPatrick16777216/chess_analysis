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


class Button:
    def __init__(self, colors, text, border, border_col):
        self.colors = colors
        self.text = text
        self.text_dims = (text.get_width(), text.get_height())
        self.border = border
        self.border_col = border_col

    def draw(self, window, events, loc, size):
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
                    break

        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            bg_col = self.colors[1] if clicked else self.colors[2]
        else:
            bg_col = self.colors[0]

        pygame.draw.rect(window, bg_col, (loc[0], loc[1], size[0], size[1]))
        pygame.draw.rect(window, self.border_col, (loc[0], loc[1], size[0], size[1]), self.border)
        window.blit(self.text, (loc[0]+(size[0]-self.text_dims[0]) / 2, loc[1]+(size[1]-self.text_dims[1]) / 2))