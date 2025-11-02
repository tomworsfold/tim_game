import pygame

monster_data = {
    "cake1": {"health": 100, "attack_damage": 20, "roaming_speed": 2, "hunting_speed": [4,4,7,7,7], "image": pygame.image.load("images/cake1.png"), "image_scale": 1.5, "hitbox_rect": pygame.Rect(0,0,75,100), "animation_speed": 0.2, "roam_animation_speed": 0.05, "death_animation_speed": 0.12, "notice_radius": 500},
    "cake2": {"health": 100, "attack_damage": 40, "roaming_speed": 4, "hunting_speed": [4,4,6,6,6], "image": pygame.image.load("images/cake2.png"), "image_scale": 1.9, "hitbox_rect": pygame.Rect(0,0,75,90), "animation_speed": 0.1, "roam_animation_speed": 0.12, "death_animation_speed": 0.2, "notice_radius": 400},
    "cake3": {"health": 100, "attack_damage": 20, "roaming_speed": 2, "hunting_speed": [4,4,7,7,7], "image": pygame.image.load("images/cake3.png"), "image_scale": 1.5, "hitbox_rect": pygame.Rect(0,0,75,100), "animation_speed": 0.2, "roam_animation_speed": 0.05, "death_animation_speed": 0.12, "notice_radius": 500},
    "cake4": {"health": 100, "attack_damage": 40, "roaming_speed": 4, "hunting_speed": [4,4,6,6,6], "image": pygame.image.load("images/cake4.png"), "image_scale": 1.9, "hitbox_rect": pygame.Rect(0,0,75,90), "animation_speed": 0.1, "roam_animation_speed": 0.12, "death_animation_speed": 0.2, "notice_radius": 400},
    "cake5": {"health": 100, "attack_damage": 20, "roaming_speed": 2, "hunting_speed": [4,4,7,7,7], "image": pygame.image.load("images/cake5.png"), "image_scale": 1.5, "hitbox_rect": pygame.Rect(0,0,75,100), "animation_speed": 0.2, "roam_animation_speed": 0.05, "death_animation_speed": 0.12, "notice_radius": 500},
    "cake6": {"health": 100, "attack_damage": 40, "roaming_speed": 4, "hunting_speed": [4,4,6,6,6], "image": pygame.image.load("images/cake6.png"), "image_scale": 1.9, "hitbox_rect": pygame.Rect(0,0,75,90), "animation_speed": 0.1, "roam_animation_speed": 0.12, "death_animation_speed": 0.2, "notice_radius": 400},
    "cake7": {"health": 100, "attack_damage": 20, "roaming_speed": 2, "hunting_speed": [4,4,7,7,7], "image": pygame.image.load("images/cake7.png"), "image_scale": 1.5, "hitbox_rect": pygame.Rect(0,0,75,100), "animation_speed": 0.2, "roam_animation_speed": 0.05, "death_animation_speed": 0.12, "notice_radius": 500},
}

game_stats = {
    "enemies_killed_or_removed": 0,
}