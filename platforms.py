import pygame
import powerup
from os import path

from spritesheet_functions import SpriteSheet

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
POWER_UP              = (0  , 0  , 70, 70)
POWER_DOWN            = (0  , 71 , 70, 70)

img_dir = path.join(path.dirname(__file__), "world")



class Platform(pygame.sprite.Sprite):
    """
    Class for basic platforms. Uses sprite_sheet.get
    to get the appropriate sprite according to defined values above
    """

    def __init__(self, sprite_sheet_data):
        super(Platform, self).__init__()

        self.sprite_sheet = SpriteSheet(path.join(img_dir, "tiles_spritesheet.png"))
        self.image = self.sprite_sheet.get_image(sprite_sheet_data[0],
                                                 sprite_sheet_data[1],
                                                 sprite_sheet_data[2],
                                                 sprite_sheet_data[3])

        self.sprite_sheet_data = sprite_sheet_data

        self.rect = self.image.get_rect()

    def collide(self):
        pass

    def set_image(self, block):
        self.image = self.sprite_sheet.get_image(block[0],
                                                 block[1],
                                                 block[2],
                                                 block[3])


class MovingPlatform(Platform):
    """
    Platform that moves on the x or why axis
    """
    def __init__(self, sprite_sheet_data):
        super(MovingPlatform, self).__init__(sprite_sheet_data)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.player = None
        self.level = None

    def update(self):
        """
        Moves within set boundaries, moves the player on collision.
        """
        self.rect.x += self.change_x

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        self.rect.y += self.change_y

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

    def collide(self):
        self.player.rect.x += self.change_x


class SpecialBlock(Platform):
    """ Item block class """
    def __init__(self, sprite_sheet_data):
        super(SpecialBlock, self).__init__(sprite_sheet_data)
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self.opened = False

        self.player = None
        self.level = None

    def collide(self):
        """
        Called when the player jumps against the block. Spawns its content when hit from below
        and changes its sprite to empty
        """
        if self.rect.bottom == self.player.rect.top and not self.opened:
            print "Works"
            self.opened = True
            self.spawn_item(self.rect.x, self.rect.y)
            self.set_image(POWER_DOWN)
            self.image = pygame.transform.scale(self.image, (35, 35))

            x = self.rect.x
            y = self.rect.y

            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def spawn_item(self, x, y):
        """Spawns the item at the x, y parameter passed in"""
        item = powerup.Mushroom()
        item.spawn(x, y)
        item.level_platform_list = self.level.platform_list
        item.player = self.player
        self.level.item_list.add(item)




