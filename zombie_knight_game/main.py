import pygame,random,asyncio

vector = pygame.math.Vector2

pygame.init()

ww = 1280
wh = 736

display_surface = pygame.display.set_mode((ww,wh))
pygame.display.set_caption("Zombie Knight")
fps=60
clock = pygame.time.Clock()

class Game():
    def __init__(self,player,zombiegroup,platformgroup,portalgroup,bulletgroup,rubygroup):
        self.startrntime = 30
        self.start_zombiecreatetime = 5

        self.score = 0
        self.rno = 1
        self.frame_count = 0
        self.rntime = self.startrntime
        self.zombiecreatetime = self.start_zombiecreatetime

        self.titlefont = pygame.font.Font("font/Poultrygeist.ttf",48)
        self.hudfont = pygame.font.Font("font/Pixel.ttf",24) 

        #self.lost_ruby_sound = pygame.mixer.Sound("")
        #self.rubypickup_sound = pygame.mixer.Sound("")
        #pygame.mixer.music.load("")
        
        self.player = player
        self.zombiegroup = zombiegroup
        self.portalgroup = portalgroup
        self.bulletgroup = bulletgroup
        self.rubygroup = rubygroup
        self.platformgroup = platformgroup

        

    def update(self):
        self.frame_count += 1
        if self.frame_count% fps == 0:
            self.rntime -= 1
            self.frame_count = 0

        self.checkcollide()
        self.add_zombie()
        self.checkroundcomplete()
        self.checkgameover()

    def draw(self):
        white=(255,255,255)
        green = (25,255,25)

        score_text = self.hudfont.render("score : "+str(self.score),True,white)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10 , wh-50)

        health_text = self.hudfont.render("Health : "+str(self.player.health),True,white)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10,wh-25)

        title_text =  self.titlefont.render("Zombie Knight",True,green)
        title_rect = title_text.get_rect()
        title_rect.center = (ww//2,wh-25)

        round_text = self.hudfont.render("Current round : "+ str(self.rno),True,white)
        round_rect = round_text.get_rect()
        round_rect.topright= (ww-10,wh-50)

        time_text = self.hudfont.render("Sunrise : "+str(self.rntime),True,white)
        time_rect = time_text.get_rect()
        time_rect.topright = (ww-10,wh-25)

        display_surface.blit(title_text,title_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(health_text,health_rect)
        display_surface.blit(time_text,time_rect)


    def add_zombie(self):
        if self.frame_count %fps ==0:
            if self.rntime % self.zombiecreatetime ==0 :
                zombie = Zombie(self.platformgroup,self.portalgroup,self.rno, 5 + self.rno)
                self.zombiegroup.add(zombie)

    def checkcollide(self):
        collidedict = pygame.sprite.groupcollide(self.bulletgroup,self.zombiegroup,True,False)
        if collidedict:
            for zombies in collidedict.values():
                for zombie in zombies:
                    #zombie.hit_sound.play()
                    zombie.isdead = True
                    zombie.animate_die = True

        collide_list = pygame.sprite.spritecollide(self.player,self.zombiegroup,False)
        if collide_list:
            for zombie in collide_list:
                if zombie.isdead == True:
                    #zombie.kick_sound.play()
                    zombie.kill()
                    self.score +=25

                    ruby = Ruby(self.platformgroup,self.portalgroup)
                    self.rubygroup.add(ruby)

                else:
                    self.player.health -= 20
                    #self.player_hit_sound.play()
                    self.player.position.x -= 256*zombie.direction
                    self.player.rect.bottomleft = self.player.position
                    
        if pygame.sprite.spritecollide(self.player,self.rubygroup,True):
            #self.ruby_pickup_sound.play()
            self.score += 100
            self.player.health += 10
            if self.player.health >self.player.starthealth:
                self.player.health = self.player.starthealth

        for zombie in self.zombiegroup:
            if zombie.isdead == False:
                if pygame.sprite.spritecollide(zombie,self.rubygroup,True):
                    #self.lost_rubysound.play()
                    zombie = Zombie(self.platformgroup,self.portalgroup,self.rno,self.rno+5)
                    self.zombiegroup.add(zombie)

    def checkroundcomplete(self):
        if self.rntime == 0:
            self.startnewro()

    def checkgameover(self):
        if self.player.health <= 0:
            #pygame.mixer.music.stop()
            self.pausegame("Game Over!    Final Score : "+str(self.score),"Press 'Enter' to play again...")
            self.resetgame()

    def startnewro(self):
        self.rno += 1
        if self.rno < self.zombiecreatetime:
            self.zombiecreatetime -= 1

        self.rntime = self.startrntime

        self.zombiegroup.empty()
        self.rubygroup.empty()
        self.bulletgroup.empty()

        self.player.reset()

        self.pausegame("You've Survived the night ","Press 'Enter' to continue")


    def pausegame(self,maintext,subtext):
        global running
        #pygame.mixer.music.pause()
        white=(255,255,255)
        black = (0,0,0)
        green =(25,255,25)

        main_text =self.titlefont.render(maintext,True,green)
        main_rect = main_text.get_rect()
        main_rect.center = (ww//2,wh//2-20)

        subtext=self.titlefont.render("Press 'Enter' to play the game",True,white)
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
                        #pygame.mixer.music.unpause()
                    if event.key == pygame.K_ESCAPE:
                        running=False
                if event.type == pygame.QUIT:
                    is_paused=False
                    running=False

        

    def resetgame(self):
        
        self.score = 0
        self.rno = 1
        self.rntime = self.startrntime
        self.zombiecreatetime = self.start_zombiecreatetime

        self.player.health = self.player.starthealth
        self.player.reset()

        self.zombiegroup.empty()
        self.rubygroup.empty()
        self.bulletgroup.empty()

        #pygame.mixer.music.play(-1,0,0)


class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,image_int,maingroup,subgroup=""):
        super().__init__()
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load("img/tiles/Tile1.png"),(32,32))
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load("img/tiles/Tile2.png"),(32,32))
            subgroup.add(self)
        elif image_int ==3:
            self.image = pygame.transform.scale(pygame.image.load("img/tiles/Tile3.png"),(32,32))
            subgroup.add(self)
        elif image_int ==4:
            self.image = pygame.transform.scale(pygame.image.load("img/tiles/Tile4.png"),(32,32))
            subgroup.add(self)
        elif image_int ==5:
            self.image = pygame.transform.scale(pygame.image.load("img/tiles/Tile5.png"),(32,32))
            subgroup.add(self)
        maingroup.add(self)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.mask = pygame.mask.from_surface(self.image)



