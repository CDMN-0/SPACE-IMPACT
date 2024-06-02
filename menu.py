import pygame, sys

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font_title = pygame.font.Font('Fonts/Retro.ttf', 64)
        self.font_button = pygame.font.Font('Fonts/Retro.ttf', 32)

        self.title_text = self.font_title.render("SPACE IMPACT: REVOLUTION", True, pygame.Color('white'))
        self.start_button_text = self.font_button.render("Start", True, pygame.Color('white'))
        self.quit_button_text = self.font_button.render("Quit", True, pygame.Color('white'))

        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound('Audio/Loops/mp3/Sci-Fi 1 Loop.mp3')

        button_width = 200
        button_height = self.start_button_text.get_height()
        button_x = (screen_width - button_width) // 2
        self.start_button_rect = pygame.Rect(button_x, screen_height // 2, button_width, button_height)
        self.quit_button_rect = pygame.Rect(button_x, screen_height // 2 + 60, button_width, button_height)

    def draw(self, screen):
        screen.blit(self.title_text, (self.screen_width // 2 - self.title_text.get_width() // 2, 100))
        
        pygame.draw.rect(screen, pygame.Color('green'), self.start_button_rect)
        start_button_text_rect = self.start_button_text.get_rect(center=self.start_button_rect.center)
        screen.blit(self.start_button_text, start_button_text_rect)
        
        pygame.draw.rect(screen, pygame.Color('red'), self.quit_button_rect)
        quit_button_text_rect = self.quit_button_text.get_rect(center=self.quit_button_rect.center)
        screen.blit(self.quit_button_text, quit_button_text_rect)

    def handle_click(self, pos):
        if self.start_button_rect.collidepoint(pos):
            self.stop_menu_music
            return "start"
        elif self.quit_button_rect.collidepoint(pos):
            pygame.quit()
            sys.exit()
        else:
            return None
        
    def play_menu_music(self):
        self.menu_music.set_volume(0.5)
        self.menu_music.play(-1) 

    def stop_menu_music(self):
        self.menu_music.stop()
