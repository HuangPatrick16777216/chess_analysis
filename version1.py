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
import chess
import chess.engine
import chess.pgn
from copy import deepcopy
from tkinter import Tk
from tkinter.filedialog import askopenfilename
pygame.init()
Tk().withdraw()

PARDIR = os.path.realpath(os.path.dirname(__file__))
SCREEN = (1600, 900)
FPS = 60

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

BOARD_WHITE = (220, 220, 210)
BOARD_WHITE_SELECT = (240, 240, 200)
BOARD_WHITE_MARK = (190, 190, 180)
BOARD_BLACK = (100, 140, 80)
BOARD_BLACK_SELECT = (140, 180, 80)
BOARD_BLACK_MARK = (70, 120, 50)

IMAGES = {}

for file in os.listdir(os.path.join(PARDIR, "images")):
    if file.endswith(".png"):
        image = pygame.image.load(os.path.join(PARDIR, "images", file))
        name = file.replace(".png", "")

        if len(name) == 2 and name[0] in ("b", "w"):
            name = name[1].upper() if name[0] == "w" else name[1].lower()

        IMAGES[name] = pygame.transform.scale(image, (90, 90))


class Button:
    def __init__(self, loc, size, text):
        self.loc = loc
        self.size = size
        self.text = text
        self.text_loc = (loc[0] + (size[0]-text.get_width())//2, loc[1] + (size[1]-text.get_height())//2)

    def draw(self, window, events):
        color = (GRAY_DARK if self.clicked(events) else GRAY_LIGHT) if self.hovered() else WHITE
        pygame.draw.rect(window, color, self.loc+self.size)
        pygame.draw.rect(window, WHITE, self.loc+self.size, 2)
        window.blit(self.text, self.text_loc)

    def hovered(self):
        loc = self.loc
        size = self.size
        mouse_pos = pygame.mouse.get_pos()
        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered():
                return True
        return False


class Slider:
    def __init__(self, loc, size, circle_size, font, label, default_val, val_range):
        self.loc = loc
        self.size = size
        self.circle_size = circle_size
        self.font = font
        self.label = label
        self.value = default_val
        self.range = val_range
        self.val_dist = val_range[1] - val_range[0]
        self.dragging = False

    def draw(self, window, events):
        loc = self.loc
        size = self.size

        text = self.font.render(f"{self.label}: {self.value}", 1, WHITE)
        text_loc = (loc[0] + (self.size[0]-text.get_width())//2, self.loc[1]+self.size[1]+7)
        pygame.draw.rect(window, GRAY, loc+size)
        pygame.draw.rect(window, WHITE, loc+size, 1)
        pygame.draw.circle(window, WHITE, (self.value_to_loc(), self.loc[1]+self.size[1]//2), self.circle_size)
        window.blit(text, text_loc)

        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
                    self.dragging = True

        clicked = pygame.mouse.get_pressed()[0]
        if not clicked:
            self.dragging = False
        
        if clicked and self.dragging:
            self.value = self.loc_to_value(mouse_pos[0])

    def loc_to_value(self, loc):
        fac = max(min((loc-self.loc[0]) / self.size[0], 1), 0)
        return int(fac*self.val_dist + self.range[0])

    def value_to_loc(self):
        fac = (self.value-self.range[0]) / self.val_dist
        return fac * self.size[0] + self.loc[0]


class Board:
    sq_size = 100
    loc = (50, 50)

    def __init__(self):
        self.pgn_moves = None
        self.flipped = False
        self.position = chess.Board()

    def draw(self, window, events):
        surface = pygame.Surface((800, 800))
        surface.blit(self.draw_squares(), (0, 0))
        surface.blit(self.draw_pieces(), (0, 0))
        self.update(events)

        if self.flipped:
            surface = pygame.transform.rotate(surface, 180)
        window.blit(surface, self.loc)

    def draw_squares(self):
        sq_size = self.sq_size
        surface = pygame.Surface((sq_size*8,)*2, pygame.SRCALPHA)

        for row in range(8):
            for col in range(8):
                loc = (sq_size * col, sq_size * row)
                color = BOARD_WHITE if (row+col) % 2 == 0 else BOARD_BLACK
                pygame.draw.rect(surface, color, loc+(sq_size, sq_size))

        return surface

    def draw_pieces(self):
        sq_size = self.sq_size
        surface = pygame.Surface((sq_size*8,)*2, pygame.SRCALPHA)

        for row in range(8):
            for col in range(8):
                piece = self.position.piece_at(8 * (7-row) + col)
                if piece is not None:
                    image = IMAGES[piece.symbol()]
                    if self.flipped:
                        image = pygame.transform.rotate(image, 180)
                    surface.blit(image, (sq_size * col + 5, sq_size * row + 5))

        return surface

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.flipped = not self.flipped


def main():
    pygame.display.set_caption("Chess Analysis")
    pygame.display.set_icon(IMAGES["ic"])
    window = pygame.display.set_mode(SCREEN)

    clock = pygame.time.Clock()
    board = Board()
    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        window.fill(BLACK)
        board.draw(window, events)


main()