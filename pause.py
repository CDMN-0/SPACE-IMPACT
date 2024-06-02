import pygame, sys

class PauseMenu:
    def __init__(self, screen_width, screen_height, font=None, font_size=24, paused=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paused = paused 
        font = pygame.font.Font('Fonts/Retro.ttf', 16)
        self.resume_button = font.render("Resume", True, pygame.Color('white'))
        self.return_button = font.render("Return to Menu", True, pygame.Color('white'))
        self.quit_button = font.render("Quit", True, pygame.Color('white'))

        button_width = 200
        button_height = self.resume_button.get_height()
        button_x = (screen_width - button_width) // 2

        self.resume_button_rect = pygame.Rect(button_x, screen_height // 2 - 50, button_width, button_height)
        self.return_button_rect = pygame.Rect(button_x, screen_height // 2, button_width, button_height)
        self.quit_button_rect = pygame.Rect(button_x, screen_height // 2 + 50, button_width, button_height)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('green'), self.resume_button_rect)
        resume_text_rect = self.resume_button.get_rect(center=self.resume_button_rect.center)
        screen.blit(self.resume_button, resume_text_rect)

        pygame.draw.rect(screen, pygame.Color('blue'), self.return_button_rect)
        return_text_rect = self.return_button.get_rect(center=self.return_button_rect.center)
        screen.blit(self.return_button, return_text_rect)

        pygame.draw.rect(screen, pygame.Color('red'), self.quit_button_rect)    
        quit_text_rect = self.quit_button.get_rect(center=self.quit_button_rect.center)
        screen.blit(self.quit_button, quit_text_rect)

    def handle_click(self, pos, resume_callback, return_callback):
        for rect, action in zip([self.resume_button_rect, self.return_button_rect, self.quit_button_rect],
                                [self.resume_action, self.return_action, self.quit_action]):
            if rect.collidepoint(pos):
                action(resume_callback, return_callback)

    def resume_action(self, resume_callback, return_callback):
        self.paused = False 
        resume_callback()

    def return_action(self, resume_callback, return_callback):
        return_callback()

    def quit_action(self):
        pygame.quit()
        sys.exit()
