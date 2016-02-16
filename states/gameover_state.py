from base_state import GameState
import pygame as pg


class GameOver(GameState):
    """ State class representing the opening screen. Sets the next state to map_state when pressing space """
    def __init__(self):
        super(GameOver, self).__init__()
        self.title = self.font.render("You lost all of your lives", True, pg.Color("yellow"))
        self.title_rect = self.title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height  // 4))
        self.game_over_text = self.font.render("Game Over", True, pg.Color("yellow"))
        self.game_over_rect = self.game_over_text.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height * 2 // 5))

        self.start_title = self.font.render("Press Space to restart the game", True, pg.Color("red"))
        self.start_title_rect = self.start_title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height * 3 // 4))
        self.next_state = "MAP"


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self.persist = {}
                self.persist["lives"] = 3
                self.done = True

    def draw(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.game_over_text, self.game_over_rect)
        screen.blit(self.start_title, self.start_title_rect)