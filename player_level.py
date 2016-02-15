import pygame
from spritesheet_functions import SpriteSheet
from os import path
import powerup

vector = pygame.math.Vector2

img_dir = path.join(path.dirname(__file__), "assets", "sprites", "player_character")


class Player(pygame.sprite.Sprite):
    """
    Player class. Holds all sprite images, handles movement, collision with platforms and power ups
    """
    def __init__(self):
        super(Player, self).__init__()

        self.sprite_sheet = SpriteSheet(path.join(img_dir, "p1_spritesheet.png"))
        self.stand_sprite_r = self.sprite_sheet.get_image(67, 196, 66, 92)
        self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.jumping = False
        self.jumping_sprite_r = self.sprite_sheet.get_image(438, 93, 67, 94)
        self.jumping_sprite_l = pygame.transform.flip(self.jumping_sprite_r, True, False)

        self.set_walking_animation()

        self.image = self.stand_sprite_r

        self.rect = self.image.get_rect()

        self.status = "Small" # Power up status

        self.direction = "Right" # Sprite direction

        self.level = None


        self.pos = vector(0, 0)

        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

        self.dead = False

    def set_position(self):
        self.tile_renderer = self.level.tile_renderer

        for tile_object in self.tile_renderer.tmx_data.objects:
            properties = tile_object.__dict__
            if properties["name"] == "Start":
                self.pos.x = properties['x']
                self.pos.y = properties['y']
                print self.pos.x, self.pos.y

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def set_walking_animation(self):
        """
        Called to initiate the walking animations in both directions
        """
        image = self.sprite_sheet.get_image(0, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(73, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(146, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(0, 98, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(73, 98, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(146, 98, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(219, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(292, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(219, 98, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(365, 0, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(292, 98, 72, 97)

        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

    def update(self, dt):
        """
        Updates the player position, handles platform and power up collision (will be moved to its own method)
        Experimental movement that uses floats to allow velocities like 0.5. Also uses experimental change
        to make movement FPS independent.
        """

        self.calc_grav(dt)

        self.vel.x += self.acc.x * dt
        if self.vel.x > 5:
            self.vel.x = 5
        if self.vel.x < -5:
            self.vel.x = -5
        if self.acc.x == 0 and 5 >= self.vel.x > 0:
            self.vel.x -= 0.25 * dt
        if self.acc.x == 0 and -5 <= self.vel.x < 0:
            self.vel.x += 0.25 * dt
        if -0.5 < self.vel.x < 0.5 and self.acc.x == 0:
            self.vel.x = 0

        self.pos.x += self.vel.x * dt
        self.rect.x = self.pos.x

        self.walk_animation()

        self.world_x_collision()

        # Handle item pick up collisions
        item_hit_list = pygame.sprite.spritecollide(self, self.level.item_list, True)
        for item in item_hit_list:
            item.collide()

        # Prevent the player from going off screen
        if self.pos.x <= 0:
            self.rect.x = 1
            self.pos.x = 1
            self.vel.x = 0

        self.vel.y += self.acc.y * dt
        self.pos.y += self.vel.y * dt
        self.rect.y = self.pos.y

        self.enemy_collide()

        if self.jumping:
            if self.direction == "Right":
                self.image = self.jumping_sprite_r
            else:
                self.image = self.jumping_sprite_l

        self.world_y_collision()

    def world_x_collision(self):
        for block in self.level.blockers:
            if self.rect.colliderect(block):

                if self.vel.x > 0:
                    self.rect.right = block.left
                    self.pos.x = self.rect.x
                    self.vel.x = 0
                elif self.vel.x < 0:
                    self.rect.left = block.right
                    self.pos.x = self.rect.x
                    self.vel.x = 0
        for block in self.level.platform_list:
            if self.rect.colliderect(block):
                if self.vel.x > 0:
                    self.rect.right = block.rect.left
                    self.pos.x = self.rect.x
                    self.vel.x = 0
                elif self.vel.x < 0:
                    self.rect.left = block.rect.right
                    self.pos.x = self.rect.x
                    self.vel.x = 0

    def world_y_collision(self):
        self.jumping = True
        for block in self.level.blockers:
            if self.rect.colliderect(block):
                if self.vel.y > 0:
                    self.rect.bottom = block.top
                    self.pos.y = self.rect.y
                    self.jumping = False

                elif self.vel.y < 0:
                    self.rect.top = block.bottom
                    self.pos.y = self.rect.y

                self.vel.y = 0

        for block in self.level.platform_list:
            if self.rect.colliderect(block):
                self.jumping = False
                if self.vel.y > 0:
                    self.rect.bottom = block.rect.top
                    self.pos.y = self.rect.y

                elif self.vel.y < 0:
                    self.rect.top = block.rect.bottom
                    self.pos.y = self.rect.y

                self.vel.y = 0
                block.collide()

    def enemy_collide(self):
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        for enemy in enemy_hit_list:
            # No damage is taken when jumping on top
            if self.rect.collidepoint(enemy.rect.midtop) \
                    or self.rect.collidepoint(enemy.rect.x + 7, enemy.rect.y)\
                    or self.rect.collidepoint(enemy.rect.x + enemy.rect.width - 7, enemy.rect.y):
                print "hit on top"
            else:
                # If the player has one, remove the power_up
                if self.status == "Fire":
                    self.hurt()
                    print self.status

                else:
                    self.dead = True


    def walk_animation(self):
        # If the player is moving, play the correct movement animation
        if self.vel.x != 0:
            pos = self.rect.x + self.level.world_shift_x
            if self.direction == "Right":
                frame = (pos // 20) % len(self.walking_frames_r)
                frame = int(frame)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 20) % len(self.walking_frames_l)
                frame = int(frame)
                self.image = self.walking_frames_l[frame]

        # Else display the idle sprite
        else:
            if self.direction == "Right":
                self.image = self.stand_sprite_r
            else:
                self.image = self.stand_sprite_l

    def calc_grav(self, dt):
        """
        Handles gravity
        """
        if self.vel.y == 0:
            self.vel.y = 1

        else:
            self.acc.y = 0.35


    def jump(self):
        """
        Moves the player down 2 pixels to check if he is on the ground, then sets him back up 2 pixels.
        If on the ground, sets y-velocity.
        """
        if self.jumping == False:
            self.vel.y = -11
            self.jumping = True

    def go_left(self):
        self.acc.x = -0.5
        self.direction = "Left"

    def go_right(self):
        self.acc.x = 0.5
        self.direction = "Right"

    def stop(self):
        self.acc.x = 0

    def powerup(self):
        """
        Checks if the player has already picked up a Fire power up. If that isn't the case, changes all sprites
        and sets the player status to "Fire".
        """

        if self.status != "Fire":
            self.status = "Fire"

            self.sprite_sheet = SpriteSheet(path.join(img_dir,"p3_spritesheet.png"))
            self.stand_sprite_r = self.sprite_sheet.get_image(67, 196, 66, 92)
            self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
            self.walking_frames_l = []
            self.walking_frames_r = []
            self.jumping_sprite_r = self.sprite_sheet.get_image(438, 93, 67, 94)
            self.jumping_sprite_l = pygame.transform.flip(self.jumping_sprite_r, True, False)
            self.set_walking_animation()
            self.image = self.walking_frames_r[0]

    def hurt(self):
        """ Changes the players status and sprites from "Fire" to "Small" when getting hurt """
        if self.status == "Fire":
            self.status = "Small"

            self.sprite_sheet = SpriteSheet(path.join(img_dir,"p1_spritesheet.png"))
            self.stand_sprite_r = self.sprite_sheet.get_image(67, 196, 66, 92)
            self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
            self.walking_frames_l = []
            self.walking_frames_r = []
            self.jumping_sprite_r = self.sprite_sheet.get_image(438, 93, 67, 94)
            self.jumping_sprite_l = pygame.transform.flip(self.jumping_sprite_r, True, False)
            self.set_walking_animation()
            self.image = self.walking_frames_r[0]

    def fire(self):
        """
        If the player is currently in a power up state and there are less than 4 fireballs in the game,
        spawns a fireball at the player location
        """

        if self.status == "Fire":
            if len(self.level.effect_list) < 4:
                fireball = powerup.Fireball(self, self.level, self.direction)
                self.level.effect_list.add(fireball)
