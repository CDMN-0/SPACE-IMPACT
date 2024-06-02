import pygame

class ScrollingBackground:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_image = pygame.image.load("Graphics/background.png").convert()  
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        self.bg_1 = 0
        self.bg_2 = screen_width

    def update(self):
        self.bg_1 -= 1
        self.bg_2 -= 1

        if self.bg_1 <= -self.screen_width:
            self.bg_1 = self.screen_width 

        if self.bg_2 <= -self.screen_width:
            self.bg_2 = self.screen_width 

    def draw(self, screen):
        screen.blit(self.background_image, (self.bg_1, 0))
        screen.blit(self.background_image, (self.bg_2, 0))
