import pygame
from pygame.locals import *
import random
import copy


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        self.clist = self.cell_list()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> list:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        self.clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for st in range(self.cell_height):
                for element in range(self.cell_width):
                    self.clist[st][element] = random.randint(0, 1)
        return self.clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if clist[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        x, y = cell
        n = self.cell_height - 1
        m = self.cell_width - 1
        neighbours = [self.clist[i][j] for i in range(x - 1, x + 2) for j in range(y - 1, y + 2) if
                      (0 <= i <= n) and (0 <= j <= m) and (i != x or j != y)]
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        deepcopy = copy.deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if not 1 < neighbours < 4:
                        deepcopy[i][j] = 0
                else:
                    if neighbours == 3:
                        deepcopy[i][j] = 1
        self.clist = deepcopy
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(1000, 1000, 20)
    game.run()
