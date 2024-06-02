import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_type, x, y):
        super().__init__()
        self.boss_type = boss_type
        image_path = f"Graphics/boss_{boss_type}.png"  
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topright=(x, y))