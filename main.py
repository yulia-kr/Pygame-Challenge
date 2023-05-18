import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS	= pygame.time.Clock()
HEIGHT	= 800
WIDTH	= 1200
FONT = pygame.font.SysFont('Verdana', 30)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK	= (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

backgr = pygame.transform.scale(pygame.image.load('./img/background.jpg'), (WIDTH, HEIGHT))
backgr_X1 = 0
backgr_X2 = backgr.get_width()
backgr_move = 1

IMAGE_PATH = './img/goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('./img/player.png').convert_alpha()
player_rect = player.get_rect(midleft=(0, HEIGHT // 2))

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

def create_enemy():
	enemy_size = (20, 20)
	enemy = pygame.image.load('./img/enemy.png').convert_alpha()
	enemy_rect = pygame.Rect(WIDTH, random.randint(100, 700), *enemy_size)
	enemy_move = [random.randint(-4, -2), 0]
	return [enemy, enemy_rect, enemy_move]

def create_bonus():
	bonus_size = (20, 20)
	bonus = pygame.image.load('./img/bonus.png').convert_alpha()
	bonus_rect = pygame.Rect(random.randint(200, 1000), 0, *bonus_size)
	bonus_move = [0, random.randint(1, 2)]
	return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []
score	= 0

image_index = 0

playing = True

while playing:
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
            
    backgr_X1 -= backgr_move
    backgr_X2 -= backgr_move
    
    if backgr_X1 < -backgr.get_width():
        backgr_X1 = backgr.get_width()
    if backgr_X2 < -backgr.get_width():
        backgr_X2 = backgr.get_width()
        
    main_display.blit(backgr, (backgr_X1, 0))
    main_display.blit(backgr, (backgr_X2, 0))
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
        
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
        
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
        if player_rect.colliderect(enemy[1]):
            playing = False
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
        
            
    main_display.blit(FONT.render(str(score), True, COLOR_WHITE), (WIDTH - 80, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()
    
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].bottom == HEIGHT:
            bonuses.pop(bonuses.index(bonus))