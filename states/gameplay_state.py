import pygame as pg
from base_state import GameState
from player_level import Player
import levels


class GamePlay(GameState):
    """ State running when playing a level """
    def __init__(self):
        super(GamePlay, self).__init__()
        self.screen = pg.display.get_surface()
        self.screen_rect = pg.display.get_surface().get_rect()

        self.next_state = "MAP"

    def startup(self, persistent):
        """ Set up everything for the passed in level. startup runs when switch state"""
        self.player = Player()
        self.level = None

        # Player lives
        self.persist["lives"] = persistent["lives"]

        # Access the correct level
        # persistent["level"] follows the naming scheme "Level0" + str("level number")
        # The level.tmx files are named the same way
        self.level_number = persistent["level"]
        self.persist = persistent
        self.level_class = getattr(levels, self.level_number)

        # Create an instance of the actual level with reference to the player
        self.level = self.level_class(self.player)

        # Give the player a reference to the level as well.
        self.player.level = self.level
        self.player.set_position()
        self.active_sprite_list = pg.sprite.Group()
        self.active_sprite_list.add(self.player)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                    self.player.fire()
            if event.key == pg.K_UP:
                self.player.jump()
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_LEFT]:
            self.player.go_left()
        elif not key_pressed[pg.K_LEFT] and self.player.acc.x < 0:
            self.player.stop()
        if key_pressed[pg.K_RIGHT]:
            self.player.go_right()
        elif not key_pressed[pg.K_RIGHT] and self.player.acc.x > 0:
            self.player.stop()

    def update(self, dt):
        self.level.update(dt)
        self.active_sprite_list.update(dt)
        self.move_camera_x(dt)
        self.move_camera_y(dt)

        if self.player.rect.top > self.screen_rect.height or self.player.dead:
            print "You're dead"
            self.persist["lives"] -= 1
            self.done = True

        if self.player.rect.colliderect(self.level.end_point):
            self.persist[self.level_number] = True
            print self.persist
            self.done = True

    def move_camera_x(self, dt):
        """ If the player is far to the left or to the right of the viewport, move the map accordingly
        If the viewport collides with the edge of the map, stop moving """
        if self.player.pos.x >= 500.0:
            if self.screen_rect.colliderect(self.level.right_boundary):
                pass
            else:
                diff = self.player.pos.x - 500.0
                self.player.pos.x = 500
                self.player.rect.x = self.player.pos.x
                self.level.shift_world_x(-diff)

        if self.player.pos.x <= 120:
            if self.screen_rect.colliderect(self.level.left_boundary):
                pass
            else:
                diff = 120 - self.player.pos.x
                self.player.pos.x = 120
                self.player.rect.x = self.player.pos.x
                self.level.shift_world_x(diff)

    def move_camera_y(self, dt):
        """ If the player is far to the top or to the bottom of the viewport, move the map accordingly
        If the viewport collides with the edge of the map, stop moving """
        if self.player.pos.y > 320.0:
            if self.screen_rect.colliderect(self.level.bottom_boundary):
                pass
            else:
                diff = self.player.pos.y - 320.0
                self.player.pos.y = 320.0
                self.player.rect.y = self.player.pos.y
                self.level.shift_world_y(-diff)

        if self.player.pos.y <= 120:
            if self.screen_rect.colliderect(self.level.top_boundary):
                pass
            else:
                diff = 120 - self.player.pos.y
                self.player.pos.y += diff
                self.player.rect.y = self.player.pos.y
                self.level.shift_world_y(diff)

    def draw(self, screen):
        self.level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)