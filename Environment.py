import pygame
import colors
import numpy as np
from tile import Tile
from params import *


class Board:
    def __init__(self, start, end):
        self.boardArray = []
        arraynump = np.load('Mazes/Maze.npy')

        # initializing 2D matrix as board:
        for row in range(rows):
            self.boardArray.append([])
            for col in range(cols):
                self.boardArray[row].append(Tile(row, col))

        # locking tiles based on maze file :
        for i in range(rows):
            for j in range(cols):
                if arraynump[j][i] == 0:
                    self.boardArray[i][j].block()

        # setting positions :
        # setting start positions :
        self.start_pos = start['x'], start['y']
        (self.boardArray[start['x']][start['y']]).make_start()

        # setting player position like start position
        self.agent_pos = start['x'], start['y']
        (self.boardArray[start['x']][start['y']]).set_player_here()

        # setting goal position :
        self.goal_pos = end['x'], end['y']
        (self.boardArray[end['x']][end['y']]).make_goal()

    # draws the matrix:
    def draw_tiles(self, win):
        for row in range(rows):
            for col in range(cols):
                tile = self.boardArray[row][col]
                pygame.draw.rect(win, tile.get_color(), tile.get_rect())

    # draws the matrix and shows on screen - use this method to display your outcomes
    def draw_world(self, win):
        self.draw_tiles(win)
        pygame.display.update()

    def get_current_state(self):
        return self.boardArray

    def get_agent_pos(self):
        return self.agent_pos

    # Updates the matrix values
    def update_board(self, new_state):
        self.boardArray = new_state

    def set_agent_pos(self, new_pos):

        self.agent_pos = new_pos['x'], new_pos['y']
        (self.boardArray[new_pos['x']][new_pos['y']]).set_player_here()

    def colorize(self, x, y, color):
        self.boardArray[x][y].set_color(color)
