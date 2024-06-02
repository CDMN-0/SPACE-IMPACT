import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, x, y):
        super().__init__()
        self.type = alien_type
        image_path = f"Graphics/enemy_{alien_type}.png" 
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topright=(x, y))