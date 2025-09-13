import pygame,random

pygame.init()

ww = 800
wh = 600
display_surface = pygame.display.set_mode((ww,wh))
pygame.display.set_caption("Burger Dog")

#fps and clock
fps = 60
Clock = pygame.time.Clock()

#game values
player_starting_lives = 3
player_normal_velocity = 5
player_boost = 10
starting_boost_level = 100
starting_burger_velocity = 3
burger_acc = .5

buffer_dist = 100
score = 0
burger_points = 0
burger_eaten = 0

player_lives = player_starting_lives
player_velocity = player_normal_velocity

boost_level = starting_boost_level
burger_velocity = starting_burger_velocity

#color
orange = (246,170,54)
black =(0,0,0)
white = (255,255,255)

#fonts
font = pygame.font.Font("wash.ttf",32)

#set text
points_text = font.render("Burger Points : "+str(burger_points),True,orange)
points_rect = points_text.get_rect()
points_rect.topleft = (10,10)

score_text = font.render("Score : "+ str(score),True,orange)
score_rect = score_text.get_rect(topleft= (10,50))

title_text = font.render(" Burger Dog ",True,black,orange)
title_rect = title_text.get_rect()
title_rect.centerx = ww//2
title_rect.y = 10

eaten_text = font.render("Burgers Eaten : "+str(burger_eaten),True,orange)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = ww//2
eaten_rect.y = 50

lives_text = font.render("Lives : "+str(player_lives),True,orange)
lives_rect = lives_text.get_rect()
lives_rect.topright = (ww - 20, 10)

boost_text = font.render("Boost : "+str(boost_level),True,orange)
boost_rect = boost_text.get_rect()
boost_rect.topright = (ww -10,50)

game_over_text = font.render("Final Score : "+str(score), True,orange)
game_over_rect = game_over_text.get_rect(center=(ww // 2, wh // 2))

continue_text = font.render("Press any key to play again", True, orange)
continue_rect = continue_text.get_rect(center=(ww // 2, wh // 2 + 64))

#set music
#bark_sound = pygame.mixer.Sound("bark.wav")
#miss_sound = pygame.mixer.Sound("sound.wav")
#pygame.mixer.music.load("sound1.wav")
#pygame.mixer.music.play(-1,0.0)
#set image
player_imgleft = pygame.image.load("dogr.png")
player_imgright = pygame.image.load("dogl.png")

player_img = player_imgleft
player_rect = player_img.get_rect()
player_rect.centerx = ww//2
player_rect.bottom = wh

burger_img = pygame.image.load("burger.png")
burger_rect = burger_img.get_rect()
burger_rect.topleft = (random.randint(0,ww-32),-buffer_dist)

#game loop
running = True
while running :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    #move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0 :
        player_rect.x -= player_velocity
        player_img = player_imgleft
    if keys[pygame.K_RIGHT] and player_rect.right < ww :
        player_rect.x += player_velocity
        player_img = player_imgright
    if keys[pygame.K_UP] and player_rect.top > 100 :
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < wh :
        player_rect.y += player_velocity
    
    #boost
    if keys[pygame.K_SPACE] and boost_level > 0 :
        player_velocity = player_boost
        boost_level -= 1
    else :
        player_velocity = player_normal_velocity

    #move the burger and update
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity*(wh - burger_rect.y))

    #player missed the burger
    if burger_rect.y > wh :
        player_lives -= 1
        #miss_sound.play()
        
        burger_rect.topleft = (random.randint(0,ww-32),-buffer_dist)
        burger_velocity = starting_burger_velocity
        
        player_rect.centerx = ww//2
        player_rect.bottom = wh
        
        boost_level = starting_boost_level
    
    #check for collision
    if player_rect.colliderect(burger_rect) :
        burger_eaten += 1
        score += burger_points
        #bark_sound.play()
        
        burger_rect.topleft = (random.randint(0,ww-32),-buffer_dist)
        burger_velocity += burger_acc

        boost_level += 25
        if boost_level>starting_boost_level:
            boost_level = starting_boost_level
    #update hud
    points_text = font.render("Burger Points : "+str(burger_points),True,orange)
    score_text = font.render("Score : "+ str(score),True,orange)
    eaten_text = font.render("Burgers Eaten : "+str(burger_eaten),True,orange)
    lives_text = font.render("Lives : "+str(player_lives),True,orange)
    boost_text = font.render("Boost : "+str(boost_level),True,orange)

    #check the game over
    if player_lives == 0 :
        game_over_text = font.render("FINAL SCORE : "+str(score)+" ", True,orange,black)
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()
        #pygame.mixer.music.stop()

        is_pause =True
        while is_pause :
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    score = 0
                    burger_eaten = 0
                    player_lives = player_starting_lives
                    boost_level =starting_boost_level
                    burger_velocity = starting_burger_velocity
                    #pygame.mixer.music.play(-1,0.0)
                    is_pause =False 
                if event.type == pygame.QUIT :
                    is_pause = False
                    running = False

    #fill the surface
    display_surface.fill(black)

    #blit
    display_surface.blit(points_text,points_rect)
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(eaten_text,eaten_rect)
    display_surface.blit(lives_text,lives_rect)
    display_surface.blit(boost_text,boost_rect)
    pygame.draw.line(display_surface,white,(0,100),(ww,100),3)

    #image blit
    display_surface.blit(burger_img,burger_rect)
    display_surface.blit(player_img,player_rect)

    #update
    pygame.display.update()
    Clock.tick(fps)

#end of game
pygame.quit()