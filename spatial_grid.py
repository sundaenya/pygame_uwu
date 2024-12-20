# spatial_grid.py

import pygame
from collections import defaultdict

class SpatialGrid:
    def __init__(self, cell_size, world_width, world_height):
        self.cell_size = cell_size
        self.cells = defaultdict(list)
        self.world_width = world_width
        self.world_height = world_height

    def _get_cell_coords(self, rect):
        x_start = rect.left // self.cell_size
        y_start = rect.top // self.cell_size
        x_end = rect.right // self.cell_size
        y_end = rect.bottom // self.cell_size
        return x_start, y_start, x_end, y_end

    def add(self, enemy):
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.cells[(x, y)].append(enemy)

    def remove(self, enemy):
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                if enemy in self.cells[(x, y)]:
                    self.cells[(x, y)].remove(enemy)

    def update(self, enemy):
        self.remove(enemy)
        self.add(enemy)

    def get_nearby(self, enemy):
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        nearby = set()
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                nearby.update(self.cells.get((x, y), []))
        return nearby
    
    def clear(self):
        self.cells.clear()

