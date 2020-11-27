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
import chess
from _constants import *


class Board:
    def __init__(self):
        self.position = chess.Board()
        self.flipped = False

    def draw(self, window, events, loc, size):
        sq_size = size / 8
        window.blit(self.draw_squares(sq_size), loc)
        window.blit(self.draw_pieces(sq_size), loc)

        self.update(events)
        
    def draw_squares(self, sq_size):
        size = int(sq_size * 8)
        surface = pygame.Surface((size, size))

        for row in range(8):
            for col in range(8):
                curr_loc = (col*sq_size, row*sq_size)
                color = BOARD_WHITE if (row+col) % 2 == 0 else BOARD_BLACK
                pygame.draw.rect(surface, color, curr_loc+(sq_size+1, sq_size+1))

        return surface

    def draw_pieces(self, sq_size):
        size = int(sq_size * 8)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        piece_size = int(sq_size * 0.9)
        piece_offset = sq_size * 0.05
        for row in range(8):
            for col in range(8):
                piece = self.position.piece_at(8 * (7-row) + col)
                if piece is not None:
                    image = pygame.transform.scale(IMAGES[piece.symbol()], (piece_size, piece_size))
                    if self.flipped:
                        image = pygame.transform.rotate(image, 180)
                    curr_loc = (col*sq_size + piece_offset, row*sq_size + piece_offset)
                    surface.blit(image, curr_loc)

        if self.flipped:
            surface = pygame.transform.rotate(surface, 180)
        return surface

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.flipped = not self.flipped