import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        # self.image = spritesheet.parse_sprite(image)
        # Manual load in: self.image = pygame.image.load(image)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                """if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('grass.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                    # Move to next tile in current row
                    """
                tiles.append(Tile(f'data\grass{int(tile) + 1}.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                # match tile:
                    
                #     case '0' :
                #         self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                #     case '1' :
                #         tiles.append(Tile('data\grass1.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '2' :
                #         tiles.append(Tile('data\grass2.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '3' :
                #         tiles.append(Tile('data\grass3.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '4' :
                #         tiles.append(Tile('data\grass4.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '5' :
                #         tiles.append(Tile('data\grass5.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '6' :
                #         tiles.append(Tile('data\grass6.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '7' :
                #         tiles.append(Tile('data\grass7.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '8' :
                #         tiles.append(Tile('data\grass8.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '9' :
                #         tiles.append(Tile('data\grass9.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '10' :
                #         tiles.append(Tile('data\grass10.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '11' :
                #         tiles.append(Tile('data\grass11.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case '12' :
                #         tiles.append(Tile('data\grass12.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     # case '13' :
                #     #     tiles.append(Tile('data\grass13.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     # case '14' :
                #     #     tiles.append(Tile('data\grass14.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                #     case _:
                #         pass
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles









