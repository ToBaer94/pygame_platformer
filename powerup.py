import pygame
import constants
import random
from spritesheet_functions import SpriteSheet


from os import path
img_dir = path.join(path.dirname(__file__), "power_ups")


class Mushroom(pygame.sprite.Sprite):
    """ Class for the mushroom pickup item, moves like an enemy with slightly less gravity """
    def __init__(self):
        super(Mushroom, self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "mushroomRed.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))

        self.rect = self.image.get_rect()
        self.direction = "Right" if random.randrange(2) == 0 else "Left"

        self.change_x = 1 if self.direction == "Right" else -1
        self.change_y = 0

        self.player = None

        self.level_platform_list = None

    def collide(self):
        """ Called when the player collides with the mushroom """
        self.player.powerup()

    def spawn(self, x, y):
        """ Called when the player jumps against the bottom of an item block """
        self.rect.x = x
        self.rect.y = y - self.rect.height -1

    def update(self):
        self.calc_grav()

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_x *= -1

            elif self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1

        if self.rect.y > 600:
            self.kill()

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.25


class Fireball(pygame.sprite.Sprite):
    """ Class used for the behavior of the fireball by the player. Moves in a jumping motion"""
    def __init__(self):
        super(Fireball, self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "fireball2.png")).convert_alpha()

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.player = None
        self.direction = None
        self.level = None
        self.level_platform_list = None

        self.last_update = pygame.time.get_ticks()

    def spawn(self, level):
        """
        Called when the player presses the space bar, sets the spawn position and direction accordingly
        """
        self.level = level
        self.level_platform_list = self.level.platform_list
        if self.direction == "Right":
            self.rect.x = self.player.rect.x + self.player.rect.width
            self.rect.y = self.player.rect.y
            self.change_x = 2
        else:
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y
            self.change_x = -2

    def update(self):
        """
        Same as other objects, but jumps when colliding with a platform on the y-axis.
        On enemy collision, removes both. Disappears after being on screen for 4000 frames.
        """

        self.calc_grav()

        if self.change_y < 0:
            self.direction_horizontal = "Up"
        else:
            self.direction_horizontal = "Down"

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.direction_horizontal == "Down":
                self.rect.bottom = block.rect.top
                self.rect.y -= 5
                self.change_y = -4
            else:
                self.rect.top = block.rect.bottom
                self.rect.y += 5
                self.change_y = 4

        if self.rect.y > 600:
            self.kill()

        self.rect.x += self.change_x

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        if enemy_hit_list:
            self.kill()

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.x += 3
                self.change_x *= -1

            elif self.change_x > 0:
                self.rect.x -= 3
                self.change_x *= -1

        now = pygame.time.get_ticks()
        if now - self.last_update > 4000:
            self.kill()

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.35


















