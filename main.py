import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() - time) / 100)
    score_surf = font.render(f"Score: {current_time}", False, (63, 64, 64))
    scrore_rect = score_surf.get_rect(midtop = (700, 50))
    screen.blit(score_surf,scrore_rect)
    return current_time


def collisions(player,obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):return False
    return True


def obstacles_move(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 290: screen.blit(snail_surf, obstacle_rect)

            else: screen.blit(fly_surf, obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return []
    
    
def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
        
        
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf', 50)

#menu text
title = font.render('Pixel runner', False, (111,196,169 ))
title_rect = title.get_rect(center=(400, 50))
info = font.render('Press space to start the game', False, (111,196,169))
info_rect = info.get_rect(center=(400,350))

#Background
albert_surf = pygame.image.load("graphics/albert.png").convert_alpha()
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
albert_rect = albert_surf.get_rect(center=(400,200))

#Player 
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_index = 0
player_walk = [player_walk1, player_walk2]
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 1
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

#obstacles 
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_index = 0
fly_frames = [fly_frame1, fly_frame2]
fly_surf = fly_frames[fly_index]

obstacles_rect_list = []

#timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1050)
        
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,600)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

#score
time = 0
score = 0

game_active = False # if false game showing home screen
#Game loop
while True:
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #Jumping by clicking on player
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos):
                player_gravity = -34
            
            #Jumping on space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacles_rect_list.append(fly_surf.get_rect(midbottom=(randint(950,1000),300)).inflate(-30,-20))
                else:
                    obstacles_rect_list.append(snail_surf.get_rect(midbottom=(randint(950,1000),200)).inflate(-30,-20))
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly_frames[fly_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                time = pygame.time.get_ticks()
                
    
    if game_active:
        if score > 20:
            screen.blit(sky_surf, (0,0)) 
            screen.blit(albert_surf, albert_rect)
        else:
            screen.blit(sky_surf, (0,0)) 
        screen.blit(ground_surf, (0,300))
        
        #Player BEHAVIOR
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        player_animation()
        
        #obstacjes movement
        obstacles_rect_list = obstacles_move(obstacles_rect_list)
        
        game_active = collisions(player_rect, obstacles_rect_list) # if player collides with something end game :)
        score = display_score() # updating score
    else:
        #show home screen
        obstacles_rect_list.clear()
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title, title_rect)
        if score == 0:
            screen.blit(info, info_rect)
        else:
            score_message = font.render(f"Last score: {score}", False, (111,196,169))
            score_mesage_rect = score_message.get_rect(center=(400,350))
            screen.blit(score_message, score_mesage_rect)

    pygame.display.update()
    clock.tick(60)