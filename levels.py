import pygame
import constants
import platforms
import enemies
import tilerenderer
from player_level import Player
from os import path
import math

img_dir = path.join(path.dirname(__file__), "world")
level_dir = path.join(path.dirname(__file__), "assets", "levels")
music_dir = path.join(path.dirname(__file__), "assets", "music")


class Level(object):
    """
    Level class. Handles updating and drawing of the objects in the current level as well as moving the viewport.
    Holds methods for spawning enemies, platforms and item blocks.
    """
    def __init__(self, player, level):
        super(Level, self).__init__()

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.effect_list = pygame.sprite.Group()
        self.kill_animation_list = pygame.sprite.Group()

        self.tmx_file = path.join(level_dir, level + ".tmx")
        self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
        self.map_surface = self.tile_renderer.make_map()
        self.map_rect = self.map_surface.get_rect()
        try:
            pygame.mixer.music.load(path.join(music_dir, level + ".mp3"))
        except:
            pass

        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.player = player
        self.blockers = []
        self.end_point = []
        self.ladders = []
        self.ropes = []

        self.world_shift_x = 0
        self.world_shift_y = 0

        self.background = None

        self.map_x = 0
        self.map_y = 0
        self.end_point = None

        self.left_boundary = None
        self.right_boundary = None
        self.bottom_boundary = None
        self.top_boundary = None

        self.setup_level()

    def update(self, dt):
        self.platform_list.update(dt)
        self.enemy_list.update(dt)
        self.item_list.update(dt)
        self.effect_list.update(dt)
        self.kill_animation_list.update(dt)

    def draw(self, screen):
        screen.blit(self.map_surface, (self.map_x, self.map_y))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)
        self.effect_list.draw(screen)
        self.kill_animation_list.draw(screen)

        # Draw rects to debug rectangles
        """
        for enemy in self.enemy_list:
            pygame.draw.rect(screen, constants.BLACK, [enemy.x_pos, enemy.y_pos, enemy.rect.width, enemy.rect.height], 1)


        for ladder in self.ladders:
            pygame.draw.rect(screen, constants.BLACK, [ladder.x, ladder.y, ladder.width, ladder.height], 1)
        pygame.draw.rect(screen, constants.BLACK, [self.player.rect.x, self.player.rect.y, self.player.rect.width, self.player.rect.height], 1)
        """
    def shift_world_x(self, shift_x):
        """
        Offset all objects handled by the level class according to the viewport
        """

        if shift_x > 0:
            shift_x = math.ceil(shift_x)
        elif shift_x < 0:
            shift_x = math.floor(shift_x)
        self.world_shift_x += shift_x

        self.map_x += shift_x
        self.end_point.x += shift_x

        for blocker in self.blockers:
            blocker.x += shift_x

        for ladder in self.ladders:
            ladder.x += shift_x

        for rope in self.ropes:
            rope.x += shift_x

        for movingplatform in self.platform_list:
            movingplatform.x_pos += shift_x
            movingplatform.rect.x = movingplatform.x_pos

        for enemy in self.enemy_list:
            enemy.x_pos += shift_x
            enemy.rect.x = enemy.x_pos

        for item in self.item_list:
            item.x_pos += shift_x
            item.rect.x = item.x_pos

        for effect in self.effect_list:
            effect.x_pos += shift_x
            effect.rect.x = effect.x_pos

        for dead_enemy in self.kill_animation_list:
            dead_enemy.x_pos += shift_x
            dead_enemy.rect.x = dead_enemy.x_pos

        self.left_boundary.x += shift_x
        self.right_boundary.x += shift_x
        self.bottom_boundary.x += shift_x
        self.top_boundary.x += shift_x

    def shift_world_y(self, shift_y):
        """
        Offset all objects handled by the level class according to the viewport
        """

        #if self.world_shift_y + shift_y > 0:
        #    pass

        shift_y = round(shift_y)
        self.world_shift_y += shift_y

        self.map_y += shift_y
        self.end_point.y += shift_y

        for blocker in self.blockers:
            blocker.y += shift_y

        for ladder in self.ladders:
            ladder.y += shift_y

        for rope in self.ropes:
            rope.y += shift_y


        for movingplatform in self.platform_list:
            movingplatform.boundary_bottom += shift_y
            movingplatform.boundary_top += shift_y
            movingplatform.y_pos += shift_y
            movingplatform.rect.y = movingplatform.y_pos


        for enemy in self.enemy_list:
            enemy.y_pos += shift_y
            enemy.rect.y = enemy.y_pos

        for item in self.item_list:
            item.y_pos += shift_y
            item.rect.y = item.y_pos

        for effect in self.effect_list:
            effect.y_pos += shift_y
            effect.rect.y = effect.y_pos

        for dead_enemy in self.kill_animation_list:
            dead_enemy.y_pos += shift_y
            dead_enemy.rect.y = dead_enemy.y_pos

        self.left_boundary.y += shift_y
        self.right_boundary.y += shift_y
        self.bottom_boundary.y += shift_y
        self.top_boundary.y += shift_y

    def create_enemy(self, x, y):
        """
        Creates an enemy instance at the parameter pixel location, gives the enemy instance a reference to
        all platforms. Adds the enemy to the Sprite list used for updating and drawing
        """
        enemy = enemies.Enemy(x, y, self)
        self.enemy_list.add(enemy)

    def create_edgewalker(self, x, y):
        """
        Creates an Edgewalker enemy instance at the parameter pixel location, gives the enemy instance a reference to
        all platforms. Adds the enemy to the Sprite list used for updating and drawing
        """
        enemy = enemies.EdgeWalker(x, y, self)
        self.enemy_list.add(enemy)

    def create_moving_platform(self, platform, player):  ##create_moving_platform([0, 0, 100, 25], player)
        """
        Takes a list as parameter. Creates a moving platform for every item in the list. Adds a player and
        level reference to the platform
        """

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

    def create_special_block(self, pos, player):
        """
        Takes a list as parameter. Creates an item block.
        """

        block = platforms.SpecialBlock(platforms.POWER_UP, pos[0], pos[1])
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

    def setup_level(self):
        for tile_object in self.tile_renderer.tmx_data.objects:
            properties = tile_object.__dict__
            if properties["name"] == "blocker":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.blockers.append(new_rect)
            if properties["name"] == "enemy":
                x = properties['x']
                y = properties['y']
                self.create_enemy(x, y)
            if properties["name"] == "enemy2":
                x = properties['x']
                y = properties['y']
                self.create_edgewalker(x, y)
            if properties["name"] == "movingplatlr":
                x = properties['x']
                y = properties['y']
                self.create_moving_platform([x, y, x-50, x+50, 0, 0, 1, 0], self.player)
            if properties["name"] == "movingplatud":
                x = properties['x']
                y = properties['y']
                self.create_moving_platform([x, y, 0, 0, y-300, y+300, 0, 1], self.player)
            if properties["name"] == "itemblock":
                x = properties['x']
                y = properties['y']
                self.create_special_block((x, y), self.player)
            if properties["name"] == "end":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.end_point = new_rect
            if properties["name"] == "lowb":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.bottom_boundary = new_rect
            if properties["name"] == "leftb":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.left_boundary = new_rect
            if properties["name"] == "rightb":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.right_boundary = new_rect
            if properties["name"] == "upb":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.top_boundary = new_rect
            if properties["name"] == "ladder":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.ladders.append(new_rect)
            if properties["name"] == "rope":
                x = properties['x']
                y = properties['y']
                width = properties['width']
                height = properties['height']
                new_rect = pygame.Rect(x, y, width, height)
                self.ropes.append(new_rect)


