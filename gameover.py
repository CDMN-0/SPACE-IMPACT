import pygame, sys
from game import Game

class GameOverScreen:
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

        self.game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))

        self.game_over_music = pygame.mixer.Sound('Audio/Super Mario World Game Over.mp3')

        self.retry_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
        self.return_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 120, 200, 50)
        self.quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 190, 200, 50)

    def draw(self, screen):
        screen.fill((29, 29, 27))
        screen.blit(self.game_over_text, self.game_over_rect)

        pygame.draw.rect(screen, pygame.Color('#00008B'), self.retry_button_rect)
        pygame.draw.rect(screen, pygame.Color('#00008B'), self.return_button_rect)
        pygame.draw.rect(screen, pygame.Color('#A42A04'), self.quit_button_rect)

        retry_text = self.font.render("Retry", True, pygame.Color('white'))
        retry_text_rect = retry_text.get_rect(center=self.retry_button_rect.center)
        screen.blit(retry_text, retry_text_rect)

        return_text = self.font.render("Return", True, pygame.Color('white'))
        return_text_rect = return_text.get_rect(center=self.return_button_rect.center)
        screen.blit(return_text, return_text_rect)

        quit_text = self.font.render("Quit", True, pygame.Color('white'))
        quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

    def play_game_over_music(self):
        self.game_over_music.play()

    def stop_game_over_music(self):
        self.game_over_music.stop()
