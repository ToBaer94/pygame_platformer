import pygame
import constants
import random
from spritesheet_functions import SpriteSheet


from os import path
img_dir = path.join(path.dirname(__file__), "assets", "sprites", "power_ups")
sound_dir = path.join(path.dirname(__file__), "assets", "sound")

class Mushroom(pygame.sprite.Sprite):
    """ Class for the mushroom pickup item, moves like an enemy with slightly less gravity """
    def __init__(self, x, y):
        super(Mushroom, self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "mushroomRed.png")).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height - 2
        self.x_pos = x
        self.y_pos = self.rect.y

        self.direction = "Right" if random.randrange(2) == 0 else "Left"

        self.change_x = 1 if self.direction == "Right" else -1
        self.change_y = 0

        self.player = None

        self.level = None

    def collide(self):
        """ Called when the player collides with the mushroom """
        self.player.powerup()

    def update(self, dt):
        self.calc_grav(dt)

        self.y_pos += self.change_y * dt
        self.rect.y = self.y_pos

        self.world_y_collision()

        self.x_pos += self.change_x * dt
        self.rect.x = self.x_pos

        self.world_x_collision()

        if self.y_pos > 600:
            self.kill()

    def calc_grav(self, dt):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.25 * dt

    def world_x_collision(self):
        for block in self.level.platform_list:
            if self.rect.colliderect(block):
                if self.change_x < 0:
                    self.rect.left = block.rect.right
                    self.x_pos = self.rect.x
                    self.change_x *= -1

                elif self.change_x > 0:
                    self.rect.right = block.rect.left
                    self.x_pos = self.rect.x
                    self.change_x *= -1

        for block in self.level.blockers:
            if self.rect.colliderect(block):
                if self.change_x < 0:
                    self.rect.left = block.right
                    self.x_pos = self.rect.x
                    self.change_x *= -1

                elif self.change_x > 0:
                    self.rect.right = block.left
                    self.x_pos = self.rect.x
                    self.change_x *= -1

    def world_y_collision(self):
        for block in self.level.platform_list:
            if self.rect.colliderect(block):
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.y_pos = self.rect.y
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    self.y_pos = self.rect.y
                self.change_y = 0

        for block in self.level.blockers:
            if self.rect.colliderect(block):
                if self.change_y > 0:
                    self.rect.bottom = block.top
                    self.y_pos = self.rect.y
                elif self.change_y < 0:
                    self.rect.top = block.bottom
                    self.y_pos = self.rect.y
                self.change_y = 0

class Fireball(pygame.sprite.Sprite):
    """ Class used for the behavior of the fireball by the player. Moves in a jumping motion"""
    def __init__(self, player, level, direction):
        super(Fireball, self).__init__()
        self.orig_image = pygame.image.load(path.join(img_dir, "fireball2.png")).convert_alpha()
        self.image = self.orig_image

        self.rect = self.image.get_rect()

        self.player = player
        self.direction = direction

        self.level = level

        self.change_x = 0
        self.change_y = 0

        self.hit_sound = pygame.mixer.Sound(path.join(sound_dir, "hit.wav"))

        if self.direction == "Right":
            self.rect.x = self.player.rect.x + self.player.rect.width
            self.rect.y = self.player.rect.y
            self.x_pos = self.rect.x
            self.y_pos = self.rect.y
            self.change_x = 3
            self.rot_speed = -20
        else:
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y
            self.x_pos = self.rect.x
            self.y_pos = self.rect.y
            self.change_x = -3
            self.rot_speed = 20

        self.rot = 0

        self.last_update = pygame.time.get_ticks()
        self.last_fire_update = pygame.time.get_ticks()

    def update(self, dt):
        """
        Same as other objects, but jumps when colliding with a platform on the y-axis.
        On enemy collision, removes both. Disappears after being on screen for 4000 frames.

        Currently the movement speed isnt adjusted for the time delta because of rounding issues with
        my rotation
        """

        self.rotate(dt)
        self.calc_grav(dt)

        if self.change_y < 0:
            self.direction_horizontal = "Up"
        else:
            self.direction_horizontal = "Down"

        self.y_pos += self.change_y # * dt
        self.rect.y = self.y_pos

        self.world_y_collide()

        if self.rect.y > 600:
            self.kill()

        self.x_pos += self.change_x # * dt
        self.rect.x = self.x_pos

        self.world_x_collide()

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if enemy_hit_list:
            self.kill()
            for enemy in enemy_hit_list:
                self.hit_sound.play()
                enemy.kill_init()

        now = pygame.time.get_ticks()
        if now - self.last_fire_update > 2500:
            self.last_fire_update = now
            self.kill()

    def world_x_collide(self):
        """ Check for collisions on the x-axis """
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x < 0:
                self.rect.x += 3
                self.x_pos = self.rect.x
                self.change_x *= -1
                self.rot_speed *= -1

            elif self.change_x > 0:
                self.rect.x -= 3
                self.x_pos = self.rect.x
                self.change_x *= -1
                self.rot_speed *= -1

        for block in self.level.blockers:
            if self.rect.colliderect(block):
                if self.change_x < 0:
                    self.rect.x += 3
                    self.x_pos = self.rect.x
                    self.change_x *= -1
                    self.rot_speed *= -1

                elif self.change_x > 0:
                    self.rect.x -= 3
                    self.x_pos = self.rect.x
                    self.change_x *= -1
                    self.rot_speed *= -1

    def world_y_collide(self):
        """ Check for collisions on the y-axis """
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.direction_horizontal == "Down":
                self.rect.bottom = block.rect.top
                self.rect.y -= 5
                self.y_pos = self.rect.y
                self.change_y = -4
            else:
                self.rect.top = block.rect.bottom
                self.rect.y += 5
                self.y_pos = self.rect.y
                self.change_y = 4

        for block in self.level.blockers:
            if self.rect.colliderect(block):
                if self.direction_horizontal == "Down":
                    self.rect.bottom = block.top
                    self.rect.y -= 5
                    self.y_pos = self.rect.y
                    self.change_y = -4
                else:
                    self.rect.top = block.bottom
                    self.rect.y += 5
                    self.y_pos = self.rect.y
                    self.change_y = 4

    def rotate(self, dt):
        """
        Rotate the picture every X ticks, set the new picture and the new rect. Position new rect
        at the same position as old rect. Set the proxy coordinates used for float position

        Bug with rotation causes the movement speed to break when using floats (delta time). Dont know a fix
        yet
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed * dt) % 360
            new_image = pygame.transform.rotate(self.orig_image, self.rot)

            self.image = new_image
            self.rect = self.image.get_rect(center = self.rect.center)

            self.x_pos = self.rect.x
            self.y_pos = self.rect.y

    def calc_grav(self, dt):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.25


















