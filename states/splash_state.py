from base_state import GameState
import pygame as pg


class SplashScreen(GameState):
    """ State class representing the opening screen. Sets the next state to map_state when pressing space """
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render("Platform Jumper", True, pg.Color("yellow"))
        self.title_rect = self.title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height  // 4))

        self.start_title = self.font.render("Press Space to start", True, pg.Color("red"))
        self.start_title_rect = self.start_title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height * 3 // 4))
        self.next_state = "MAP"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self.done = True

    def draw(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.start_title, self.start_title_rect)