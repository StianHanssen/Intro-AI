import os
from math import floor, ceil
from cell import Cell
import emoji as em


class Board():
    def __init__(self, file_name, default_g=None, default_h=None, mac=False, emoji=False):
        self.__INPUT = (file_name, default_g, default_h, mac, emoji)
        self.__EMOJI = emoji
        self.__cells = []
        self.START = None
        self.END = None
        self.BOARD_STR = Board.__read_file(Board.__get_board_path(file_name, mac))
        self.WIDTH = self.__find_width()
        self.__gen_cells(self.BOARD_STR)
        self.__set_default_g(default_g)
        self.__set_default_h(default_h)
        self.HEIGHT = ceil(len(self.__cells) / self.WIDTH)

    def __str__(self):
        return self.BOARD_STR

    @staticmethod
    def __get_board_path(file_name, mac=False):
        folder = "/boards/" if mac else "\\boards\\"
        path = os.path.dirname(os.path.abspath(__file__))
        path += folder + file_name
        return path

    @staticmethod
    def __read_file(file_path):
        with open(file_path) as f:
            read_data = f.read()
        return read_data

    @staticmethod
    def __clean_up(text):
        clean_text = ""
        for c in text:
            if c in Cell.WEIGHTS:
                clean_text += c
        return clean_text

    def __get_heuristic(self, cell):
        diff_x = abs(cell.X - self.END.X)
        diff_y = abs(cell.Y - self.END.Y)
        v = 0
        if diff_x > 0 and diff_y > 0:
            v = 1
        return (abs(cell.X - self.END.X) + abs(cell.Y - self.END.Y)) - v

    def __find_width(self):
        return len(self.BOARD_STR.split("\n")[0])

    def __gen_cells(self, board_string):
        board_string = Board.__clean_up(board_string)
        for i in range(len(board_string)):
            x = i % self.WIDTH
            y = floor(i / self.WIDTH)
            cell = Cell(x, y, board_string[i])
            self.__cells.append(cell)
            if cell.SYMBOL == 'A':
                self.START = cell
            elif cell.SYMBOL == 'B':
                self.END = cell

    def __set_default_h(self, h):
        for cell in self.__cells:
            if h is None:
                cell.set_h(self.__get_heuristic(cell))
            else:
                cell.set_h(h)

    def __set_default_g(self, g):
        if g is not None:
            for cell in self.__cells:
                cell.set_g(g)

    def __is_cell(self, x, y):
        return (x >= 0 and x < self.WIDTH) and (y >= 0 and y < self.HEIGHT)

    def get_cell(self, x, y):
        return self.__cells[x + y * self.WIDTH]

    def get_cells(self):
        return self.__cells

    def clone(self):
        file_name, default_g, default_h, mac, emoji = self.__INPUT
        return Board(file_name, default_g, default_h, mac, emoji)

    def get_neighbours(self, cell):
        neighbours = []
        for offset in (1, 0), (-1, 0), (0, 1), (0, -1):
            x, y = cell.X + offset[0], cell.Y + offset[1]
            if self.__is_cell(x, y):
                neighbour = self.get_cell(x, y)
                if neighbour.WEIGHT is not None:  # None meaning a wall
                    neighbours.append(neighbour)
        return neighbours

    def update_neighbour(self, neighbour, cell):
        neighbour.set_g(cell.get_g() + neighbour.WEIGHT)
        neighbour.set_parent(cell)

    def get_path(self):
        cell = self.END
        path = [(cell.X, cell.Y)]
        while cell.get_parent() is not self.START:
            cell = cell.get_parent()
            path.append((cell.X, cell.Y))
        path.append((self.START.X, self.START.Y))
        path.reverse()
        return path

    def get_path_str(self, opened=None, closed=None):
        path = self.get_path()
        text = list(Board.__clean_up(self.BOARD_STR))
        if closed is not None:
            closed -= {self.START, self.END}
            for c in closed:
                text[c.X + c.Y * self.WIDTH] = 'x'
        if opened is not None:
            opened = set(opened)
            opened -= {self.START, self.END}
            for c in opened:
                text[c.X + c.Y * self.WIDTH] = '*'
        for x, y in path[1:-1]:
            text[x + y * self.WIDTH] = em.emojize(':runner:', use_aliases=True) if self.__EMOJI else "o"
        board = "".join(text)
        path_str = ""
        for i in range(self.HEIGHT):
            path_str += board[i * self.WIDTH: i * self.WIDTH + self.WIDTH] + '\n'
        return path_str[:-2]
