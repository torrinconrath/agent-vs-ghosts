import pygame
import sys
import os
import random
import math

from game_classes import *

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("AGENT V.S. GHOSTS")

        # Define tan and brown colors
        self.tan = (210, 180, 140)
        self.brown = (61, 39, 24)

        # Define sizes
        self.square_size = 20
        self.character_size = 50  
        self.bullet_size = 10
        self.enemy_size = 50

        # Create character sprite
        self.character = Character()

        # Create a sprite groups
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Create scoreboard
        self.scoreboard = Scoreboard()
        self.scoreboard.update_text_dimensions()
        self.high_score = 0

        # Create powerup and hearts sprite groups
        self.hearts = pygame.sprite.Group()
        self.lightnings = pygame.sprite.Group()
        self.cannons = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.infections = pygame.sprite.Group() 
        self.allies = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.honeys = pygame.sprite.Group()
        self.firecrackers = pygame.sprite.Group() 
        self.fireworks = pygame.sprite.Group()

        # Initialize the flags
        self.bullet_fired = False
        self.infected = False
        self.enemy_positions = (0, 0)
        self.last_enemy_location = (0, 0)
        self.four_bullet = False
        self.invulnerable = False
        self.slowed = False
        self.lights = False
        self.game_running = True
        self.game_over = False
        self.game_start = False
        self.end_screen = False
        self.menu_screen = False

        # Clock to create a constant fps
        self.clock = pygame.time.Clock()

        # Time for enemy spawning
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 3000

        # Time speedup interval for the enemies
        self.spawn_speedup_interval = 30000
        self.spawn_speedup_percentage = 0.03

        # Power up spawn time 
        self.power_up_timer = pygame.time.get_ticks()
        self.power_up_spawn = 10000

    # A function that displays the menu
    def show_menu(self):
        
        # Create a new Pygame window for the menu screen
        menu_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("AGENT V.S. GHOSTS")

        # Fill the background with a color
        menu_screen.fill((255, 255, 255))

        # Create a font for the AGENT V.S. GHOSTS game message
        font = pygame.font.SysFont('courier new', 64, bold=True)

        # Create a font for the start message
        start_font = pygame.font.SysFont('courier new', 48, bold=True)

        # Render the AGENT V.S. GHOSTS game message
        menu_text = font.render("AGENT V.S. GHOSTS", True, (0, 0, 0))
        menu_text_rect = menu_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))

        # Render the start message
        start_text = start_font.render("Press Enter To Start", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))

        # Blit the text onto the screen
        menu_screen.blit(menu_text, menu_text_rect)
        menu_screen.blit(start_text, start_text_rect)

        # Update the display
        pygame.display.flip()
    
    # A function that updates the highscore of the running pygame
    def update_highscore(self, score):
        if self.high_score < score:
            self.high_score = score

    # A function that displays the game over window
    def show_game_over(self, score):
        # Create a new Pygame window for the game over screen
        game_over_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("AGENT V.S. GHOSTS")

        # Fill the background with a color
        game_over_screen.fill((255, 255, 255))

        # Create a font for the game over message
        font = pygame.font.SysFont('courier new', 64, bold=True)

        # Create a font for the start message
        start_font = pygame.font.SysFont('courier new', 48, bold=True)

        # Render the game over message
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))

        # Render the score message
        score_text = start_font.render("Score: {}".format(score), True, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))

        # Render the highscore message
        self.update_highscore(score)
        highscore_text = start_font.render("Highscore: {}".format(self.high_score), True, (0, 0, 0))
        highscore_text_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        # Render the start message
        start_text = start_font.render("Press Enter To Restart", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))

        # Blit the text onto the screen
        game_over_screen.blit(game_over_text, game_over_text_rect)
        game_over_screen.blit(score_text, score_text_rect)
        game_over_screen.blit(highscore_text, highscore_text_rect)
        game_over_screen.blit(start_text, start_text_rect)

        # Update the display
        pygame.display.flip()


    def start_game(self):

        while self.game_running:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle keyboard input
            if pygame.key.get_pressed()[pygame.K_RETURN]:  # Check if Enter key is pressed
                    if self.menu_screen:
                        self.menu_screen = False
                        self.game_start = True

                    elif self.game_over:
                        self.game_over = False
                        self.game_start = True
                        self.end_screen = False
                        self.reset_game()
            
            # When the game starts
            if not self.game_over and self.game_start:   
                self.update_objects(keys)
                self.draw_objects()
            
            # When before game starts
            elif not self.menu_screen and not self.game_start and not self.game_over:
                self.show_menu()
                self.menu_screen = True 
            
            # When the game ends (break happens)
            elif not self.end_screen and self.game_over and not self.game_start:
                self.show_game_over(self.scoreboard.score)
                self.end_screen = True
            
            # Ending condition
            else:
                # Handle keyboard input for when no screen
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()


    def reset_game(self):
        self.game_over = False
        self.game_start = True
        self.end_screen = False

        # Reset the game by re-initializing variables and objects
        self.character = Character()
        self.bullets.empty()
        self.enemies.empty()
        self.scoreboard.score = 0
        self.scoreboard.update_text_dimensions()
        self.spawn_timer = pygame.time.get_ticks()
        pygame.display.set_caption("AGENT V.S. GHOSTS")

        # Clear the hearts group before adding new hearts
        self.hearts.empty()

        # Create hearts
        heart_spacing = 50
        heart_start_x = (self.screen_width - 60)
        heart_start_y = 20
        for i in range(3):
            heart = Heart(heart_start_x - i * heart_spacing, heart_start_y)
            self.hearts.add(heart)

        # Reset powerups
        self.lightnings.empty()
        self.cannons.empty()
        self.bombs.empty()
        self.infections.empty()
        self.allies.empty()
        self.barriers.empty()
        self.shields.empty()
        self.stars.empty()
        self.honeys.empty()
        self.firecrackers.empty()
        self.fireworks.empty()

        # Time for enemy spawning
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 3000  # 3000 milliseconds = 3 seconds

        # Time speedup interval for the enemies
        self.spawn_speedup_interval = 30000  # 30000 milliseconds = 30 seconds
        self.spawn_speedup_percentage = 0.03  # 3% faster spawn rate

        # Power up spawn time 
        self.power_up_timer = pygame.time.get_ticks()
        self.power_up_spawn = 10000  # 10000 milliseconds = 10 seconds

    def shooting_logic(self, keys):

        # Shooting logic
        if keys[pygame.K_UP] and not self.bullet_fired and not self.four_bullet:
            bullet = Bullet(self.character.rect, "up", self)
            self.bullets.add(bullet)
            self.bullet_fired = True
        if keys[pygame.K_DOWN] and not self.bullet_fired and not self.four_bullet:
            bullet = Bullet(self.character.rect, "down", self)
            self.bullets.add(bullet)
            self.bullet_fired = True
        if keys[pygame.K_LEFT] and not self.bullet_fired and not self.four_bullet:
            bullet = Bullet(self.character.rect, "left", self)
            self.bullets.add(bullet)
            self.bullet_fired = True
        if keys[pygame.K_RIGHT] and not self.bullet_fired and not self.four_bullet:
            bullet = Bullet(self.character.rect, "right", self)
            self.bullets.add(bullet)
            self.bullet_fired = True
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if self.four_bullet and not self.bullet_fired:
                bullet_up = Bullet(self.character.rect, "up", self)
                self.bullets.add(bullet_up)
                bullet_down = Bullet(self.character.rect, "down", self)
                self.bullets.add(bullet_down)
                bullet_left = Bullet(self.character.rect, "left", self)
                self.bullets.add(bullet_left)
                bullet_right = Bullet(self.character.rect, "right", self)
                self.bullets.add(bullet_right)
                self.bullet_fired = True

        # Reset bullet_fired flag if no shooting key is held down
        if not any(keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
            self.bullet_fired = False 

    def update_objects(self, keys):

        self.character.update(keys)

        # Update bullets
        self.shooting_logic(keys)
        self.bullets.update()

        # Update enemies given the spawn timer
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer >= self.spawn_delay:
            enemy = Enemy(self.character, self)
            self.enemies.add(enemy)
            self.spawn_timer = current_time

            # Speed up enemy spawn rate every 3 seconds
            if (current_time - self.spawn_timer) % self.spawn_speedup_interval == 0:
                self.spawn_delay *= (1 - self.spawn_speedup_percentage)

        self.enemies.update(self.character, self.bullets, self.hearts, self.shields, self.scoreboard, self.allies, self.fireworks)

        powerup_index = random.randint(1, 8)
        # Update the powerups given the spawn timer
        if current_time - self.power_up_timer >= self.power_up_spawn:
            
            if powerup_index == 1:
                lightning = Lightning(self.character)
                self.lightnings.add(lightning)
                self.power_up_timer = current_time

            if powerup_index == 2:
                cannon = Cannon(self.character, self.bullets, self)
                self.cannons.add(cannon)
                self.power_up_timer = current_time
            
            if powerup_index == 3:
                bomb = Bomb(self.character, self.enemies)
                self.bombs.add(bomb)
                self.power_up_timer = current_time
            
            if powerup_index == 4: 
                infection = Infection(self.character, self)
                self.infections.add(infection)
                self.power_up_timer = current_time
            
            if powerup_index == 5 and len(self.shields) < 3: 
                barrier = Barrier(self.character)
                self.barriers.add(barrier)
                self.power_up_timer = current_time
            
            if powerup_index == 6:
                star = Star(self.character, self.bullets, self)
                self.stars.add(star)
                self.power_up_timer = current_time
            
            if powerup_index == 7:
                honey = Honey(self.character, self)
                self.honeys.add(honey)
                self.power_up_timer = current_time

            if powerup_index == 8:
                firecracker = Firecracker(self.character, self)
                self.firecrackers.add(firecracker)
                self.power_up_timer = current_time

        # Update the powerups
        self.lightnings.update()
        self.cannons.update()
        self.bombs.update()
        self.infections.update()
        self.allies.update(keys)
        self.barriers.update(self.shields)
        self.shields.update()
        self.stars.update()
        self.honeys.update()
        self.firecrackers.update()
        self.fireworks.update()

        # Game over condition
        if len(self.hearts) == 0:
            self.game_over = True
            self.game_start = False
            self.show_game_over(self.scoreboard.score)


    def draw_objects(self):

        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Draw the checkered background
        for row in range(self.screen_height // self.square_size):
            for col in range(self.screen_width // self.square_size):
                if (row + col) % 2 == 0:
                    color = self.tan
                else:
                    color = self.brown

                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, 
                self.square_size, self.square_size))

        # Draw the objects
        self.screen.blit(self.character.image, self.character.rect)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.hearts.draw(self.screen)
        self.lightnings.draw(self.screen)
        self.cannons.draw(self.screen)
        self.bombs.draw(self.screen)
        self.infections.draw(self.screen)
        self.allies.draw(self.screen)
        self.barriers.draw(self.screen)
        self.shields.draw(self.screen)
        self.stars.draw(self.screen)
        self.honeys.draw(self.screen)
        self.firecrackers.draw(self.screen)
        self.fireworks.draw(self.screen)

        # Flip the display
        pygame.display.flip()

# Main function to run the game
def main():
    game = Game()
    game.start_game()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
