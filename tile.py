import colors
import pygame
from params import *


class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.contains_player = False
        self.isStart = False
        self.isGoal = False
        self.isBlocked = False

        if (x + y) % 2 == 0:
            self.color = colors.evenColor
        else:
            self.color = colors.oddColor

    def block(self):
        self.isBlocked = True
        self.color = colors.blockColor

    def unblock(self):
        self.isBlocked = False
        if (self.get_coordinates()[0] + self.get_coordinates()[1]) % 2 == 0:
            self.color = colors.evenColor
        else:
            self.color = colors.oddColor

    def get_coordinates(self):
        return self.x, self.y

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_rect(self):
        return (
            self.get_coordinates()[0] * square_size, self.get_coordinates()[1] * square_size, square_size, square_size)

    def make_start(self):
        self.isStart = True
        self.color = colors.startColor

    def make_goal(self):
        self.isGoal = True
        self.color = colors.endColor

    def contains_player(self):
        return self.contains_player

    def set_player_here(self):
        self.contains_player = True
        self.color = colors.playerColor

    def is_inside_me(self, mousePos):
        rectangle = pygame.Rect(self.get_rect())
        return True if rectangle.collidepoint(mousePos[0], mousePos[1]) else False

    def is_blocked(self):
        return self.isBlocked
