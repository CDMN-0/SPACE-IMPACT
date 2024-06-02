import pygame, sys
from game import Game
from pause import PauseMenu
from menu import MainMenu
from victory import VictoryScreen
from gameover import GameOverScreen

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GREY = (29, 29, 27)

font = pygame.font.Font('Fonts/Retro.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Impact by Nolasco BT 605")

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
victory = VictoryScreen(SCREEN_WIDTH, SCREEN_HEIGHT, font, game.player_score)
game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT, font)
pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

clock = pygame.time.Clock()
paused = False
menu_active = True
victory_state = False
game_over = False
count = 0

main_menu.play_menu_music()

def resume_game():
    global paused
    paused = False

def return_to_main_menu():
    global menu_active
    menu_active = True    

def victory_menu():
    global victory_state
    victory_state = True

while True:
    while menu_active:
        game.stop_game_music()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = main_menu.handle_click(pygame.mouse.get_pos())
                if clicked_button == "start":
                    main_menu.stop_menu_music()
                    game.play_game_music()
                    menu_active = False
                    game.game_active = True
                    count = 0
                    print("MENU ACTIVE IS: ", menu_active)
                    break

        screen.fill(GREY)
        main_menu.draw(screen)
        pygame.display.update()
        clock.tick(60)

    while not menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    pause_menu.handle_click(pygame.mouse.get_pos(), resume_game, return_to_main_menu)
                    if not pause_menu.paused: 
                        paused = False  
                elif victory_state:
                    victory.draw(screen)
                    pygame.display.update()
                    clock.tick(60)
                    mouse_pos = pygame.mouse.get_pos()
                    if victory.retry_button_rect.collidepoint(mouse_pos):
                        victory.stop_victory_music()
                        game.play_game_music()
                        game.reset_game() 
                        game.game_active = True
                        victory_state = False  
                        game_over = False
                        count = 0
                    elif victory.return_button_rect.collidepoint(mouse_pos):
                        victory.stop_victory_music()
                        main_menu.play_menu_music()
                        game.reset_game()  
                        game.game_active = True
                        menu_active = True 
                        victory_state = False  
                        game_over = False
                        count = 0
                    elif victory.quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif game_over:
                    game_over_screen.draw(screen)
                    game.current_stage == 5
                    pygame.display.update()
                    clock.tick(60)
                    mouse_pos = pygame.mouse.get_pos()
                    if game_over_screen.retry_button_rect.collidepoint(mouse_pos):
                        game_over_screen.stop_game_over_music()
                        game.play_game_music()
                        game.reset_game() 
                        game.game_active = True
                        game_over = False  
                        victory_state = False
                        count = 0
                    elif game_over_screen.return_button_rect.collidepoint(mouse_pos):
                        game.game_active = True
                        game_over_screen.stop_game_over_music()
                        main_menu.play_menu_music()
                        game.reset_game() 
                        menu_active = True  
                        game_over = False  
                        victory_state = False
                        count = 0
                    elif game_over_screen.quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        if not paused:     
            screen.fill(GREY)
            game.background.draw(screen)
            game.create_aliens()
            game.spaceship_group.update()
            game.update_aliens()
            game.check_for_collisions()
            game.boss_lasers_group.update()

        if game.check_for_victory():
            victory_state = True
            victory.player_score = game.player_score

        if game.player_health <= 0:
            game_over = True
            if count == 0:
                game.stop_game_music()
                game_over_screen.play_game_over_music()
                count = 1

        if menu_active:
            if count == 0:
                game.stop_game_music()
                main_menu.play_menu_music()
                count = 1

        if game_over:
            screen.fill(GREY)
            game_over_screen.draw(screen)
            pygame.display.update()
            clock.tick(60)

        elif victory_state:
            if count == 0:
                game.stop_game_music()
                victory.play_victory_music()
                count = 1
            screen.fill(GREY)
            victory.draw(screen)
            pygame.display.update()
            clock.tick(60)

        if paused:
            pause_menu.draw(screen)
        elif game.game_active:
            game.spaceship_group.draw(screen)   
            if game.spaceship_group.sprite: 
                game.spaceship_group.sprite.lasers_group.draw(screen)
            game.aliens_group.draw(screen)
            game.draw_boss(screen)
            game.render_hud(screen)
            game.boss_lasers_group.draw(screen) 
        else:
            game.spaceship_group.draw(screen)   
            game.aliens_group.draw(screen)
            game.draw_boss(screen)
            game.render_hud(screen)
            game.boss_lasers_group.draw(screen) 

        pygame.display.update()
        clock.tick(60)
