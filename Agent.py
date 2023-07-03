import colors
import params
import time
import pygame
class Agent:
    def __init__(self, board):
        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()

    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position['x'], position['y']
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def percept(self, board): # didn't need this function
        self.current_state = board.get_current_state()
        pass

    def move(self, direction, board):
        current_pos = self.get_position()
        x, y = current_pos[0], current_pos[1]
        board.colorize(x, y, colors.green)
        self.set_position(direction, board=board)

        pass

    @staticmethod
    def get_actions(boardArray, start):
        actions = []
        x, y = start[0], start[1]
        if(x - 1 >= 0 and not boardArray[x - 1][y].isBlocked):
            actions.append({'x': -1, 'y': 0})
        if(x + 1 < params.rows and not boardArray[x + 1][y].isBlocked):
            actions.append({'x': 1, 'y': 0})
        if(y - 1 >= 0 and not boardArray[x][y - 1].isBlocked):
            actions.append({'x': 0, 'y': -1})
        if(y + 1 < params.cols and not boardArray[x][y + 1].isBlocked):
            actions.append({'x': 0, 'y': 1})
        return actions

    def bfs(self, environment):
        visited, path = self.bfs_find()
        for node in visited:
            environment.colorize(node[0], node[1], colors.red)
            time.sleep(0.05)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        for node in path:
            self.move({'x': node[0], 'y': node[1]}, environment)
            time.sleep(0.08)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        return path
    
    def bfs_find(self):
        generalVisited = []
        start_point = self.get_position()
        x, y = start_point[0], start_point[1]
        open_list = []
        open_list.append([start_point])
        while not self.current_state[x][y].isGoal:
            if start_point not in generalVisited:
                generalVisited.append(start_point)
            new_path = open_list.pop(0)
            start_point = new_path[len(new_path) - 1]
            x, y = start_point[0], start_point[1]
            actions = Agent.get_actions(self.current_state, start_point)
            new_start = x - 1, y
            if {'x':-1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x + 1, y
            if {'x':1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x, y - 1
            if {'x':0, 'y': -1} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x, y + 1
            if {'x':0, 'y': 1} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
        return generalVisited, new_path

    def dfs(self, environment):
        visited, path = self.dfs_find()
        for node in visited:
            environment.colorize(node[0], node[1], colors.red)
            time.sleep(0.1)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        for node in path:
            self.move({'x': node[0], 'y': node[1]}, environment)
            time.sleep(0.08)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        return path

    def dfs_find(self):
        generalVisited = []
        start_point = self.get_position()
        x, y = start_point[0], start_point[1]
        open_list = []
        open_list.append([start_point])
        while not self.current_state[x][y].isGoal:
            if start_point not in generalVisited:
                generalVisited.append(start_point)
            new_path = open_list.pop(len(open_list) - 1)
            start_point = new_path[len(new_path) - 1]
            x, y = start_point[0], start_point[1]
            actions = Agent.get_actions(self.current_state, start_point)
            new_start = x, y + 1
            if {'x':0, 'y': 1} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x, y - 1
            if {'x':0, 'y': -1} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x + 1, y
            if {'x':1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
            new_start = x - 1, y
            if {'x':-1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append(new_path + [new_start])
        return generalVisited, new_path

    def h_calculator(self, start_point, end_point):
        start_x, start_y = start_point
        end_x, end_y = end_point
        y = end_y - start_y
        if y < 0:
            y = y * -1
        x = end_x - start_x
        if x < 0:
            x = x * -1
        return x + y

    def a_star(self, environment, end):
        visited, path = self.star_find(end)
        for node in visited:
            environment.colorize(node[0], node[1], colors.red)
            time.sleep(0.05)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        for node in path:
            self.move({'x': node[0], 'y': node[1]}, environment)
            time.sleep(0.08)
            WIN = pygame.display.set_mode((params.width, params.height))
            environment.draw_world(WIN)
        return path

    def star_find(self, end):
        end_point = end['x'], end['y']
        generalVisited = []
        start_point = self.get_position()
        x, y = start_point[0], start_point[1]
        open_list = []
        open_list.append([start_point] + [self.h_calculator(start_point, end_point)] + [0])
        while not self.current_state[x][y].isGoal:
            if start_point not in generalVisited:
                generalVisited.append(start_point)
            least = 1000
            leastIndex = 0
            for i in range(len(open_list)):
                if open_list[i][len(open_list[i]) - 2] < least:
                    leastIndex = i
                    least = open_list[i][len(open_list[i]) - 2]
            new_path = open_list.pop(leastIndex)
            numVisited = new_path.pop(len(new_path) - 1) + 1
            new_path.pop(len(new_path) - 1)
            start_point = new_path[len(new_path) - 1]
            x, y = start_point[0], start_point[1]
            actions = Agent.get_actions(self.current_state, start_point)
            new_start = x - 1, y
            if {'x':-1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append((new_path + [new_start]) + [self.h_calculator(start_point, end_point) + numVisited] + [numVisited])
            new_start = x, y - 1
            if {'x':0, 'y': -1} in actions and not new_start in  new_path:
                open_list.append((new_path + [new_start]) + [self.h_calculator(start_point, end_point) + numVisited] + [numVisited])
            new_start = x, y + 1
            if {'x':0, 'y': 1} in actions and not new_start in  new_path:
                open_list.append((new_path + [new_start]) + [self.h_calculator(start_point, end_point) + numVisited] + [numVisited])
            new_start = x + 1, y
            if {'x':1, 'y': 0} in actions and not new_start in  new_path:
                open_list.append((new_path + [new_start]) + [self.h_calculator(start_point, end_point) + numVisited] + [numVisited])
        return generalVisited, new_path