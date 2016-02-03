import pygame
import constants
import platforms

from os import path
img_dir = path.join(path.dirname(__file__), "enemy")


class Enemy(pygame.sprite.Sprite):
    """Base enemy class used for testing. Doesnt have an animation set"""
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "base_enemy", "base_enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 38))

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 400 - self.rect.height

        self.change_x = -1
        self.change_y = 0

        self.direction = "Left"

        self.level_platform_list = None

    def update(self):
        """
        Moves the enemy, handles platform collision.
        Uses flip() method to flip the sprite when hitting a wall
        on the x-axis
        """
        self.calc_grav()

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            #block.collide()
            if isinstance(block, platforms.MovingPlatform):
                self.rect.x += block.change_x

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_x *= -1
                self.flip()
            elif self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1
                self.flip()

        if self.rect.y > 600:
            self.kill()

    def flip(self):
        """
        Flips the enemy sprite if the enemy collided with a vertical wall and changed direction
        """
        x = self.rect.x
        y = self.rect.y
        if self.direction == "Left" and self.change_x > 0:
            self.direction = "Right"
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft = (x, y))

        if self.direction == "Right" and self.change_x < 0:
            self.direction = "Left"
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft=(x, y))

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.35


class Koopa(Enemy):
    """
    More advanced enemy. Turns around at ledges of platforms and uses
    sprite animation.
    """
    def __init__(self):
        super(Koopa, self).__init__()

        self.image = pygame.image.load(path.join(img_dir, "worm", "worm.png")).convert_alpha()
        self.rect = self.image.get_rect()

        self.onground = False

        self.frame = 0 # Used for animation speed
        self.anim_speed = 100 # Used for animation speed
        self.last_update = pygame.time.get_ticks() # Used for animation speed
        self.walking_r = []
        self.walking_l = []
        self.create_images()

    def create_images(self):
        """
        Creates the sprite list for horizontal movement.
        """
        for x in range(0, 8):
            image = pygame.image.load(path.join(img_dir, "worm", "frame-%s.png" % (1+x))).convert_alpha()
            image = pygame.transform.scale(image, (40, 44))
            self.walking_l.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_r.append(image)

    def animate(self):
        """ animates the enemy """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.anim_speed:
            self.last_update = now
            if self.change_x > 0:
                self.image = self.walking_r[self.frame]
                self.frame += 1
                self.frame %= 8

            else:
                self.image = self.walking_l[self.frame]
                self.frame += 1
                self.frame %= 8

    def update(self):
        """ Handles movement and platform collision """
        self.calc_grav()
        self.animate()

        right = self.change_x > 0

        # Create a point to the bottom left or bottom right of the enemy
        m = (1, 1) if right else (-1, 1)
        point = self.rect.bottomright if right else self.rect.bottomleft
        fp = map(sum, zip(m, point))

        # Check if the created point does collide with a platform
        collide = any(p for p in self.level_platform_list if p.rect.collidepoint(fp))

        # If there is no collision, turn the enemy around (if the enemy is not in the air)
        if not collide:
            if self.onground:
                self.change_x *= -1
                self.flip()

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            self.onground = True
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            if isinstance(block, platforms.MovingPlatform):
                self.rect.x += block.change_x

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level_platform_list, False)
        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_x *= -1
                self.flip()
            elif self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x *= -1
                self.flip()