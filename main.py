import pygame
from constants import *
from player_1 import Player
import levels


def main():

    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platform Jumper")

    player = Player() # Create the player

    level_list = [] # Set up the list of levels
    level_list.append(levels.Level_01(player))
    #level_list.append( Level_02(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group() # Sprite group used for the player independent of the level
    player.level = current_level # Set first level in player class

    active_sprite_list.add(player)

    done = False

    clock = pygame.time.Clock()

    target_fps = 60.0 # Intended FPS maximum
    ms_per_sec = 1000.0 # Ms in one second
    desired_frame_time = float(ms_per_sec) / float(target_fps) # Amount of ms per frame at target_fps
    max_delta_time = 1.0 # Max step the game physics get moved by

    current_time = pygame.time.get_ticks() # time since pygame.init()

    while not done:
        frame_time = clock.tick(60)
        total_delta_time = float(frame_time) / float(desired_frame_time) # Total amount of steps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

                if event.key == pygame.K_SPACE:
                    player.fire()

        while total_delta_time > 0.0: # While there still have to be made steps to keep physics constant
            # Update physics by 1 step until enough steps have been made
            delta_time = min(total_delta_time, max_delta_time)
            active_sprite_list.update(delta_time)
            current_level.update(delta_time)
            total_delta_time -= delta_time


        # Camera / Viewport control
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            player.x_pos = player.rect.x
            current_level.shift_world(-diff)

        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            if player.level.world_shift >= -5:
                pass
            else:
                player.rect.left = 120
                player.x_pos = player.rect.x
            current_level.shift_world(diff)

        # Level control
        if current_level.world_shift < current_level.level_limit and player.rect.x >= 450:
            player.rect.x = 120
            player.x_pos = player.rect.x
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = 560 - player.rect.height
            else:
                #If last level, rest viewport and player position to level start
                current_level.shift_world((-current_level.world_shift))
                current_level.world_shift = 0
                player.rect.y = 560 - player.rect.height
                print "reached the end of the last level"

        # Enemy collision detection (Probably to be moved out of the main file later)
        enemy_hit_list = pygame.sprite.spritecollide(player, player.level.enemy_list, True)
        for enemy in enemy_hit_list:
            # No damage is taken when jumping on top
            if player.rect.collidepoint(enemy.rect.midtop) \
                    or player.rect.collidepoint(enemy.rect.x + 7, enemy.rect.y)\
                    or player.rect.collidepoint(enemy.rect.x + enemy.rect.width - 7, enemy.rect.y):
                print "hit on top"
            else:
                # If the player has one, remove the power_up
                if player.status == "Fire":
                    player.hurt()
                    print player.status
                # Else end the game (placeholder till i create a game over screen and/or extra lives)
                else:
                    print "You're dead"
                    done = True

        # End the game if the player falls into a gap (placeholder)
        if player.rect.top > SCREEN_HEIGHT:
            print "Game over"
            done = True

        # Draw everything
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()