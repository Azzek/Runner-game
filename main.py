import pygame
from sys import exit
from random import choice, randint

class Player(pygame.sprite.Sprite):
    
    
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.animation_index = 0
        self.player_walk = [player_walk1, player_walk2]
        self.image = self.player_walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0 
        self.player_jump = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20
    
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.animation_index += 0.1
            if self.animation_index >= len(self.player_walk): self.animation_index = 0
            self.image = self.player_walk[int(self.animation_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
    
    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): 
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animation()
        self.destroy()
        self.rect.x -= 5
            
            
def display_score():
    current_time = int((pygame.time.get_ticks() - time) / 100)
    score_surf = font.render(f"Score: {current_time}", False, (63, 64, 64))
    scrore_rect = score_surf.get_rect(midtop = (700, 50))
    screen.blit(score_surf,scrore_rect)
    return current_time 
        
        
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

font = pygame.font.Font('font/Pixeltype.ttf', 50)

time = 0
score = 0
game_active = False # if false game showing home screen
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(-1)

#Home screen stuff
title = font.render('Pixel runner', False, (111,196,169 ))
title_rect = title.get_rect(center=(400, 50))
info = font.render('Press space to start the game', False, (111,196,169))
info_rect = info.get_rect(center=(400,350))
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

#Background
albert_surf = pygame.image.load("graphics/albert.png").convert_alpha()
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
albert_rect = albert_surf.get_rect(center=(400,200))

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()



#timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1050)

#Game loop
while True:
    #Event loop
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                
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
        
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        score = display_score() # updating score
        game_active = collision_sprite()
    else:
        #show home screen
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