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

import os
import pygame
pygame.init()

PARDIR = os.path.realpath(os.path.dirname(__file__))
SCREEN = (1280, 720)
FPS = 60
IMAGES = {}

BLACK = (0, 0, 0)
BOARD_WHITE = (220, 220, 210)
BOARD_WHITE_SELECT = (240, 240, 200)
BOARD_WHITE_MARK = (190, 190, 180)
BOARD_BLACK = (90, 140, 70)
BOARD_BLACK_SELECT = (140, 180, 80)
BOARD_BLACK_MARK = (70, 120, 50)

for file in os.listdir(os.path.join(PARDIR, "images")):
    if file.endswith(".png"):
        name = file.replace(".png", "")
        image = pygame.image.load(os.path.join(PARDIR, "images", file))
        if len(name) == 2 and name[0] in ("w", "b"):
            new_name = name[1].upper() if name[0] == "w" else name[1].lower()
            IMAGES[new_name] = image
        else:
            IMAGES[name] = image