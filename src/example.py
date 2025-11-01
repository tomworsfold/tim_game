# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Tim's Birthday Brawl")
clock = pygame.time.Clock()
running = True
dt = 0

player_img = pygame.image.load("../images/player.png").convert_alpha()
player = pygame.transform.scale(player_img, (75, 75))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    
    screen.blit(player, player_pos)

    hitbox = pygame.Rect(player_pos[0]+25, player_pos[1], player.get_width() - 50, player.get_height())

    target = pygame.Rect(400, 0, 160, 280)
    collision = hitbox.colliderect(target)
    pygame.draw.rect(screen, (255 *collision, 255, 0), target)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()