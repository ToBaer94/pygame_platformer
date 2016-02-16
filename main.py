import sys
import pygame as pg
from states.splash_state import SplashScreen
from states.map_state import Map
from states.gameplay_state import GamePlay
from states.level_start_state import LevelOpening
from states.gameover_state import GameOver


class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen

        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.target_fps = 60.0
        self.ms_per_sec = 1000.0
        self.desired_frame_time = self.ms_per_sec / self.target_fps
        self.max_step = 1.0

        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        print self.state.persist
        current_state = self.state_name
        next_state = self.state.next_state
        print current_state, next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist

        self.state = self.states[next_state]
        self.state.screen = self.screen
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:

            self.event_loop()

            frame_time = self.clock.tick(self.fps)
            total_dt = frame_time / self.desired_frame_time
            while total_dt > 0.0:
                delta_time = min(total_dt, self.max_step)
                self.update(delta_time)
                total_dt -= delta_time

            self.draw()
            pg.display.flip()







if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("Platform Jumper 2")
    screen = pg.display.set_mode((800, 600))
    states = {"SPLASH": SplashScreen(),
              "MAP": Map(),
              "LEVEL": GamePlay(),
              "LEVELPREVIEW": LevelOpening(),
              "GAMEOVER": GameOver()
                  }
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()














