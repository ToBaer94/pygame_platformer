# pygame_platformer

Simple game to teach myself programming. Requires python 2.7 and pygame 1.9.2a0 win32 bit: http://www.pygame.org/download.shtml

Uses pytmx version 3.20 to allow loading of .tmx map files. pytmx is licensed under LGPL v3:  https://github.com/bitcraft/PyTMX

To update the pytmx library, download the newest build from https://github.com/bitcraft/PyTMX and replace the pytmx folder
with the pytmx folder from bitcraft's repository.
 
Updating pytmx possibly requires you to modifiy the tilerenderer.py file.

pytmx additionally uses the "six"-module by "gutworth". "six" is licensed under MIT: https://bitbucket.org/gutworth/six


Controls:

Overworld - Arrow keys for movement, space to enter a level. You need to beat the previous level to access the next one. Currently 3 levels implemented.

Level - Arrow keys for directional movement and jumping, space to throw fireballs after picking up a mushroom.



Credit for most of the art goes to Kenney: http://opengameart.org/content/platformer-art-deluxe

Credit for the overworld art goes to Buch: http://opengameart.org/content/the-field-of-the-floating-islands

Credit for the Land Monster and the Worm-type Enemy goes to bevouliin: http://opengameart.org/content/bevouliin-free-sprite-sheets-underground-worm-monster
http://opengameart.org/content/bevouliin-free-sprite-sheets-monster-game-asset
