import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Crate.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size) / 2
        center_y = y + int(size) / 2
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value

class Tree2(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Tree_2.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Tree3(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Tree_3.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Sign(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Sign_2.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Stomp(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Tree_1.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Rock(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Stone.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Mushroom(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Mushroom_1.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Mushroom2(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Mushroom_2.png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class Small_bush(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("./graphics/Object/Bush (4).png").convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


