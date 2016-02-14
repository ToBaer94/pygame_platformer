import pygame as pg
from base_state import GameState
import tilerenderer


class Map(GameState):
    """ Map class handling the overworld screen. Sets the next state to gameplay_state
     when pressing space while the character is positioned on a valid spot (on a level) """
    def __init__(self):
        super(Map, self).__init__()
        import overworld_player as playerobject

        self.tmx_file = "overworld.tmx"
        self.tile_renderer = tilerenderer.Renderer(self.tmx_file)
        self.map_surface = self.tile_renderer.make_map()
        self.map_rect = self.map_surface.get_rect()

        self.lives = 3

        self.start = None
        self.path_list = [] # Rects on all paths. Used to check for allowed moves.
        self.level_collision_list = [] # Rects used to stop the player when he reaches a level position
        self.level_list = [] # Rects representing each level
        self.text_pos_list = [] # List of rectangle positions for text
        self.text_list = [] # List of rendered font objects

        self.next_state = "LEVEL"

        # Create rects from objects on the map's object layer. Used for varying collision checks
        self.create_collision_objects()

        self.create_text() # Creates the text for each text field

        # Creates the player with reference to various rects for collision
        self.player = playerobject.Player(self.start, self.path_list, self.level_collision_list)
        self.sprite_list = pg.sprite.Group()
        self.sprite_list.add(self.player)

    def create_collision_objects(self):
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
                    self.text_pos_list.append(new_rect)
                for i in range(1, 6):
                    if properties["name"] == ("level" + str(i)):
                        x = properties['x']
                        y = properties['y']
                        width = properties['width']
                        height = properties['height']
                        new_rect = pg.Rect(x, y, width, height)
                        self.level_list.append(new_rect)

    def create_text(self):
        for index, location in enumerate(self.text_pos_list):
            font = pg.font.Font(None, 24)
            text = font.render("Level" + " " + str(index + 1), True, pg.Color("black"))
            self.text_list.append(text)


    def startup(self, persistent):
        """ Startup when the state is set. Tries to update the life count of the player
        and updates the "persistent" dictionary used to pass on information between states"""
        try:
            self.lives = persistent["lives"]
        except:
            print "exception"

        self.persist = persistent

    def get_event(self, event):
        """ Handle events """
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if not self.player.moving:
                    self.player.direction = "right"
            elif event.key == pg.K_LEFT:
                if not self.player.moving:
                    self.player.direction = "left"
            elif event.key == pg.K_DOWN:
                if not self.player.moving:
                    self.player.direction = "down"
            elif event.key == pg.K_UP:
                if not self.player.moving:
                    self.player.direction = "up"

            # If the player presses space, the game checks if he is allowed to enter the level
            # The game checks the self.persist dictionary if the level name as key has the value True
            # If he isnt allowed, the game catches a KeyError as the key:value pair isn't in the dict
            elif event.key == pg.K_SPACE:
                for index, level in enumerate(self.level_list):
                    if self.player.rect.colliderect(level):
                        # If the player is on the rect of level 1 (index 0 in self.leve_list)
                        if index == 0:
                            print "should be first level"
                            level_name = "Level_0" + str(index+1)
                            self.persist["level"] = level_name
                            self.persist["lives"] = self.lives
                            self.done = True
                        # Else check if the player is allowed to enter the level
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

    def update(self, dt):
        self.player.update()
        if self.lives <= 0:
            print "You lost all your lives. Game Over"
            self.quit = True

    def draw(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.map_surface, (self.screen_rect))

        # Iterate through the list of textboxes and blit them on screen
        for item, index in zip(self.text_list, self.text_pos_list):
            screen.blit(item, (index))
        self.sprite_list.draw(screen)