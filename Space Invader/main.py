import pygame,random

pygame.init()

ww=1200
wh=700

display_surface=pygame.display.set_mode((ww,wh))
pygame.display.set_caption("Space Invader")

fps=60
clock=pygame.time.Clock()

class Game():
    def __init__(self,player,aliengroup,playerbullet,alienbullet):
        self.roundno = 1
        self.score = 0
        
        self.player = player
        self.alien_group = aliengroup
        self.aleinbullet =alienbullet
        self.playerbullet = playerbullet

        #self.newround = pygame.mixer.Sound()
        #self.breach_point = pygame.mixer.Sound()
        #self.alien_hit = pygame.mixer.Sound()
        #self.player_hit = pygame.mixer.Sound()
        
        self.font = pygame.font.Font("font1.ttf",32)

    def update(self):
        self.shift_alien()
        self.checkcollision()
        self.checkroundcomplete()

    def draw(self):
        white = (255,255,255)

        score_text=self.font.render("Score : "+str(self.score),True,white)
        score_rect = score_text.get_rect()
        score_rect.top= (10)

        lives_text = self.font.render("Lives : " + str(self.player.lives),True,white)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (ww-20,10)

        round_text = self.font.render("Round : "+ str(self.roundno),True,white)
        round_rect = round_text.get_rect()
        round_rect.topleft = (ww//2-50,10)

        
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(lives_text,lives_rect)

        pygame.draw.line(display_surface,white,(0,50),(ww,50),4)
        pygame.draw.line(display_surface,white,(0,wh-100),(ww,wh-100),4)

    def shift_alien(self):
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= ww:
                shift = True
        
        if shift == True:
            breach=False
            for alien in (self.alien_group.sprites()):
                alien.rect.y += 10*self.roundno
        
                alien.direction = -1*alien.direction
                alien.rect.x +=alien.direction * alien.velocity

                if alien.rect.bottom >= wh-100 :
                    breach = True
            if breach==True:
                #self.breach_sound.play()
                self.player.lives -= 1
                self.checkgamestatus("Alien breached the line","Press 'Enter' to continue")

    def checkcollision(self):
        if pygame.sprite.groupcollide(self.playerbullet,self.alien_group,True,True):
            #self.alien_hit_sound.play()
            self.score += 100
        if pygame.sprite.spritecollide(self.player,self.aleinbullet,True):
            #self.player_hit_sound.play()
            self.player.lives -=1

            self.checkgamestatus("You've been hit","press 'Enter' to continue")

    def startnewround(self): 
        for i in range(11):
            for j in range(5):
                alien = Alein(64 + i*64,64+j*64,self.roundno,self.aleinbullet)
                my_alein_group.add(alien)

        #self.new_round_sound.play()
        self.pausegame("space Invader Round "+str(self.roundno),"Press 'Enter' to Begin") 

    def checkroundcomplete(self):
        
        if not (self.alien_group):
            self.score += 1000*self.roundno
            self.roundno += 1

            self.startnewround()
        
    def checkgamestatus(self,maintext,subtext):
        self.aleinbullet.empty()
        self.playerbullet.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()
        
        if self.player.lives <= 0 :
            self.resetgame()
        else:
            self.pausegame(maintext,subtext)

    def pausegame(self,maintext,subtext):
        global running
        
        white =(255,255,255)
        black = (0,0,0)

        main_text =self.font.render(maintext,True,(white))
        main_rect = main_text.get_rect()
        main_rect.center = (ww//2,wh//2)

        subtext=self.font.render("Press 'Enter' to play the game",True,white)
        subrect=subtext.get_rect()
        subrect.center = (ww//2,wh//2+64)

        display_surface.fill(black)
        display_surface.blit(main_text,main_rect)
        display_surface.blit(subtext,subrect)
        
        pygame.display.update()
        
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused=False
                    if event.key == pygame.K_ESCAPE:
                        running=False
                if event.type == pygame.QUIT:
                    is_paused=False
                    running=False

    def resetgame(self):
        self.pausegame("Final Score: "+str(self.score),"press 'Enter' to play again")
        self.score = 0
        self.roundno = 1
        self.player.lives=5

        self.aleinbullet.empty()
        self.alien_group.empty()
        self.playerbullet.empty()

        self.startnewround()

class Player(pygame.sprite.Sprite):
    def __init__(self,bullet_group):
        super().__init__()
        self.image = pygame.image.load("space.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = ww//2
        self.rect.bottom =wh

        self.lives = 5
        self.velocity = 8

        self.bullet_group =bullet_group
        #self.shoot_sound =pygame.mixer.Sound("")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right <ww:
            self.rect.x += self.velocity
        
    def fire(self):
        #self.shootsound.play()
        if len(self.bullet_group)<3:
            PlayerBullet(self.rect.centerx,self.rect.top,self.bullet_group)
    def reset(self):
        self.rect.centerx = ww//2

class Alein(pygame.sprite.Sprite):
    def __init__(self,x,y,velocity,bullet_group):
        super().__init__()
        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.starting_x = x
        self.starting_y = y
  
        self.direction = 1
        self.velocity = velocity
        self.bulletgroup = bullet_group

        #self.shootsound = pygame.mixer.Sound("")

    def update(self):
        self.rect.x += self.direction*self.velocity

        if random.randint(0,1000)>999 and len(self.bulletgroup)<3:
            #self.shootsound.play()
            self.fire()
        
    def fire(self):
        AlienBullet(self.rect.centerx,self.rect.bottom,self.bulletgroup)
    def reset(self):
        self.rect.topleft = (self.starting_x,self.starting_y)
        self.direction = 1
        
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,bullet_group):
        super().__init__()
        self.image =pygame.image.load("green.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10
        bullet_group.add(self)
    
    def update(self):
        self.rect.y -= self.velocity
        if self.rect.bottom < 0 :
            self.kill()   

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,bullet_group):
        super().__init__()
        self.image = pygame.image.load("red.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 5
        bullet_group.add(self)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.bottom > wh :
            self.kill() 

my_player_bullet_group = pygame.sprite.Group()
my_alein_bullet_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
myplayer=Player(my_player_bullet_group)
my_player_group.add(myplayer)

my_alein_group = pygame.sprite.Group()

my_game=Game(myplayer,my_alein_group,my_player_bullet_group,my_alein_bullet_group)
my_game.startnewround()

running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                myplayer.fire()
    
    display_surface.fill((0,0,0))

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alein_group.update()
    my_alein_group.draw(display_surface)

    my_alein_bullet_group.update()
    my_alein_bullet_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()