# class Level_01(Level):
#     """
#     Class creating the first level
#     """
#     def __init__(self, player):
#
#         Level.__init__(self, player)
#
#         self.tmx_file = path.join(level_dir, "map.tmx")
#         self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
#         self.map_surface = self.tile_renderer.make_map()
#         self.map_rect = self.map_surface.get_rect()
#
#         self.player = player
#
#         self.blockers = []
#         self.end_point = []
#         self.left_boundary = None
#         self.right_boundary = None
#         self.bottom_boundary = None
#         self.top_boundary = None
#
#         self.setup_level()
#
# class Level_02(Level):
#     """
#     Class creating the first level
#     """
#     def __init__(self, player):
#
#         Level.__init__(self, player)
#
#
#
#         self.tmx_file = path.join(level_dir, "map2.tmx")
#         self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
#         self.map_surface = self.tile_renderer.make_map()
#         self.map_rect = self.map_surface.get_rect()
#
#         self.player = player
#
#         self.blockers = []
#         self.end_point = []
#
#         self.setup_level()
#
# class Level_03(Level):
#     """
#     Class creating the first level
#     """
#     def __init__(self, player):
#
#         Level.__init__(self, player)
#
#         self.tmx_file = path.join(level_dir, "map3.tmx")
#         self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
#         self.map_surface = self.tile_renderer.make_map()
#         self.map_rect = self.map_surface.get_rect()
#
#         self.player = player
#
#         self.blockers = []
#         self.end_point = []
#
#         self.setup_level()
