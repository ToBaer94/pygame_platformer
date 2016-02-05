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
    def __init__(self, sprite_sheet_data, x, y):
        super(Platform, self).__init__()

        self.sprite_sheet = SpriteSheet(path.join(img_dir, "tiles_spritesheet.png"))
        self.image = self.sprite_sheet.get_image(sprite_sheet_data[0],
                                                 sprite_sheet_data[1],
                                                 sprite_sheet_data[2],
                                                 sprite_sheet_data[3])

        self.sprite_sheet_data = sprite_sheet_data

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_pos = x
        self.y_pos = y

    def collide(self, dt):
        pass

    def update(self, dt):
        pass

    def set_image(self, block):
        self.image = self.sprite_sheet.get_image(block[0],
                                                 block[1],
                                                 block[2],
                                                 block[3])


class MovingPlatform(Platform):
    """
    Platform that moves on the x or y axis
    """
    def __init__(self, sprite_sheet_data, x, y):
        super(MovingPlatform, self).__init__(sprite_sheet_data, x, y)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_pos = x
        self.y_pos = y

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.player = None
        self.level = None

    def update(self, dt):
        """
        Moves within set boundaries, moves the player on collision.
        """

        self.x_pos += self.change_x * dt
        self.rect.x = self.x_pos

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
                self.player.x_pos = self.player.rect.x
            else:
                self.player.rect.left = self.rect.right
                self.player.x_pos = self.player.rect.x

        self.player_collide(dt)

        self.y_pos += self.change_y * dt
        self.rect.y = self.y_pos

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
                self.player.y_pos = self.player.rect.y
            else:
                self.player.rect.top = self.rect.bottom
                self.player.y_pos = self.player.rect.y
        if self.change_y != 0:
            cur_y_pos = round(self.y_pos)
            if cur_y_pos > self.boundary_bottom or cur_y_pos < self.boundary_top:
                self.change_y *= -1

        if self.change_x != 0:
            cur_x_pos = self.x_pos - self.level.world_shift
            if cur_x_pos < self.boundary_left:
                self.change_x *= -1
                self.x_pos = self.boundary_left + 1 + self.level.world_shift

            if cur_x_pos > self.boundary_right:
                self.change_x *= -1
                self.x_pos = self.boundary_right - 1 + self.level.world_shift

    def collide(self, dt):
        pass
        #self.player.x_pos += self.change_x * dt
        #self.player.rect.x = self.player.x_pos

    def player_collide(self, dt):

        if self.change_x != 0:
            self.player.y_pos += 2
            self.player.rect.y = self.player.y_pos
            hit = pygame.sprite.collide_rect(self, self.player)
            self.player.y_pos -= 2
            self.player.rect.y = self.player.y_pos
            if hit:
                print "yey"
                self.player.x_pos += self.change_x * dt
                self.player.rect.x = self.player.x_pos


class SpecialBlock(Platform):
    """ Item block class """
    def __init__(self, sprite_sheet_data, x, y):
        super(SpecialBlock, self).__init__(sprite_sheet_data, x, y)
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_pos = x
        self.y_pos = y


        self.opened = False

        self.player = None
        self.level = None

    def collide(self, dt):
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
        item = powerup.Mushroom(x, y)
        item.level_platform_list = self.level.platform_list
        item.player = self.player
        self.level.item_list.add(item)