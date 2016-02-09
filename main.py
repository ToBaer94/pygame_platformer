import pygame
from constants import *
from player_1 import Player
import levels


class GameEngine(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Jumper")
        self.size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(self.size)

        self.target_fps = 60.0 # Intended FPS maximum
        self.ms_per_sec = 1000.0 # Ms in one second
        self.desired_frame_time = float(self.ms_per_sec) / float(self.target_fps) # Amount of ms per frame at target_fps
        self.max_delta_time = 1.0 # Max step the game physics get moved by

        self.player = Player()

        self.level_list = [] # Set up the list of levels
        level = levels.Level_01(self.player)
        self.level_list.append(level)

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.player.level = self.current_level
        self.player.set_position()
        self.active_sprite_list = pygame.sprite.Group() # Sprite group used for the player independent of the level
        self.active_sprite_list.add(self.player)

        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.done = False
        self.game_over = True

        self.started = 0

    def run(self):
        while not self.done:
            frame_time = self.clock.tick(self.FPS)

            if self.game_over:
                self.started = 0
                self.game_over_reset()
            if self.started > 2:
                self.handle_events()
                self.update_everything(frame_time)
            self.draw_everything()
            self.started += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.fire()
                if event.key == pygame.K_UP:
                    self.player.jump()
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_a:
                    self.FPS -= 2
                if event.key == pygame.K_s:
                    self.FPS += 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.acc.x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.acc.x > 0:
                    self.player.stop()
            """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            self.player.go_left()
        elif not key_pressed[pygame.K_LEFT] and self.player.acc.x < 0:
            self.player.stop()
        if key_pressed[pygame.K_RIGHT]:
            self.player.go_right()
        elif not key_pressed[pygame.K_RIGHT] and self.player.acc.x > 0:
            self.player.stop()

    def update_everything(self, frame_time):
        total_delta_time = float(frame_time) / float(self.desired_frame_time) # Total amount of steps

        while total_delta_time > 0.0: # While there still have to be made steps to keep physics constant
            # Update physics by 1 step until enough steps have been made
            delta_time = min(total_delta_time, self.max_delta_time)
            self.current_level.update(delta_time) # Current level (enemies, platforms, powerups) update
            self.active_sprite_list.update(delta_time) # Player update
            total_delta_time -= delta_time

        self.move_camera()

        if self.player.rect.colliderect(self.current_level.end_point):
            self.switch_level()

        if self.player.rect.top > SCREEN_HEIGHT or self.player.dead:
            print "Game over"
            self.game_over = True

    def move_camera(self):
        if self.player.pos.x >= 500:
            diff = self.player.pos.x - 500.0
            self.player.pos.x = 500
            self.player.rect.x = self.player.pos.x
            self.current_level.shift_world(-diff)

        if self.player.pos.x <= 120:
            diff = 120 - self.player.pos.x
            if self.player.level.world_shift >= -7:
                pass
            else:
                self.player.pos.x = 120
                self.player.rect.x = self.player.pos.x
            self.current_level.shift_world(diff)

    def switch_level(self):
        if self.current_level_no < len(self.level_list)-1:
            self.current_level_no += 1
            self.current_level = self.level_list[self.current_level_no]
            self.player.level = self.current_level
            self.player.set_position()
        else:
            # If last level, rest viewport and player position to level start
            self.current_level.shift_world((-self.current_level.world_shift))
            self.current_level.world_shift = 0
            self.player.set_position()
            print "reached the end of the last level"

    def draw_everything(self):
        self.current_level.draw(self.screen)
        self.active_sprite_list.draw(self.screen)

        pygame.display.flip()

    def game_over_reset(self):
        self.show_go_screen()
        ###
         # Create the player

        self.player = Player()

        self.level_list = [] # Set up the list of levels
        level = levels.Level_01(self.player)
        self.level_list.append(level)

        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.player.level = self.current_level
        self.player.set_position()
        self.active_sprite_list = pygame.sprite.Group() # Sprite group used for the player independent of the level
        self.active_sprite_list.add(self.player)
        ###
        self.game_over = False

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Platform Jumper", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.draw_text(self.screen, "Arrow keys to move, up to jump, space to throw a fireball after picking up"
                          " a mushroom", 22,  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text(self.screen, "Press space to start the game", 18, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT * 3 // 4)
        pygame.display.flip()
        waiting = True
        while waiting:

            #self.clock.tick(self.FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.done = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def draw_text(self, screen, text, size, x, y):
        font = pygame.font.Font(pygame.font.match_font("comic sans"), size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

class GameLogic(object):
    pass



if __name__ == "__main__":

    game = GameEngine()
    logic = GameLogic()
    game.run()