class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,platformgroup,portalgroup,bulletgroup) :
        super().__init__()
        self.hori_acc = 1.7
        self.hori_friction = 0.15
        self.vertical_acc = 0.8
        self.vert_jump_speed = 17
        self.starthealth = 100

        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_left_sprites = []
        self.jump_right_sprites = []
        self.attack_left_sprites = []
        self.attack_right_sprites = []
        
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (1).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (2).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (3).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (4).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (5).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (6).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (7).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (8).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (9).png"),(64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/run/Run (10).png"),(64,64)))
        for sprite in self.move_right_sprites:
            #flip(var,flip horizontal, flip vertical)
            self.move_left_sprites.append(pygame.transform.flip(sprite,True,False))

        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (1).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (2).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (3).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (4).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (5).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (6).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (7).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (8).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (9).png"),(64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/idle/Idle (10).png"),(64,64)))
        for sprite in self.idle_right_sprites:
            #flip(var,flip horizontal, flip vertical)
            self.idle_left_sprites.append(pygame.transform.flip(sprite,True,False))

        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (1).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (2).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (3).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (4).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (5).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (6).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (7).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (8).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (9).png"),(64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/jump/Jump (10).png"),(64,64)))
        for sprite in self.jump_right_sprites:
            #flip(var,flip horizontal, flip vertical)
            self.jump_left_sprites.append(pygame.transform.flip(sprite,True,False))

        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (1).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (2).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (3).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (4).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (5).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (6).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (7).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (8).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (9).png"),(64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("img/player/attack/Attack (10).png"),(64,64)))
        for sprite in self.attack_right_sprites:
            #flip(var,flip horizontal, flip vertical)
            self.attack_left_sprites.append(pygame.transform.flip(sprite,True,False))


        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect =self.image.get_rect()
        self.rect.bottomleft = (x,y)

        self.platformgroup =platformgroup
        self.portalgroup = portalgroup
        self.bulletgroup = bulletgroup

        self.animate_jump = False
        self.animate_fire = False
        
        #self.jump_sound = pygame.mixer.Sound("")
        #self.slash_sound = pygame.mixer.Sound("")
        #self.portal_sound = pygame.mixer.Sound("")
        #self.hit_sound = pygame.mixer.Sound("")
        
        #kinematics
        self.position = vector(x,y)
        self.velocity = vector(0,0)
        self.accelerate = vector(0,self.vertical_acc)

        self.health = self.starthealth
        self.start_x = x
        self.start_y = y


    def update(self):
        self.move()
        self.checkcollide()
        self.checkanimate()

        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.accelerate = vector(0,self.vertical_acc)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.accelerate.x = -self.hori_acc
            self.animate(self.move_left_sprites,.5)
        elif keys[pygame.K_RIGHT]:
            self.accelerate.x = self.hori_acc
            self.animate(self.move_right_sprites,.5)
        else:
            if self.velocity.x >0:
                self.animate(self.idle_right_sprites,.5)
            else:
                self.animate(self.idle_left_sprites,.5)


        self.accelerate.x -=self.velocity.x *self.hori_friction
        self.velocity += self.accelerate
        self.position += self.velocity + 0.5*self.accelerate

        if self.position.x <0:
            self.position.x = ww
        elif self.position.x >ww:
            self.position.x = 0
        
        self.rect.bottomleft = self.position

    def checkcollide(self):
        if self.velocity.y > 0 :
            collided_platorm = pygame.sprite.spritecollide(self,self.platformgroup,False,pygame.sprite.collide_mask)
            if collided_platorm :
                self.position.y = collided_platorm[0].rect.top + 5
                self.velocity.y = 0

        if self.velocity.y < 0 :
            collided_platorm = pygame.sprite.spritecollide(self,self.platformgroup,False,pygame.sprite.collide_mask)
            if collided_platorm:
                self.velocity.y =0
                while pygame.sprite.spritecollide(self,self.platformgroup,False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        if pygame.sprite.spritecollide(self,self.portalgroup,False):
            #self.portal_sound.play()
            if self.position.x > ww//2:
                self.position.x = 86
            else :
                self.position.x = ww -150
            
            if self.position.y > wh//2:
                self.position.y = 64
            else:
                self.position.y = wh -132
            
            self.rect.bottomleft = self.position



    def checkanimate(self):
        if self.animate_jump == True:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites,.1)
            else:
                self.animate(self.jump_left_sprites,.1)
        
        if self.animate_fire == True:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites,.5)
            else:
                self.animate(self.attack_left_sprites,.5)
        

    def jump(self):
        if pygame.sprite.spritecollide(self,self.platformgroup,False):
            #self.jump_sound.play()
            self.velocity.y = -self.vert_jump_speed
            self.animate_jump = True


    def fire(self):
        #self.slash_sound.play()
        Bullet(self.rect.centerx,self.rect.centery,self.bulletgroup,self)
        self.animate_fire =True

    def reset(self):
        self.velocity = vector(0,0)
        self.position = vector(self.start_x,self.start_y)
        self.rect.bottomleft = self.position

    def animate(self,sprite_list,speed):
        if self.current_sprite < len(sprite_list) -1 :
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            if self.animate_jump == True:
                self.animate_jump =False
            if self.animate_fire :
                self.animate_fire = False
        
        self.image = sprite_list[int(self.current_sprite)]


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,bulletgroup,player):
        super().__init__()
        self.velocity = 18
        self.range = 300

        if player.velocity.x >0:
            self.image = pygame.transform.scale(pygame.image.load("img/player/Slash.png"),(32,32))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip
                                                (pygame.image.load("img/player/Slash.png"),True,False),(32,32))
            self.velocity = -self.velocity
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.start_x = x
        bulletgroup.add(self)
        

    def update(self):
        self.rect.x +=self.velocity
        if abs(self.rect.x - self.start_x)>self.range:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self,platformgroup,portalgroup,minspeed, maxspeed) :
        super().__init__()
        self.vertical_acc = 3
        self.rise_time = 2

        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []
        
        gender = random.randint(0,1)
        if gender == 0:
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (1).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (2).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (3).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (4).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (5).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (6).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (7).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (8).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (9).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Walk (10).png"),(64,64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite,True,False))

    
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (1).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (2).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (3).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (4).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (5).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (6).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (7).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (8).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (9).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (10).png"),(64,64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite,True,False))

            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (10).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (9).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (8).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (7).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (6).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (5).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (4).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (3).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (2).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/boy/Dead (1).png"),(64,64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite,True,False))
        else:
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (1).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (2).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (3).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (4).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (5).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (6).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (7).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (8).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (9).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Walk (10).png"),(64,64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite,True,False))

    
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (1).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (2).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (3).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (4).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (5).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (6).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (7).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (8).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (9).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (10).png"),(64,64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite,True,False))

            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (10).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (9).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (8).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (7).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (6).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (5).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (4).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (3).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (2).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("img/zombie/girl/Dead (1).png"),(64,64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite,True,False))
        
        self.direction = random.choice([-1,1])

        self.current_sprite =0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.current_sprite]
        else:
            self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100,ww-100),-100)
        self.platformgroup = platformgroup
        self.portalgroup = portalgroup

        self.animate_die = False
        self.animate_rise = True

        #self.hit_sound= pygame.mixer.Sound("")
        #self.kick_sound= pygame.mixer.Sound("")
        #self.portalgroup_sound= pygame.mixer.Sound("")

        self.position = vector(self.rect.x , self.rect.y)
        self.velocity = vector(self.direction*random.randint(minspeed,maxspeed),0)
        self.accelerate = vector(0,self.vertical_acc)

        self.isdead = False
        self.rntime = 0
        self.frame_count = 0

    def update(self):
        self.move()
        self.checkcollide()
        self.checkanimate()

        if self.isdead :
            self.frame_count +=1
            if self.frame_count % fps == 0:
                self.rntime +=1
                if self.rntime == self.rise_time:
                    self.animate_rise = True
                    self.current_sprite = 0

    def move(self):
        if not self.isdead :
            if self.direction == -1:
                self.animate(self.walk_left_sprites,.5)
            else:
                self.animate(self.walk_right_sprites,.5)
            
            self.velocity += self.accelerate
            self.position += self.velocity + 0.5*self.accelerate

            if self.position.x <0:
                self.position.x = ww
            elif self.position.x >ww:
                self.position.x = 0
            
            self.rect.bottomleft = self.position

    def checkcollide(self):
    
        collided_platorm = pygame.sprite.spritecollide(self,self.platformgroup,False)
        if collided_platorm :
            self.position.y = collided_platorm[0].rect.top + 1
            self.velocity.y = 0

        
        if pygame.sprite.spritecollide(self,self.portalgroup,False):
            #self.portal_sound.play()
            if self.position.x > ww//2:
                self.position.x = 86
            else :
                self.position.x = ww -150
            
            if self.position.y > wh//2:
                self.position.y = 64
            else:
                self.position.y = wh -132
            
            self.rect.bottomleft = self.position

    def checkanimate(self):
        if self.animate_die:
            if self.direction == 1:
                self.animate(self.die_right_sprites,0.09)
            else:
                self.animate(self.die_left_sprites,0.09)
        
        if self.animate_rise :
            if self.direction == 1:
                self.animate(self.rise_right_sprites,0.09)
            else:
                self.animate(self.rise_left_sprites,.09)

    def animate(self,sprite_list,speed):
        if self.current_sprite < len(sprite_list) -1 :
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            if self.animate_die :
                self.current_sprite = len(sprite_list)-1
                self.animate_die = False
            if self.animate_rise :
                self.animate_rise = False
                self.isdead = False
                self.frame_count = 0
                self.rntime = 0

        
        self.image = sprite_list[int(self.current_sprite)]


