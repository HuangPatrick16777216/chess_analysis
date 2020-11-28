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


class Checkbox:
    def __init__(self, init_val, text):
        self.text = text
        self.value = init_val

    def draw(self, window, events, loc, box_size):
        window.blit(self.text, (loc[0] + box_size+10, loc[1] - self.text.get_height()/2))
        pygame.draw.circle(window, WHITE, loc, box_size)
        if not self.value:
            pygame.draw.circle(window, CYAN, loc, box_size - 2)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if loc[0]-box_size <= mouse_pos[0] <= loc[0]+box_size and loc[1]-box_size <= mouse_pos[1] <= loc[1]+box_size:
                    self.value = not self.value