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
import chess.pgn
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from _constants import *
from _button import Button
Tk().withdraw()


class Board:
    button_load_pgn = Button((WHITE, GRAY_LIGHT, GRAY_DARK), FONT_SMALL.render("Load PGN", 1, BLACK), 3, GRAY)

    def __init__(self):
        self.position = chess.Board()
        self.flipped = False
        self.pgn_loaded = False
        self.pgn_moves = None
        self.pgn_curr_move = 0

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

    def draw_elements(self, window, events, loc, size):
        self.button_load_pgn.draw(window, events, ((loc[0] + size[0] / 2 - 100, loc[1]+25)), (200, 50))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.flipped = not self.flipped

                elif event.key == pygame.K_LEFT:
                    self.pgn_curr_move = max(self.pgn_curr_move-1, 0)
                    self.update_pgn_move()
                elif event.key == pygame.K_RIGHT:
                    self.pgn_curr_move = min(self.pgn_curr_move+1, len(self.pgn_moves))
                    self.update_pgn_move()

        if self.button_load_pgn.clicked(events):
            self.load_pgn()

    def load_pgn(self):
        path = askopenfilename()
        if path == "":
            return

        with open(path, "r") as pgn:
            self.pgn_moves = list(chess.pgn.read_game(pgn).mainline_moves())
        self.pgn_curr_move = 0
        self.pgn_loaded = True
        self.update_pgn_move()

    def update_pgn_move(self):
        if not self.pgn_loaded:
            return

        self.position = chess.Board()
        for move in self.pgn_moves[:self.pgn_curr_move]:
            self.position.push(move)