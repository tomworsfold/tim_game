# Example file showing a circle moving on screen
import pygame
import math
import numpy.random as random

from settings import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Tim's Birthday Brawl")
clock = pygame.time.Clock()
running = True
dt = 0

class Player(pygame.sprite.Sprite):
    pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    def __init__(self):
        super().__init__(all_sprites_group)
        self.image = pygame.transform.scale((pygame.image.load("images/player.png").convert_alpha()), (120, 120))
        self.base_player_image = self.image
        self.hitbox_rect = self.image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = 5
        self.health = 100
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            # Handle player death here (e.g., game over)

    def player_rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()

        #calculate angle
        x_dist = self.mouse_pos[0] - self.hitbox_rect.centerx
        y_dist = -(self.mouse_pos[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.base_player_image, self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed

        #handle moving diagonally
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 7
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 5  # place bar just above the sprite

        # Calculate health ratio (assuming max health is 100)
        ratio = max(self.health, 0) / 100

        # Draw background (full health) in red
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Draw foreground (remaining health) in green proportional to current health
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * ratio, bar_height))

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        collided_enemies = pygame.sprite.spritecollide(player, enemy_group, False)
        for enemy in collided_enemies:
            player.take_damage(2)
            # Optionally add invincibility frames to avoid multiple damage per frame

class Sparkler(pygame.sprite.Sprite):
    pos = ((0,0))
    def __init__(self, player):
        super().__init__(all_sprites_group)
        self.player = player
        self.pos = player.pos
        self.image = pygame.transform.scale(pygame.image.load("images/sparks.png").convert_alpha(), (300, 50))
        self.base_image = self.image
        self.hitbox_rect = self.image.get_rect(center = player.pos)
        self.rect = self.hitbox_rect.copy()
        self.active = False
        self.offset = pygame.math.Vector2(150, 30)  # Adjust based on your sprite size
        self.sparkler_length = 100  # max fuel
        self.fuel = self.sparkler_length
        self.recharge = False
        self.empty_penalty = False

    def update(self):
        self.active = pygame.mouse.get_pressed()[0]

        # Rotate offset vector by player's angle
        rotated_offset = self.offset.rotate(-self.player.angle)

        # Calculate new position for sparkler
        sparkler_pos = self.player.pos + rotated_offset

        # Rotate sparkler image by player's angle
        rotated_image = pygame.transform.rotate(self.base_image, self.player.angle+180)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=sparkler_pos)


        if not self.recharge:
            if self.active and not self.empty_penalty:
                if self.fuel > 0:
                    self.fuel -= 0.6
                    self.image.set_alpha(255)
                else:
                    # Fuel hit zero, start penalty cooldown
                    self.empty_penalty = True
                    self.recharge = True
                    self.image.set_alpha(0)
            else:
                self.image.set_alpha(0)
                self.fuel += 0.1
                if self.fuel > 100:
                    self.fuel = 100
        else:
            self.image.set_alpha(0)
            # Slow recharge during penalty
            recharge_rate = 0.8 if self.empty_penalty else 0.25
            self.fuel += recharge_rate
            if self.fuel >= 100:
                self.recharge = False
                if self.empty_penalty:
                    self.empty_penalty = False


        # Detect enemies colliding with sparkler rect while it is active
        if sparkler.active and sparkler.fuel > 0 and not sparkler.recharge and not sparkler.empty_penalty:
            collided_enemies = pygame.sprite.spritecollide(sparkler, enemy_group, False)
            for enemy in collided_enemies:
                enemy.take_damage(2)  # Adjust damage value as desired

