from base_state import GameState
import pygame as pg


class LevelOpening(GameState):
    """ State class representing the opening screen. Sets the next state to map_state when pressing space """
    def __init__(self):
        super(LevelOpening, self).__init__()
        self.title = None
        self.title_rect = None

        self.start_title = None
        self.start_title_rect = None
        self.next_state = "LEVEL"
        self.drawn = False

    def startup(self, persistent):
        self.persist = persistent
        self.drawn = False

        self.level_name = self.persist["level"]
        self.lives = self.persist["lives"]

        self.title = self.font.render(str(self.level_name), True, pg.Color("red"))

        self.title_rect = self.title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height // 4))

        self.start_title = self.font.render("Lives left: " + str(self.lives),
                                            True, pg.Color("yellow"))

        self.start_title_rect = self.start_title.get_rect(center = (self.screen_rect.width // 2,
                                                          self.screen_rect.height * 3 // 4))

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        # elif event.type == pg.KEYUP:
        #     if event.key == pg.K_SPACE:
        #         self.done = True
    def update(self, dt):
        if self.drawn:

            pg.time.wait(1200)
            print "1000 is over"
            self.done = True

    def draw(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.start_title, self.start_title_rect)
        self.drawn = True
