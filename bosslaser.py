import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_width):
        super().__init__()
        self.image = pygame.Surface((15,4))
        self.image.fill((255, 102, 102))
        self.rect = self.image.get_rect(midbottom=position)
        self.speed = speed
        self.screen_width = screen_width

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()