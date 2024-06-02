import pygame, sys
from random import randint
from playership import Spaceship
from alien import Alien
from boss import Boss
from bosslaser import Laser
from pause import PauseMenu
from menu import MainMenu
from victory import VictoryScreen
from background import ScrollingBackground

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_active = True
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.aliens_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.boss_lasers_group = pygame.sprite.Group()
        self.background = ScrollingBackground(self.screen_width, self.screen_height)
        self.game_music = pygame.mixer.Sound('Audio/Loops/mp3/Sci-Fi 8 Loop.mp3')

        self.spaceship = Spaceship(self.screen_width, self.screen_height)
        self.spaceship_group.add(self.spaceship)
        self.alien_kill_points = 100  
        self.laser_kill_points = 500
        self.boss_kill_points = 1000
        self.alien_crash_reduction = 50
        self.boss_hit_reduction = 250

        self.current_stage = 1
        self.max_player_health = 3
        self.player_health = self.max_player_health
        self.player_score = 0
        self.full_heart_image = pygame.image.load("Graphics/UI Package/Status/1-4.png").convert_alpha()
        self.empty_heart_image = pygame.image.load("Graphics/UI Package/Status/1-3.png").convert_alpha()
        self.pixel_font = pygame.font.Font('Fonts/Retro.ttf', 16)

        self.last_spawn_time = pygame.time.get_ticks() 
        self.spawn_delay = 2000 
        self.max_alien_count = 5  

        self.create_aliens(stage=1)
        self.zigzag_direction = 1
        self.zigzag_counter = 0

        self.aliens_destroyed = 0  
        self.boss_spawned = False 
        self.max_boss_health = 10
        self.boss_health = self.max_boss_health
        
        self.HUD_FONT_SIZE = 24
        self.HUD_COLOR = (255, 255, 255)  
        self.HUD_MARGIN = 10
        self.HEART_SIZE = (32, 32)
        self.STAGE_POSITION = (self.screen_width - self.HUD_MARGIN, self.screen_height - self.HUD_MARGIN)
        self.SCORE_POSITION = (self.screen_width - self.HUD_MARGIN, self.HUD_MARGIN + 25)
        self.BOSS_HEALTH_BAR_POSITION = (self.screen_width - 1120, self.HUD_MARGIN)
        self.BOSS_HEALTH_BAR_WIDTH = 200
        self.BOSS_HEALTH_BAR_HEIGHT = 20
        self.BOSS_HEALTH_BAR_COLOR = (255, 0, 0)

    def play_game_music(self):
        self.game_music.set_volume(0.3)
        self.game_music.play(loops=-1)

    def stop_game_music(self):
        self.game_music.stop()

    def render_hud(self, screen):
        if self.game_active:
            for i in range(self.max_player_health):  
                heart_x = self.HUD_MARGIN + i * (self.HEART_SIZE[0] + self.HUD_MARGIN)
                heart_y = self.screen_height - self.HUD_MARGIN - 18
                heart_rect = pygame.Rect(heart_x, heart_y, *self.HEART_SIZE)
                heart_surface = self.full_heart_image 
                
                if i >= self.player_health:  
                    heart_surface = self.empty_heart_image

                screen.blit(heart_surface, heart_rect)

            self.background.update()
            stage_text = f"Stage: {self.current_stage}"
            stage_surface = self.pixel_font.render(stage_text, True, self.HUD_COLOR)
            stage_rect = stage_surface.get_rect(bottomright=self.STAGE_POSITION) 
            screen.blit(stage_surface, stage_rect)

            score_text = f"Score: {self.player_score}"
            score_surface = self.pixel_font.render(score_text, True, self.HUD_COLOR)
            score_rect = score_surface.get_rect(bottomright=self.SCORE_POSITION) 
            screen.blit(score_surface, score_rect)

            if self.boss_spawned and self.boss_health > 0:
                boss_health_text = f"BOSS HEALTH: "
                boss_health_surface = self.pixel_font.render(boss_health_text, True, self.HUD_COLOR)
                boss_health_rect = boss_health_surface.get_rect(topleft=(self.HUD_MARGIN, self.HUD_MARGIN)) 
                screen.blit(boss_health_surface, boss_health_rect)

                boss_health_percentage = self.boss_health / self.max_boss_health 
                boss_health_bar_width = int(self.BOSS_HEALTH_BAR_WIDTH * boss_health_percentage)
                boss_health_bar_rect = pygame.Rect(self.BOSS_HEALTH_BAR_POSITION[0], self.BOSS_HEALTH_BAR_POSITION[1], boss_health_bar_width, self.BOSS_HEALTH_BAR_HEIGHT)
                pygame.draw.rect(screen, self.BOSS_HEALTH_BAR_COLOR, boss_health_bar_rect)
        
    def update(self):
        if self.game_active:
            self.background.update()
            self.update_aliens()  
            self.spawn_aliens() 
            if self.player_health <= 0:
                self.game_over = True
                self.game_active = False

    def create_aliens(self, stage = None):
        if self.game_active:
            if stage is None:
                stage = self.current_stage

            if stage == 1:
                for _ in range(3):
                    alien_type = randint(1, 3)
                    self.spawn_aliens(alien_type)
            elif stage == 2:
                for _ in range(3): 
                    alien_type = randint(4, 6)
                    self.spawn_aliens(alien_type)           
            elif stage == 3:
                for _ in range(3):
                    alien_type = randint(7, 9)
                    self.spawn_aliens(alien_type)    
            elif stage == 4:
                for _ in range(3): 
                    alien_type = randint(10, 12)
                    self.spawn_aliens(alien_type) 

    def spawn_aliens(self, alien_type):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.spawn_delay and len(self.aliens_group) < self.max_alien_count and not self.boss_spawned:
            print(f"Spawning alien of type {alien_type}...")
            y = randint(0, self.screen_height - 50) 
            x = self.screen_width + 150
            alien = Alien(alien_type, x, y)
            self.aliens_group.add(alien)
            print("Alien spawned.")
            self.last_spawn_time = current_time

    def aliens_needed_to_spawn(self):
        if self.current_stage == 1:
            return 5
            # return 10
        elif self.current_stage == 2:
            return 5
            # return 15
        elif self.current_stage == 3:
            return 5
            # return 20
        else:
            return 5
            # return 25
        
    def update_aliens(self):
        self.zigzag_counter += 1

        for alien in self.aliens_group:
            alien.rect.x -= 2

            if alien.rect.right <= 0:
                alien.kill()
                self.aliens_destroyed += 1

        if self.zigzag_counter >= 250:  
            self.zigzag_direction *= -1
            self.zigzag_counter = 0

        for alien in self.aliens_group:
            if not isinstance(alien, Boss):
                alien.rect.y += self.zigzag_direction * 1  
                alien.rect.y = max(0, min(alien.rect.y, self.screen_height - alien.rect.height))

        if not self.boss_spawned:
            if self.aliens_destroyed >= self.aliens_needed_to_spawn():
                self.spawn_boss(self.current_stage)

        for boss in self.boss_group.sprites():
            if isinstance(boss, Boss) and self.boss_spawned:
                if boss.rect.right > self.screen_width:
                    boss.rect.x -= 5
                else:
                    boss.rect.y += self.zigzag_direction * 1
                    boss.rect.y = max(0, min(boss.rect.y, self.screen_height - boss.rect.height))
                    
                    boss.rect.x = max(0, min(boss.rect.x, self.screen_width - boss.rect.width))

                if self.current_stage == 1:
                    if randint(1, 75) == 1:
                        boss_center = (boss.rect.centerx, boss.rect.centery)
                        boss_laser = Laser((boss_center[0] - 10, boss_center[1]), 5, self.screen_width)  
                        self.boss_lasers_group.add(boss_laser)  
                elif self.current_stage == 2:
                    if randint(1, 60) == 1:
                        boss_center = (boss.rect.centerx, boss.rect.centery)
                        boss_laser1 = Laser((boss_center[0] - 125, boss_center[1] + 10), 5, self.screen_width)  
                        boss_laser2 = Laser((boss_center[0] - 125, boss_center[1] - 10), 5, self.screen_width) 
                        self.boss_lasers_group.add(boss_laser1, boss_laser2) 
                elif self.current_stage == 3:
                    if randint(1, 30) == 1:
                        boss_center = (boss.rect.centerx, boss.rect.centery)
                        boss_laser1 = Laser((boss_center[0] - 150, boss_center[1] + 3), 5, self.screen_width)  
                        boss_laser2 = Laser((boss_center[0] - 150, boss_center[1] - 3), 5, self.screen_width) 
                        boss_laser3 = Laser((boss_center[0] - 150, boss_center[1]), 5, self.screen_width) 
                        boss_laser4 = Laser((boss_center[0] - 150, boss_center[1] - 6), 5, self.screen_width) 
                        boss_laser5 = Laser((boss_center[0] - 150, boss_center[1] + 6), 5, self.screen_width) 
                        boss_laser6 = Laser((boss_center[0] - 150, boss_center[1] - 9), 5, self.screen_width) 
                        boss_laser7 = Laser((boss_center[0] - 150, boss_center[1] + 9), 5, self.screen_width) 
                        self.boss_lasers_group.add(boss_laser1, boss_laser2, boss_laser3, boss_laser4, boss_laser5, boss_laser6, boss_laser7) 
                elif self.current_stage == 4:
                    if randint(1, 30) == 1:
                        self.aliens_group.empty()
                        boss_center = (boss.rect.centerx, boss.rect.centery)
                        boss_laser1 = Laser((boss_center[0] - 100, boss_center[1] + 50), 5, self.screen_width)  
                        boss_laser2 = Laser((boss_center[0] - 100, boss_center[1] - 50), 5, self.screen_width) 
                        boss_laser3 = Laser((boss_center[0] - 50, boss_center[1] + 95), 5, self.screen_width) 
                        boss_laser4 = Laser((boss_center[0] - 50, boss_center[1] - 95), 5, self.screen_width) 
                        boss_laser5 = Laser((boss_center[0] - 12, boss_center[1] + 116), 5, self.screen_width) 
                        boss_laser6 = Laser((boss_center[0] - 12, boss_center[1] - 116), 5, self.screen_width) 
                        boss_laser7 = Laser((boss_center[0] + 40, boss_center[1] + 135), 5, self.screen_width) 
                        boss_laser8 = Laser((boss_center[0] + 40, boss_center[1] - 135), 5, self.screen_width) 
                        
                        self.boss_lasers_group.add(boss_laser1, boss_laser2, boss_laser3, boss_laser4, boss_laser5, boss_laser6, boss_laser7, boss_laser8)  
                
    def spawn_boss(self, boss_type):
        self.aliens_destroyed = 0
        x = self.screen_width + 400  
        y = (self.screen_height - 427) // 2 
        boss = Boss(boss_type, x, y)
        self.boss_group.add(boss)
        self.boss_spawned = True

    def draw_boss(self, screen):
        for boss in self.boss_group:
            if isinstance(boss, Boss) and self.boss_spawned:
                screen.blit(boss.image, boss.rect)

    def check_for_collisions(self):
        if self.game_active:
            if self.spaceship_group.sprite:
                if self.spaceship_group.sprite.lasers_group:
                    for laser_sprite in self.spaceship_group.sprite.lasers_group:
                        regular_alien_collisions = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                        for alien_hit in regular_alien_collisions:
                            laser_sprite.kill()
                            self.player_score += self.alien_kill_points
                            self.aliens_destroyed += 1 

                        if self.boss_group:
                            boss_collisions = pygame.sprite.spritecollide(laser_sprite, self.boss_group, False)  
                            for boss_hit in boss_collisions:
                                if isinstance(boss_hit, Boss):  
                                    self.reduce_boss_health()
                                laser_sprite.kill()

                        boss_laser_collisions = pygame.sprite.spritecollide(laser_sprite, self.boss_lasers_group, True)
                        for boss_laser_hit in boss_laser_collisions:
                            self.player_score += self.laser_kill_points
                            laser_sprite.kill()

            if self.boss_lasers_group and self.spaceship_group.sprite:
                player_collisions = pygame.sprite.spritecollide(self.spaceship_group.sprite, self.boss_lasers_group, True)
                for player_hit in player_collisions:
                    self.player_score -= self.boss_hit_reduction
                    self.reduce_player_health()

            if self.spaceship_group.sprite:
                player_alien_collisions = pygame.sprite.spritecollide(self.spaceship_group.sprite, self.aliens_group, True)
                for alien_hit in player_alien_collisions:
                    self.player_score -= self.alien_crash_reduction
                    self.reduce_player_health()
        else:
            self.spaceship_group.empty()
            self.aliens_group.empty()
            self.boss_group.empty()
            self.boss_lasers_group.empty()
        
    def reduce_boss_health(self):
        self.boss_health -= 1
        print("Boss health:", self.boss_health)
        if self.boss_health <= 0 and self.boss_spawned:
            self.boss_spawned = False 
            for boss in self.boss_group:
                if isinstance(boss, Boss):
                    boss.kill()
            self.player_score += self.boss_kill_points
            self.current_stage += 1
            print("BOSS STAGE CHECK", self.current_stage)
            self.player_health = 3
            self.aliens_destroyed = 0
            self.boss_spawned = False
            self.max_boss_health += 5
            # self.max_boss_health += 10
            self.boss_health = self.max_boss_health

    def reduce_player_health(self):
        self.player_health -= 1
        print("Player HP: ", self.player_health)
        if self.player_health <= 0:
            self.game_active = False
            self.aliens_group.empty()
            self.boss_group.empty()
            self.boss_lasers_group.empty()
            self.clear_player_ship()
            print("YOU LOSE!") 
            self.player_health = 0     

    def check_for_victory(self):
        if self.current_stage == 5 and len(self.boss_group) == 0:
            self.game_active = False
            self.aliens_group.empty()
            self.boss_group.empty()
            self.boss_lasers_group.empty()
            self.clear_player_ship()
            return True
        return False
    
    def clear_player_ship(self):
        self.spaceship_group.remove(self.spaceship)

    def draw_victory_overlay(self, screen):
        self.victory_screen.draw(screen)

    def victory_loop(self, screen):
        self.victory_screen.handle_events()

    def reset_game(self):
        self.current_stage = 1
        self.player_health = self.max_player_health
        self.player_score = 0
        self.aliens_destroyed = 0
        self.boss_spawned = False
        self.boss_health = self.max_boss_health

        self.spaceship = Spaceship(self.screen_width, self.screen_height)
        self.spaceship_group.empty()  
        self.spaceship_group.add(self.spaceship)

        self.aliens_group.empty()
        self.boss_group.empty()
        self.boss_lasers_group.empty()

        self.create_aliens()