class Enemy(pygame.sprite.Sprite): 

    def __init__(self, name, position):
        super().__init__(enemy_group, all_sprites_group)
        self.alive = True
        self.name = name

        enemy_info = monster_data[self.name]
        self.health = enemy_info["health"]
        self.image_scale = enemy_info["image_scale"]
        self.image = enemy_info["image"].convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.image_scale)



        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = 3

        self.position = pygame.math.Vector2(position)
        
        self.hitbox_rect = enemy_info["hitbox_rect"]
        self.base_zombie_rect = self.hitbox_rect.copy()
        self.base_zombie_rect.center = self.rect.center
             

        self.collide = False

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove enemy sprite when health <= 0
            global enemies_killed
            enemies_killed += 1

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()
    
    def update(self):
        self.hunt_player()

    def draw_health_bar(self, surface):
        # Health bar dimensions and position above sprite
        bar_width = self.rect.width
        bar_height = 7
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 5  # 5 pixels above sprite

        # Calculate health ratio
        ratio = max(self.health, 0) / 100  # assuming max health is 100

        # Background bar (red)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Foreground bar (green) proportional to current health
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * ratio, bar_height))
def draw_fuel_bar(surf, x, y, w, h, fuel, max_fuel):
    # Draw background bar (gray)
    pygame.draw.rect(surf, (50, 50, 50), (x, y, w, h))
    
    # Calculate fuel percentage
    fuel_ratio = max(0, fuel) / max_fuel
    
    # Draw fuel bar foreground (orange)
    pygame.draw.rect(surf, (255, 165, 0), (x, y, w * fuel_ratio, h))
    
    # Optional: draw border
    pygame.draw.rect(surf, (255, 255, 255), (x, y, w, h), 2)
def restart_game():
    global player, game_over, enemies_killed
    enemies_killed = 0
    player.health = 100
    player.rect.center = (400, 300)
    for enemy in enemy_group.sprites():
        enemy_group.empty()
        all_sprites_group.remove(enemy)
        enemy.kill()
    game_over = False


all_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()  

player = Player()
sparkler = Sparkler(player)
cake = Enemy(name="cake7",position= (400,400))
spawn_timer = 0
enemy_names = ["cake1", "cake2", "cake3", "cake4", "cake5", "cake6", "cake7"]
game_over = False
enemies_killed = 0  # Track kills
show_end_screen = False
flash_interval = 500  # milliseconds
last_flash_time = 0
show_text = True
font = pygame.font.Font(None, 100)  # Font for end message

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press R to restart
                restart_game()
        if show_end_screen and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Restart from end screen as well
                restart_game()
    if player.health <= 0:
        game_over = True

    # Show end screen on 10 kills
    if enemies_killed >= 10:
        show_end_screen = True

    if game_over:
        # Draw "Game Over" screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
    elif show_end_screen:
        # Flashing logic
        if current_time - last_flash_time > flash_interval:
            show_text = not show_text
            last_flash_time = current_time

        screen.fill((0, 0, 0))
        if show_text:
            text_surface = font.render("HAPPY BIRTHDAY TIM", True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()
    else:
        spawn_timer += dt
        if spawn_timer > 2:  # spawn an enemy every 3 seconds (example)
            spawn_timer = 0
            spawn_x = random.randint(0, screen.get_width())
            spawn_y = random.randint(0, screen.get_height())
            chosen_enemy = random.choice(enemy_names)
            Enemy(name=chosen_enemy, position=(spawn_x, spawn_y))

        screen.fill("pink")
        enemies_text = pygame.font.Font(None, 74).render(f"Kill {10 - int(enemies_killed)} left to WIN", True, (255, 0, 0))
        text_rect = enemies_text.get_rect(center=(250,75))

        screen.blit(enemies_text, text_rect)
        all_sprites_group.draw(screen)
        player.draw_health_bar(screen)
        for enemy in enemy_group:
            enemy.draw_health_bar(screen)
        all_sprites_group.update()

        bar_width = 200
        bar_height = 20
        margin = 10
        x_pos = screen.get_width() - bar_width - margin
        y_pos = screen.get_height() - bar_height - margin

        draw_fuel_bar(screen, x_pos, y_pos, bar_width, bar_height, sparkler.fuel, sparkler.sparkler_length)



        pygame.display.flip()  

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()