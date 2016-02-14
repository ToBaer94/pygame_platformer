import pygame as pg


class GameState(object):
    """ Base state all other states inherit from """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {} # Used to pass information between states
        self.font = pg.font.Font(None, 96)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass