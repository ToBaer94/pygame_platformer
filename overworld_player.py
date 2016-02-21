import pygame as pg


class Player(pg.sprite.Sprite):
    """ Player class for the overworld character used to select a level """
    def __init__(self, start, paths, levels):
        super(Player, self).__init__()

        self.image = pg.image.load("assets\sprites\player_character\ov_player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = start.x
        self.rect.y = start.y

        # Predictor is a rect used to check for a collision X pixel in a direction
        # Checks for collision with self.paths. If a collision happens the player can move
        self.predictor = self.rect.copy()

        # Rects for the paths and levels to allow or stop movement
        self.paths = paths
        self.levels = levels

        # Flag to prevent movement while moving
        self.moving = False

        # Pressing an arrow key causes map_state.py to change this attribute
        # The predictor rect moves X pixels in self.direction
        # and checks for a collision with path
        self.direction = None

    def update(self):
        self.check_valid_move()
        self.move()

    def check_valid_move(self):
        """ Check if the player is allowed to move in a direction """
        if self.moving == False:
            if self.direction == "right":
                self.predictor.x += 33
                for path in self.paths:
                    if self.predictor.colliderect(path):
                        self.moving = True
                        self.rect.x += 17
                self.predictor.x -= 33
            if self.direction == "left":
                self.predictor.x += -33
                for path in self.paths:
                    if self.predictor.colliderect(path):
                        self.moving = True
                        self.rect.x += -17
                self.predictor.x += 33

            if self.direction == "down":
                self.predictor.y += 33
                for path in self.paths:
                    if self.predictor.colliderect(path):
                        self.moving = True
                        self.rect.y += 17
                self.predictor.y -= 33

            if self.direction == "up":
                self.predictor.y += -33
                for path in self.paths:
                    if self.predictor.colliderect(path):
                        self.moving = True
                        self.rect.y += -17
                self.predictor.y += 33

    def move(self):
        if self.moving == True:
            if self.direction == "right":
                self.rect.x += 2
                self.set_level_position()

            if self.direction == "left":
                self.rect.x += -2
                self.set_level_position()

            if self.direction == "down":
                self.rect.y += 2
                self.set_level_position()

            if self.direction == "up":
                self.rect.y += -2
                self.set_level_position()

    def set_level_position(self):
        for level in self.levels:
            if self.rect.colliderect(level):
                self.moving = False
                self.rect.x = level.x
                self.rect.y = level.y
                self.direction = None
                self.predictor = self.rect.copy()





