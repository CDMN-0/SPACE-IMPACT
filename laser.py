import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_width):
        super().__init__()
        self.image = pygame.Surface((15,4))
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.screen_width = screen_width

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x > self.screen_width + 15 or self.rect.x < 0:
            self.kill()