class Rubymaker(pygame.sprite.Sprite):
    def __init__(self,x,y,maingroup) -> None:
        super().__init__()
        self.rubysprite = []

        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby11.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby22.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby33.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby44.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby55.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby66.png"),(64,64)))
        
        self.cur_sprite = 0
        self.image = self.rubysprite[self.cur_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        maingroup.add(self)


    def update(self):
        self.animate(self.rubysprite,0.25)

    def animate(self,sprite_list,speed):
        if self.cur_sprite < len(sprite_list) -1 :
            self.cur_sprite += speed
        else:
            self.cur_sprite = 0
        
        self.image = sprite_list[int(self.cur_sprite)]


class Ruby(pygame.sprite.Sprite):
    def __init__(self,platformgroup,portalgroup) -> None:
        super().__init__()
        self.vertical_acc = 3
        self.hori_velocity = 5
        
        self.rubysprite = []

        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby11.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby22.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby33.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby44.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby55.png"),(64,64)))
        self.rubysprite.append(pygame.transform.scale(pygame.image.load("img/ruby/ruby66.png"),(64,64)))
        
        self.current_sprite = 0
        self.image = self.rubysprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (ww//2,100)

        self.platformgroup = platformgroup
        self.portalgroup = portalgroup

        #self.portal_spund = pygame.mixer.Sound("")

        self.position = vector(self.rect.x , self.rect.y)
        self.velocity = vector(random.choice([-self.hori_velocity ,self.hori_velocity]),0)
        self.accelarate = vector(0,self.vertical_acc)



    def update(self):
        self.animate(self.rubysprite,.25)
        self.move()
        self.checkcollide()

    def checkcollide(self):
        collided_platorm = pygame.sprite.spritecollide(self,self.platformgroup,False)
        if collided_platorm :
            self.position.y = collided_platorm[0].rect.top + 1
            self.velocity.y = 0

        
        if pygame.sprite.spritecollide(self,self.portalgroup,False):
            #self.portal_sound.play()
            if self.position.x > ww//2:
                self.position.x = 86
            else :
                self.position.x = ww -150
            
            if self.position.y > wh//2:
                self.position.y = 64
            else:
                self.position.y = wh -132
            
            self.rect.bottomleft = self.position

    def move(self):

        self.velocity += self.accelarate
        self.position += self.velocity + 0.5*self.accelarate

        if self.position.x <0:
            self.position.x = ww
        elif self.position.x >ww:
            self.position.x = 0
        
        self.rect.bottomleft = self.position

    def animate(self,sprite_list,speed):
        if self.current_sprite < len(sprite_list) -1 :
            self.current_sprite += speed
        else:
            self.current_sprite = 0
        
        self.image = sprite_list[int(self.current_sprite)]


class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y,color,portagroup="") -> None:
        super().__init__()
        if color == "green":
            self.image = pygame.transform.scale(pygame.image.load("img/portal/teleport2.png"),(64,64))
        else:
            self.image = pygame.transform.scale(pygame.image.load("img/portal/teleport1.png"),(64,64))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        portagroup.add(self)


my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
my_bullet_group = pygame.sprite.Group()
my_portal_group = pygame.sprite.Group()
my_ruby_group = pygame.sprite.Group()
my_zombie_group =pygame.sprite.Group()

# 0 - no tile , 1 - dirt, 2-5 -->platform, 6 - rubymaker, 7-8 -->zombie, 9 - player 
#23 row and 40 column

tile_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,6,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

for i in range(len(tile_map)):
    for j in range(len(tile_map[0])):
        if tile_map[i][j]== 1:
            Tile(j*32,i*32,1,my_main_tile_group)
        elif tile_map[i][j]== 2:
            Tile(j*32,i*32,2,my_main_tile_group,my_platform_group)
        elif tile_map[i][j]== 3:
            Tile(j*32,i*32,3,my_main_tile_group,my_platform_group)
        elif tile_map[i][j]== 4:
            Tile(j*32,i*32,4,my_main_tile_group,my_platform_group)
        elif tile_map[i][j]== 5:
            Tile(j*32,i*32,5,my_main_tile_group,my_platform_group)
        elif tile_map[i][j]== 6:
            Rubymaker(j*32,i*32,my_main_tile_group)
        elif tile_map[i][j]== 7:
            Portal(j*32,i*32+32,"green",my_portal_group)
        elif tile_map[i][j]== 8:
            Portal(j*32,i*32+32,"blue",my_portal_group)
        elif tile_map[i][j]== 9:
            my_player = Player(j*32 - 32,i*32 +32,my_platform_group,my_portal_group,my_bullet_group)
            my_player_group.add(my_player)


backimg = pygame.transform.scale(pygame.image.load("img/tiles/BG.png"),(1280,736))
back_rect = backimg.get_rect()
back_rect.topleft = (0,0)

my_game = Game(my_player,my_zombie_group,my_platform_group,my_portal_group,my_bullet_group,my_ruby_group)
my_game.pausegame("Zombie Knight","Press 'ENTER' to play")
#pygame.mixer.music.play(-1,0,0)

async def main():
    running = True
    while running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    my_player.jump()
                if event.key == pygame.K_SPACE:
                    my_player.fire()
                ''''if event.key == pygame.K_RETURN:
                    zombie = Zombie(my_platform_group,my_portal_group,2,7)
                    my_zombie_group.add(zombie)'''

        display_surface.blit(backimg,back_rect)

        my_main_tile_group.update()
        my_main_tile_group.draw(display_surface)
        
        my_portal_group.update()
        my_portal_group.draw(display_surface)

        my_player_group.update()
        my_player_group.draw(display_surface)

        my_bullet_group.update()
        my_bullet_group.draw(display_surface)

        my_zombie_group.update()
        my_zombie_group.draw(display_surface)
        
        my_ruby_group.update()
        my_ruby_group.draw(display_surface)

        my_game.update()
        my_game.draw()

        pygame.display.flip()
        clock.tick(fps)
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())
    pygame.quit()