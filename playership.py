import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/player.png")
        self.rect = self.image.get_rect(midleft=(0, self.screen_height / 2))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 350
        self.laser_sound = pygame.mixer.Sound("Audio/laser.mp3")
        self.laser_sound.set_volume(0.10)

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, -5, self.screen_width)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True
