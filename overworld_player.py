import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, start, paths, levels):
        super(Player, self).__init__()

        self.image = pg.image.load("ov_player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = start.x
        self.rect.y = start.y

        self.predictor = self.rect.copy()

        self.paths = paths
        self.levels = levels

        self.moving = False
        self.direction = None

    def update(self):
        self.check_valid_move()
        self.move()

    def check_valid_move(self):
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





