import pygame
import constants
from platforms import MovingPlatform, SpecialBlock
from spritesheet_functions import SpriteSheet
from os import path
import powerup

img_dir = path.join(path.dirname(__file__), "player_character")


class Player(pygame.sprite.Sprite):
    """
    Player class. Holds all sprite images, handles movement, collision with platforms and power ups
    """
    def __init__(self):
        super(Player, self).__init__()

        self.sprite_sheet = SpriteSheet(path.join(img_dir, "p1_spritesheet.png"))
        self.stand_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(67, 196, 66, 92), (40, 56))
        self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.jumping = False
        self.jumping_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(438, 93, 67, 94), (40, 56))
        self.jumping_sprite_l = pygame.transform.flip(self.jumping_sprite_r, True, False)

        self.set_walking_animation()

        self.image = self.walking_frames_r[0]

        self.rect = self.image.get_rect()

        self.status = "Small" # Power up status

        self.direction = "Right" # Sprite direction
        self.change_x = 0
        self.change_y = 0

        self.level = None

    def set_walking_animation(self):
        """
        Called to initiate the walking animations in both directions
        """
        image = self.sprite_sheet.get_image(0, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(73, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(146, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(0, 98, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(73, 98, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(146, 98, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(219, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(292, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(219, 98, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(365, 0, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = self.sprite_sheet.get_image(292, 98, 72, 97)
        image = pygame.transform.scale(image, (40, 56))
        self.walking_frames_r.append(image)

        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

    def update(self):
        """
        Updates the player position, handles platform and power up collision (will be moved to its own method)
        """
        self.calc_grav()

        # If the player is moving, play the correct movement animation
        self.rect.x += self.change_x
        if self.change_x != 0:
            pos = self.rect.x + self.level.world_shift
            if self.direction == "Right":
                frame = (pos // 30) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
        # Else display the idle sprite
        else:
            if self.direction == "Right":
                self.image = self.stand_sprite_r
            else:
                self.image = self.stand_sprite_l

        # Handle platform collisions after x-axis movement
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Handle power up collisions
        item_hit_list = pygame.sprite.spritecollide(self, self.level.item_list, True)
        for item in item_hit_list:
            item.collide()

        # Prevent the player from going off screen
        if self.rect.x <= 0:
            self.rect.x = 0

        self.rect.y += self.change_y

        # Handle platform collision after y-axis movement
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if block_hit_list:
            self.jumping = False
        else:
            # Check if the player is not touching a platform after y-axis movement, set jumping sprite
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2
            if not platform_hit_list:
                if self.direction == "Right":
                    self.image = self.jumping_sprite_r
                else:
                    self.image = self.jumping_sprite_l

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

            block.collide() # Call collide method for specific platforms (item block, moving platform)

    def calc_grav(self):
        """
        Handles gravity
        """
        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += 0.35

    def jump(self):
        """
        Moves the player down 2 pixels to check if he is on the ground, then sets him back up 2 pixels.
        If on the ground, sets y-velocity.
        """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0:
            self.change_y = -10
            self.jumping = True

    def go_left(self):
        self.change_x = -4
        self.direction = "Left"

    def go_right(self):
        self.change_x = 4
        self.direction = "Right"

    def stop(self):
        self.change_x = 0

    def powerup(self):
        """
        Checks if the player has already picked up a Fire power up. If that isn't the case, changes all sprites
        and sets the player status to "Fire".
        """

        if self.status != "Fire":
            self.status = "Fire"

            self.sprite_sheet = SpriteSheet(path.join(img_dir,"p3_spritesheet.png"))
            self.stand_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(67, 196, 66, 92), (40, 56))
            self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
            self.walking_frames_l = []
            self.walking_frames_r = []
            self.jumping_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(438, 93, 67, 94), (40, 56))
            self.jumping_sprite_l = pygame.transform.flip(self.jumping_sprite_r, True, False)
            self.set_walking_animation()
            self.image = self.walking_frames_r[0]

    def hurt(self):
        """ Changes the players status and sprites from "Fire" to "Small" when getting hurt """
        if self.status == "Fire":
            self.status = "Small"

            self.sprite_sheet = SpriteSheet(path.join(img_dir,"p1_spritesheet.png"))
            self.stand_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(67, 196, 66, 92), (40, 56))
            self.stand_sprite_l = pygame.transform.flip(self.stand_sprite_r, True, False)
            self.walking_frames_l = []
            self.walking_frames_r = []
            self.jumping_sprite_r = pygame.transform.scale(self.sprite_sheet.get_image(438, 93, 67, 94), (40, 56))
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
                fireball = powerup.Fireball()
                fireball.player = self
                fireball.direction = self.direction
                fireball.spawn(self.level)
                self.level.effect_list.add(fireball)