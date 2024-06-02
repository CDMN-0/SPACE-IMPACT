import pygame, sys

class VictoryScreen:
    def __init__(self, screen_width, screen_height, font, player_score):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.player_score = player_score

        self.victory_text = self.font.render("YOU BEAT THE GAME! THANKS FOR PLAYING!", True, pygame.Color('white'))
        self.victory_text_rect = self.victory_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))

        self.score_text = self.font.render(f"Score: {self.player_score}", True, pygame.Color('white'))
        self.score_text_rect = self.score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        self.retry_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
        self.return_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 120, 200, 50)
        self.quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 190, 200, 50)

        self.victory_music = pygame.mixer.Sound('Audio/Victory Fanfare.mp3')

    def draw(self, screen):
        self.score_text = self.font.render(f"Score: {self.player_score}", True, pygame.Color('white'))
        self.score_text_rect = self.score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        screen.fill((29, 29, 27)) 
        screen.blit(self.victory_text, self.victory_text_rect)
        screen.blit(self.score_text, self.score_text_rect)

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

    def update_player_score(self, player_score):
        self.player_score = player_score

    def play_victory_music(self):
        self.victory_music.set_volume(0.15)
        self.victory_music.play()

    def stop_victory_music(self):
        self.victory_music.stop()