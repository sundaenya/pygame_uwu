# spatial_grid.py

import pygame
from collections import defaultdict

class SpatialGrid:
    def __init__(self, cell_size, world_width, world_height):
        """
        Initializes the spatial grid.

        :param cell_size: Size of each grid cell (updated to handle larger entities)
        :param world_width: Width of the game world
        :param world_height: Height of the game world
        """
        self.cell_size = cell_size
        self.cells = defaultdict(list)
        self.world_width = world_width
        self.world_height = world_height

    def _get_cell_coords(self, rect):
        """
        Determines the grid cell coordinates covered by a given rectangle.

        :param rect: The rectangle to calculate grid cells for
        :return: Coordinates of the grid cells
        """
        x_start = rect.left // self.cell_size
        y_start = rect.top // self.cell_size
        x_end = rect.right // self.cell_size
        y_end = rect.bottom // self.cell_size
        return x_start, y_start, x_end, y_end

    def add(self, enemy):
        """
        Adds an enemy to the spatial grid.

        :param enemy: The enemy object with a rect attribute
        """
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                self.cells[(x, y)].append(enemy)

    def remove(self, enemy):
        """
        Removes an enemy from the spatial grid.

        :param enemy: The enemy object to remove
        """
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                if enemy in self.cells[(x, y)]:
                    self.cells[(x, y)].remove(enemy)

    def update(self, enemy):
        """
        Updates the position of an enemy in the grid.

        :param enemy: The enemy object to update
        """
        self.remove(enemy)
        self.add(enemy)

    def get_nearby(self, enemy):
        """
        Gets all nearby objects in the grid for a given enemy.

        :param enemy: The enemy object to find nearby objects for
        :return: A set of nearby objects
        """
        x_start, y_start, x_end, y_end = self._get_cell_coords(enemy.rect)
        nearby = set()
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                nearby.update(self.cells.get((x, y), []))
        return nearby

    def clear(self):
        self.cells.clear()


# Usage Example
if __name__ == "__main__":
    # Set larger cell size for the grid
    cell_size = 128  # Adjusted to accommodate larger enemies
    world_width = 4096
    world_height = 4096

    spatial_grid = SpatialGrid(cell_size, world_width, world_height)
    print(f"Spatial grid initialized with cell size: {cell_size}")



