import pygame
import constants
import platforms
import enemies
from os import path

img_dir = path.join(path.dirname(__file__), "world")


class Level(object):
    """
    Level class. Handles updating and drawing of the objects in the current level as well as moving the viewport.
    Only used as base class.
    Holds methods for spawning enemies, platforms and item blocks.
    """
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.effect_list = pygame.sprite.Group()
        self.player = player

        self.world_shift = 0

        self.background = None

    def update(self, dt):
        self.platform_list.update(dt)
        self.enemy_list.update(dt)
        self.item_list.update(dt)
        self.effect_list.update(dt)

    def draw(self, screen):
        screen.fill(constants.BLUE)
        screen.blit(self.background, (self.world_shift // 3,0))

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)
        self.effect_list.draw(screen)

    def shift_world(self, shift_x):
        """
        Offset all objects handled by the level class according to the viewport
        """

        shift_x = shift_x
        if self.world_shift + shift_x > 0:
            pass
        else:
            self.world_shift += shift_x
            for platform in self.platform_list:
                platform.x_pos += shift_x
                platform.rect.x = platform.x_pos

            for enemy in self.enemy_list:
                enemy.x_pos += shift_x
                enemy.rect.x = enemy.x_pos

            for item in self.item_list:
                item.x_pos += shift_x
                item.rect.x = item.x_pos

            for effect in self.effect_list:
                effect.x_pos += shift_x
                effect.rect.x = effect.x_pos

    def create_enemy(self, x, y):
        """
        Creates an enemy instance at the parameter pixel location, gives the enemy instance a reference to
        all platforms. Adds the enemy to the Sprite list used for updating and drawing
        """
        enemy = enemies.Enemy(x, y)
        enemy.level_platform_list = self.platform_list
        self.enemy_list.add(enemy)

    def create_koopa(self, x, y):
        """
        Creates a Koopa enemy instance at the parameter pixel location, gives the enemy instance a reference to
        all platforms. Adds the enemy to the Sprite list used for updating and drawing
        """
        enemy = enemies.Koopa(x, y)
        enemy.level_platform_list = self.platform_list
        self.enemy_list.add(enemy)

    def create_platform(self, level):
        """
        Takes a list as parameter. Creates a platform for every item in the list. Adds a player reference
        to the platform
        """
        for platform in level:
            block = platforms.Platform(platform[0], platform[1], platform[2])
            block.player = self.player
            self.platform_list.add(block)

    def create_moving_platform(self, level, player):  ##create_moving_platform([0, 0, 100, 25], player)
        """
        Takes a list as parameter. Creates a moving platform for every item in the list. Adds a player and
        level reference to the platform
        """
        for platform in level:
            #print platform
            block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE,
                                             platform[0], platform[1])
            block.boundary_left = platform[2]
            block.boundary_right = platform[3]
            block.boundary_top = platform[4]
            block.boundary_bottom = platform[5]
            block.change_x = platform[6]
            block.change_y = platform[7]
            block.player = self.player
            block.level = self
            self.platform_list.add(block)

    def create_special_block(self, level, player):
        """
        Takes a list as parameter. Creates an item block.
        """
        for platform in level:
            block = platforms.SpecialBlock(platforms.POWER_UP, platform[0], platform[1])
            block.player = self.player
            block.level = self
            self.platform_list.add(block)


class Level_01(Level):
    """
    Class creating the first level
    """
    def __init__(self, player):

        Level.__init__(self, player)

        self.background = pygame.image.load(path.join(img_dir, "background_01.png")).convert()
        self.background.set_colorkey(constants.WHITE)

        self.level_limit = -500 - self.player.rect.width

        # List of platforms, [platform type, x, y]
        level = [[platforms.STONE_PLATFORM_MIDDLE, 0, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 70, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 140, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 210, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 280, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 350, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 420, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 560, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 630, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 700, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 770, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 840, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 910, 560],
                 [platforms.STONE_PLATFORM_MIDDLE, 980, 560],

                 [platforms.GRASS_LEFT, 200, 430],
                 [platforms.GRASS_MIDDLE, 270, 430],
                 [platforms.GRASS_RIGHT, 340, 430],

                 [platforms.GRASS_LEFT, 440, 330],
                 [platforms.GRASS_MIDDLE, 510, 330],
                 [platforms.GRASS_RIGHT, 580, 330]
                 ]

        # List of moving platforms
        # [x, y, left_boundary, r_boundary, top_boundary, bottom_boundary, x velocity, y velocity]
        level_moving = [[670, 230, 670, 790, 0, 0, 1, 0],
                        [890, 330, 0, 0, 130, 370, 0, 1 ]
                        ]

        level_special = [[50, 400],
                         [700, 400]
                         ]

        self.create_moving_platform(level_moving, player) # Create moving platforms

        for x in range(3):
            self.create_enemy(x*100 + 400, 540) # Spawn base_enemies

        for x in range(2):
            self.create_koopa(400 + 100 * x, 100) # Spawn Koopas

        self.create_platform(level) # Create the platforms
        self.create_special_block(level_special, player) # Create item blocks


# Level 2 not updated for use
"""
class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        self.level_limit = -500 - self.player.rect.width

        level = [[0, 580, 800, 20],
                 [200, 500, 100, 20],
                 [1000, 570, 100, 20]
                ]

        self.create_platform(level)

        for x in range(2):
            self.create_enemy(500+50*x, 0)
"""
