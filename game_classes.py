# General imports
import pygame
import sys
import os
import random
import math

# Turning the code back to images
import base64
from io import BytesIO
from PIL import Image
from image_data import *

# Function to decode the base64-encoded image
def decode_image(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    image_surface = pygame.image.load(BytesIO(decoded_image))
    return image_surface

# Use the decoded images in your script
agent_image = decode_image(agent)
barrier_image = decode_image(barrier)
bomb_exploding_image = decode_image(bomb_exploding)
bomb_image = decode_image(bomb)
bullet_image = decode_image(bullet)
cannon_image = decode_image(cannon)
enemy_image = decode_image(enemy)
heart_image = decode_image(heart)
lightning_image = decode_image(lightning)
poison_image = decode_image(poison)
shield_image = decode_image(shield)
zombie_image = decode_image(zombie)
star_image = decode_image(star)
saiyan_image = decode_image(saiyan)
gold_bullet_image = decode_image(gold_bullet)
honey_image = decode_image(honey)
firecracker_u_image = decode_image(firecracker_u)
firecracker_l_image = decode_image(firecracker_l)
firecracker_r_image = decode_image(firecracker_r)
firecracker_d_image = decode_image(firecracker_d)
firework_image = decode_image(firework)


# ---------------------------------------------------------------

# Define some sizes
character_size = 50  
bullet_size = 10
enemy_size = 50
screen_width = 800
screen_height = 800
item_size = 40

# Define character class
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = agent_image
        self.image = pygame.transform.scale(self.image, (character_size, character_size))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 4
        self.last_lightning_spawn_time = 0  # Initialize the attribute

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < screen_height - character_size:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < screen_width - character_size:
            self.rect.x += self.speed

# Define bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, character_rect, direction, game):
        super().__init__()
        self.game = game
        if not self.game.invulnerable:
            self.image = bullet_image
        else:
            self.image = gold_bullet_image 
        self.image = pygame.transform.scale(self.image, (bullet_size, bullet_size))
        self.rect = self.image.get_rect()
        self.rect.centerx = character_rect.centerx
        self.rect.centery = character_rect.centery
        self.speed = 10
        self.direction = direction

    def update(self):
        if self.direction == "left":
            if self.game.lights:
                self.image = firecracker_l_image
            self.rect.x -= self.speed
        elif self.direction == "right":
            if self.game.lights:
                self.image = firecracker_r_image
            self.rect.x += self.speed
        elif self.direction == "up":
            if self.game.lights:
                self.image = firecracker_u_image
            self.rect.y -= self.speed
        elif self.direction == "down":
            if self.game.lights:
                self.image = firecracker_d_image
            self.rect.y += self.speed

# Define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, target, game):
        super().__init__()
        self.image = enemy_image
        self.image = pygame.transform.scale(self.image, (enemy_size, enemy_size))
        self.rect = self.image.get_rect()  
        self.speed = 6
        self.target = target
        self.game = game
        self.bullet_collisions = False
        

        # Set initial position along the border
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect.centerx = random.randint(0, screen_width)
            self.rect.y = -enemy_size
        elif side == "bottom":
            self.rect.centerx = random.randint(0, screen_width)
            self.rect.y = screen_height
        elif side == "left":
            self.rect.x = -enemy_size
            self.rect.centery = random.randint(0, screen_height)
        elif side == "right":
            self.rect.x = screen_width
            self.rect.centery = random.randint(0, screen_height)

    def update(self, character, bullets, hearts, shields, scoreboard, allies, fireworks):

        if not self.game.slowed:
            self.speed = 6
        else:
            self.speed = 3

        dx_char = self.target.rect.centerx - self.rect.centerx
        dy_char = self.target.rect.centery - self.rect.centery
        dist_char = math.hypot(dx_char, dy_char)

        # Calculate distance to each ally and find the nearest one
        nearest_ally = None
        nearest_dist_ally = float('inf')

        for ally in allies:
            dx_ally = ally.rect.centerx - self.rect.centerx
            dy_ally = ally.rect.centery - self.rect.centery
            dist_ally = math.hypot(dx_ally, dy_ally)

            if dist_ally < nearest_dist_ally:
                nearest_ally = ally
                nearest_dist_ally = dist_ally

        # Choose the target based on distance
        if nearest_dist_ally < dist_char:
            dx = nearest_ally.rect.centerx - self.rect.centerx
            dy = nearest_ally.rect.centery - self.rect.centery
        else:
            dx = dx_char
            dy = dy_char

        angle = math.atan2(dy, dx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx) 

        enemy_positions = [pygame.math.Vector2(enemy.rect.center) for enemy in self.game.enemies]

        if self.game.lights:
            for bullet in bullets:
                for enemy_position in enemy_positions:
                    if enemy_position.distance_to(pygame.math.Vector2(bullet.rect.center)) <= 100:
                        firework = Firework(bullet.rect.centerx, bullet.rect.centery)
                        fireworks.add(firework)
                        self.bullet_collisions = True
                        break
        else:
        # Check for collision with bullets
            self.bullet_collisions = pygame.sprite.spritecollide(self, bullets, True)

        if self.bullet_collisions:

            self.kill()  # Remove the enemy 
            scoreboard.increment_score()  # Increment the score

            # If you are infected, it will spawn an ally at the previously killed enemy
            if self.game.infected:
                ally = Ally(self.game.last_enemy_location)
                allies.add(ally)
            
            # Update the variable with the enemy's current location
            self.game.last_enemy_location = (self.rect.x, self.rect.y)
            
        # Check for collision with the character
        player_collisions = self.target.rect.colliderect(self)
        if player_collisions:
            self.kill()  # Remove the enemy

            if not self.game.invulnerable: # Checks if the player is invulnerable
            
                if len(shields) == 0:
                    hearts.remove(hearts.sprites()[-1])  # Remove a heart    
                else:
                    shields.remove(shields.sprites()[-1])  # Remove a shield
        
        # Check for collision with allies
        ally_collisions = pygame.sprite.spritecollide(self, allies, True)
        if ally_collisions:
            self.kill()  # Remove the enemy
    
# Define scoreboard class
class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('courier new', 42, bold=True)
        self.text_width = 0
        self.text_height = 0

    def increment_score(self):
        self.score += 1

    def update_text_dimensions(self):
        score_text = self.font.render("Score: {}".format(self.score), True, (0, 0, 0))
        self.text_width, self.text_height = score_text.get_size()    

    def draw(self, screen):
        score_text = self.font.render("Score: {}".format(self.score), True, (0, 0, 0))
        x = (screen_width - self.text_width) // 2
        y = 10
        screen.blit(score_text, (x, y))


# Define the heart class
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = heart_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define the lightning class
class Lightning(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = lightning_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.active = False
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.character.speed *= 2  # Speed up the character

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.character.speed /= 2  # Restore the character's normal speed
            self.active = False  # Despawn the lightning
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the lightning
            self.kill()

# Define the cannon class
class Cannon(pygame.sprite.Sprite):
    def __init__(self, character, bullets, game):
        super().__init__()
        self.image = cannon_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.bullets = bullets
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.game = game

    def update(self):

        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.game.four_bullet = True

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.active = False  # Despawn the cannon
            self.game.four_bullet = False
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the cannon
            self.kill()

# Define the bomb class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, character, enemies):
        super().__init__()
        self.image = bomb_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.normal = bomb_image
        self.normal = pygame.transform.scale(self.normal, (item_size, item_size))
        self.exploding = bomb_exploding_image
        self.exploding = pygame.transform.scale(self.exploding, (item_size, item_size))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.enemies = enemies
        self.active = False
        self.start_time = pygame.time.get_ticks()

    def update(self):

        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.image = self.exploding
            self.active = True

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            # Kill enemies currently spawned
            for enemy in self.enemies:
                enemy.kill()

            self.image = self.normal
            self.active = False  # Despawn the bomb
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the bomb
            self.kill()

# Define ally class
class Ally(pygame.sprite.Sprite):
    def __init__(self, spawn_location):
        super().__init__()
        self.image = zombie_image
        self.image = pygame.transform.scale(self.image, (character_size, character_size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn_location
        self.speed = 1

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < screen_height - character_size:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < screen_width - character_size:
            self.rect.x += self.speed
        

class Infection(pygame.sprite.Sprite):
    def __init__(self, character, game):
        super().__init__()
        self.image = poison_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.game = game

    def update(self):

        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.game.infected = True

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.active = False  # Despawn the poison
            self.game.infected = False
            self.kill()       

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the poison
            self.kill()
           

class Barrier(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = barrier_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.shield_spacing = 50
        self.shield_start_x = 20
        self.shield_start_y = 20

    def update(self, shields):

        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True

            if len(shields) < 3:
                # Create a shield sprite and add it to the shields group
                shield = Shield(self.shield_start_x + len(shields) * self.shield_spacing, self.shield_start_y)
                shields.add(shield)

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.active = False  # Despawn the barrier
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the barrier
            self.kill()


# Define the shield class
class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = shield_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define the star class
class Star(pygame.sprite.Sprite):
    def __init__(self, character, bullets, game):
        super().__init__()
        self.image = star_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.bullets = bullets
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.game = game

    def update(self):

        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.character.image = saiyan_image # Switch to the saiyan image 
            self.character.image = pygame.transform.scale(self.character.image, (character_size, character_size))
            self.character.speed *= 2  # Speed up the character
            self.game.four_bullet = True
            self.game.invulnerable = True

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.active = False  # Despawn the cannon
            self.character.image = agent_image # Switch back to the character image 
            self.character.image = pygame.transform.scale(self.character.image, (character_size, character_size))
            self.character.speed /= 2  # Restore the character's normal speed
            self.game.four_bullet = False
            self.game.invulnerable = False
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False  # Despawn the cannon
            self.kill()

# Define the honey class
class Honey(pygame.sprite.Sprite):
    def __init__(self, character, game):
        super().__init__()
        self.image = honey_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.game = game

    def update(self):
        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.game.slowed = True  # Slows down the enemies

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.game.slowed = False  # Returns the enemies movement speed to normal
            self.active = False 
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False 
            self.kill()

# Define the firecracker class
class Firecracker(pygame.sprite.Sprite):
    def __init__(self, character, game):
        super().__init__()
        self.image = firecracker_u_image
        self.image = pygame.transform.scale(self.image, (item_size, item_size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.character = character
        self.active = False
        self.start_time = pygame.time.get_ticks()
        self.game = game

    def update(self):
        if not self.active and pygame.sprite.collide_rect(self, self.character):
            self.active = True
            self.game.lights = True

        if self.active and pygame.time.get_ticks() - self.start_time >= 5000:
            self.game.lights = False
            self.active = False 
            self.kill()

        if pygame.time.get_ticks() - self.start_time >= 7000:
            self.active = False 
            self.kill()

# Define the firework class
class Firework(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = firework_image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.start_time = pygame.time.get_ticks()
    
    def update(self):
        if pygame.time.get_ticks() - self.start_time >= 150:
            self.kill()

