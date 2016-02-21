import pygame
import constants
import platforms

from os import path
img_dir = path.join(path.dirname(__file__), "assets", "sprites", "enemy")


class Enemy(pygame.sprite.Sprite):
    """Base enemy class used for testing. Doesnt have an animation set"""
    def __init__(self, x, y, level):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "base_enemy", "base_enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 76))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_pos = x
        self.y_pos = y

        self.change_x = -1
        self.change_y = 0

        self.dead = False

        self.direction = "Left"

        self.level = level

    def update(self, dt):
        """
        Moves the enemy, handles platform collision.
        Uses flip() method to flip the sprite when hitting a wall
        on the x-axis
        """
        if not self.dead:
            self.calc_grav(dt)

            self.y_pos += float(self.change_y) * dt
            self.rect.y = self.y_pos

            for block in self.level.blockers:
                if self.rect.colliderect(block):
                    if self.change_y > 0:
                        self.rect.bottom = block.top
                        self.y_pos = self.rect.y
                    elif self.change_y < 0:
                        self.rect.top = block.bottom
                        self.y_pos = self.rect.y
                    self.change_y = 0
                #block.collide()
                #if isinstance(block, platforms.MovingPlatform):
                #    self.rect.x += block.change_x

            self.x_pos += float(self.change_x) * dt
            self.rect.x = self.x_pos

            for block in self.level.blockers:
                if self.rect.colliderect(block):
                    if self.change_x < 0:
                        self.rect.left = block.right
                        self.x_pos = self.rect.x
                        self.change_x *= -1
                        self.flip()
                    elif self.change_x > 0:
                        self.rect.right = block.left
                        self.x_pos = self.rect.x
                        self.change_x *= -1
                        self.flip()
        elif self.dead:
            self.calc_grav(dt)

            self.y_pos += float(self.change_y) * dt
            self.rect.y = self.y_pos

            self.x_pos += float(self.change_x) * dt
            self.rect.x = self.x_pos

        if self.rect.y > 5000:
            self.kill()

    def kill_init(self):
        self.dead = True
        self.level.kill_animation_list.add(self)
        self.level.enemy_list.remove(self)
        self.change_y = -5 # Make the enemy fly a small distance into the air
        self.image = pygame.transform.flip(self.image, False, True) # Flip the enemy upside down


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
            self.x_pos = self.rect.x


        if self.direction == "Right" and self.change_x < 0:
            self.direction = "Left"
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(topleft=(x, y))
            self.x_pos = self.rect.x

    def calc_grav(self, dt):
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.35 * dt


class EdgeWalker(Enemy):
    """
    More advanced enemy. Turns around at ledges of platforms and uses
    sprite animation.
    """
    def __init__(self, x, y, level):
        super(EdgeWalker, self).__init__(x, y, level)

        self.image = pygame.image.load(path.join(img_dir, "worm", "frame-1.png")).convert_alpha()
        self.image =pygame.transform.scale(self.image, (72, 76))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.x_pos = x
        self.y_pos = y

        self.onground = False
        self.dead = False

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
            image = pygame.transform.scale(image, (72, 76))
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

    def update(self, dt):
        """ Handles movement and platform collision """
        if not self.dead:
            self.calc_grav(dt)
            self.animate()

            # Create a point to the bottom left or bottom right of the enemy
            m = (1, 1) if self.change_x > 0 else (-1, 1)
            point = self.rect.bottomright if self.change_x > 0 else self.rect.bottomleft
            fp = map(sum, zip(m, point))

            # Check if the created point does collide with a platform
            collide = any(p for p in self.level.blockers if p.collidepoint(fp))

            # If there is no collision, turn the enemy around (if the enemy is not in the air)
            if not collide:
                if self.onground:
                    self.change_x *= -1
                    self.flip()

            self.y_pos += float(self.change_y) * dt
            self.rect.y = self.y_pos

            for block in self.level.blockers:
                if self.rect.colliderect(block):
                    self.onground = True
                    if self.change_y > 0:
                        self.rect.bottom = block.top
                        self.y_pos = self.rect.y
                    elif self.change_y < 0:
                        self.rect.top = block.bottom
                        self.y_pos = self.rect.y

                    self.change_y = 0

            self.x_pos += float(self.change_x) * dt
            self.rect.x = self.x_pos

            for block in self.level.blockers:
                if self.rect.colliderect(block):
                    if self.change_x < 0:
                        self.rect.left = block.right
                        self.x_pos = self.rect.x
                        self.change_x *= -1
                        self.flip()
                    elif self.change_x > 0:
                        self.rect.right = block.left
                        self.x_pos = self.rect.x
                        self.change_x *= -1
                        self.flip()

        elif self.dead:
            self.calc_grav(dt)

            self.y_pos += float(self.change_y) * dt
            self.rect.y = self.y_pos

            self.x_pos += float(self.change_x) * dt
            self.rect.x = self.x_pos

        if self.rect.y > 5000:
            self.kill()