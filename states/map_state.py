import pygame as pg
from base_state import GameState
import tilerenderer


class Map(GameState):
    def __init__(self):
        super(Map, self).__init__()
        import overworld_player as playerobject

        self.tmx_file = "overworld.tmx"
        self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
        self.map_surface = self.tile_renderer.make_map()
        self.map_rect = self.map_surface.get_rect()

        self.lives = 3


        self.start = None
        self.path_list = []
        self.level_collision_list = []
        self.level_list = []
        self.text_list = []
        self.text_list_2 = []
        self.text_pos_list = []



        self.next_state = "LEVEL"

        for object_group in self.tile_renderer.tmx_data.objectgroups:
            for tile_object in object_group:
                properties = tile_object.__dict__

                if properties["name"] == "start":
                    x = properties['x']
                    y = properties['y']
                    width = properties['width']
                    height = properties['height']
                    new_rect = pg.Rect(x, y, width, height)
                    self.start = new_rect
                if properties["name"] == "path":
                    x = properties['x']
                    y = properties['y']
                    width = properties['width']
                    height = properties['height']
                    new_rect = pg.Rect(x, y, width, height)
                    self.path_list.append(new_rect)
                if properties["name"] == "level":
                    x = properties['x']
                    y = properties['y']
                    width = properties['width']
                    height = properties['height']
                    new_rect = pg.Rect(x, y, width, height)
                    self.level_collision_list.append(new_rect)
                if properties["name"] == "text":
                    x = properties['x']
                    y = properties['y']
                    width = properties['width']
                    height = properties['height']
                    new_rect = pg.Rect(x, y, width, height)
                    self.text_list.append(new_rect)
                for i in range(1, 6):
                    if properties["name"] == ("level" + str(i)):
                        x = properties['x']
                        y = properties['y']
                        width = properties['width']
                        height = properties['height']
                        new_rect = pg.Rect(x, y, width, height)
                        self.level_list.append(new_rect)

        self.create_text()
        self.player = playerobject.Player(self.start, self.path_list, self.level_collision_list)
        self.sprite_list = pg.sprite.Group()
        self.sprite_list.add(self.player)

    def create_text(self):
        for index, location in enumerate(self.text_list):
            font = pg.font.Font(None, 24)
            text = font.render("Level" + " " + str(index + 1), True, pg.Color("black"))
            self.text_list_2.append(text)
            self.text_pos_list.append(location)




    def startup(self, persistent):
        try:
            self.lives = persistent["lives"]
        except:
            print "exception"

        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if self.player.moving == False:
                    self.player.direction = "right"
            elif event.key == pg.K_LEFT:
                if self.player.moving == False:
                    self.player.direction = "left"
            elif event.key == pg.K_DOWN:
                if self.player.moving == False:
                    self.player.direction = "down"
            elif event.key == pg.K_UP:
                if self.player.moving == False:
                    self.player.direction = "up"

            elif event.key == pg.K_SPACE:
                for index, level in enumerate(self.level_list):
                    if self.player.rect.colliderect(level):
                        if index == 0:
                            print "should be first level"
                            level_name = "Level_0" + str(index+1)
                            self.persist["level"] = level_name
                            self.persist["lives"] = self.lives
                            self.done = True
                        else:
                            try:
                                level_name = "Level_0" + str(index)
                                if self.persist[level_name]:
                                    level_name = "Level_0" + str(index+1)
                                    self.persist["level"] = level_name
                                    self.persist["lives"] = self.lives
                                    self.done = True


                            except KeyError:
                                print "you must beat" + " " + level_name + " " + "first"


        # elif event.type == pg.KEYUP:
         #   self.change = 0

    def update(self, dt):
        self.player.update()
        if self.lives <= 0:
            print "You lost all your lives. Game Over"
            self.quit = True


    def draw(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.map_surface, (self.screen_rect))
        for item, index in zip(self.text_list_2, self.text_pos_list):
            screen.blit(item, (index))
        self.sprite_list.draw(screen)