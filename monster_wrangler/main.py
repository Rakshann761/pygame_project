import pygame,random,asyncio

pygame.init()

ww=1200
wh=700
display_surface=pygame.display.set_mode((ww,wh))
pygame.display.set_caption("Monster Wrangled")

clock=pygame.time.Clock()
fps=60

#define classes
class Game():
    def __init__(self,player,monstergroup):
        self.score=0
        self.roundno=0

        self.roundtime=0
        self.frame_count=0

        self.player=player
        self.monster=monstergroup

        #self.nextlevelsound=pygame.mixer.Sound("")
        self.font=pygame.font.Font("font1.ttf",24)

        blue_image= pygame.image.load("bmonster.png")

        green_image= pygame.image.load("gmonster.png")
        puple_image= pygame.image.load("pmonster.png")
        yellow_image= pygame.image.load("omonster.png")

        self.target_monster=[blue_image,green_image,puple_image,yellow_image]
        self.target_monster_type=random.choice([0,1,2,3])
        self.target_monster_image = self.target_monster[self.target_monster_type]

        self.target_monster_rect =self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = ww//2
        self.target_monster_rect.top = 30

    def update(self):
        self.frame_count +=1
        if(self.frame_count==fps):
            self.roundtime += 1
            self.frame_count=0
        self.checkcolide()

    def draw(self):
        white =(255,255,255)
        blue = (20,176,235)
        green = (87,201,47)
        purple = (226,73,243)
        yellow = (243,157,20)

        colors= [blue,green,purple,yellow]
        catch_text=self.font.render("current Catch",True,white)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = ww//2
        catch_rect.top = 5

        score_text=self.font.render("Score : "+str(self.score),True,white)
        score_rect = score_text.get_rect()
        score_rect.topleft= (5,5)

        lives_text = self.font.render("lives : " + str(self.player.lives),True,white)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5,35)

        round_text = self.font.render("Current round : "+ str(self.roundno),True,white)
        round_rect = round_text.get_rect()
        round_rect.topleft= (5,65)

        time_text =self.font.render("round time : "+str(self.roundtime),True,white)
        time_rect = time_text.get_rect()
        time_rect.topright = (ww-10 ,5)

        warp_text = self.font.render("warps : "+str(self.player.warps),True,white)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (ww-10,35)

        display_surface.blit(catch_text,catch_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(lives_text,lives_rect)
        display_surface.blit(time_text,time_rect)
        display_surface.blit(warp_text,warp_rect)
        display_surface.blit(self.target_monster_image,self.target_monster_rect)

        pygame.draw.rect(display_surface,colors[self.target_monster_type],(ww//2-32,30,64,64),2)
        pygame.draw.rect(display_surface,colors[self.target_monster_type],(0,100,ww,wh-200),4)



    def checkcolide(self):
        collided_monster =pygame.sprite.spritecollideany(self.player,self.monster)
        if collided_monster:
            if collided_monster.type ==self.target_monster_type:
                self.score += 100*self.roundno
                collided_monster.remove(self.monster)
                if(self.monster):
                    #self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    self.player.reset()
                    self.startround()
            else:
                #self.player.die_sound()
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.pausegame("final Score : "+str(self.score),"text")
                    self.gamereset()
                self.player.reset()   

    def startround(self):
        self.score+=int(10000*self.roundno/(1+self.roundtime))
        self.roundtime =0
        self.frame_count=0
        self.roundno+=1
        self.player.warps += 1

        for monster in self.monster:
            self.monster.remove(monster)

        #add monster to the monster group
        for i in range(self.roundno):
            self.monster.add(Monster(random.randint(0,ww-64),random.randint(100,wh-164),
                                     self.target_monster[0],0))
            self.monster.add(Monster(random.randint(0,ww-64),random.randint(100,wh-164),
                                     self.target_monster[1],1))
            self.monster.add(Monster(random.randint(0,ww-64),random.randint(100,wh-164),
                                     self.target_monster[2],2))
            self.monster.add(Monster(random.randint(0,ww-64),random.randint(100,wh-164),
                                     self.target_monster[3],3))
        #choose new target
        self.choose_new_target()
        #self.next_level.play()

    def choose_new_target(self):
        target_monster = random.choice(self.monster.sprites())
        self.target_monster_type =target_monster.type
        self.target_monster_image=target_monster.image

    def pausegame(self,maintext,sub_text):
        global running
        white=(255,255,255)
        main_text =self.font.render(maintext,True,(white))
        main_rect = main_text.get_rect()
        main_rect.center = (ww//2,wh//2-20)

        subtext=self.font.render("Press 'Enter' to play the game",True,white)
        subrect=subtext.get_rect()
        subrect.center = (ww//2,wh//2+64)

        text =self.font.render("Press 'ESC' is Quit the game",True,white)
        text_rect = text.get_rect()
        text_rect.center = (ww//2,wh//2+128)

        display_surface.fill((0,0,0))
        display_surface.blit(main_text,main_rect)
        display_surface.blit(subtext,subrect)
        display_surface.blit(text,text_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused=False
                    if event.key == pygame.K_ESCAPE:
                        running=False
                        exit()
                if event.type == pygame.QUIT:
                    is_paused=False
                    running=False
                    exit()
        

    def gamereset(self):
        self.score = 0
        self.roundno = 0
        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()
        self.startround()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("knight.png")
        self.rect=self.image.get_rect()
        self.rect.centerx = ww//2
        self.rect.bottom = wh

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        #self.catch_sound = pygame.mixer.Sound("")
        #self.die_sound = same here
        #self.warp_sound = same here

    def update(self):
        keys=pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left >0 :
            self.rect.x -= self.velocity
        if (keys[pygame.K_RIGHT]or keys[pygame.K_d])and self.rect.right <ww : 
            self.rect.x += self.velocity
        if (keys[pygame.K_UP]or keys[pygame.K_w])and self.rect.top >100 :
            self.rect.y -= self.velocity
        if (keys[pygame.K_DOWN]or keys[pygame.K_s])and self.rect.bottom < wh-100 :
            self.rect.y += self.velocity

        
    def warp(self):
        if self.warps > 0:
            self.warps-=1
            #self.warpsound.play()
            self.rect.bottom = wh
             
    def reset(self):
        self.rect.centerx = ww//2
        self.rect.bottom = wh

class Monster(pygame.sprite.Sprite):
    def __init__(self,x,y,image,monster_type):
        super().__init__()
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        #monster type is an inr 1-blue, 1-green, 2-purple, 3-yellow
        self.type = monster_type

        self.dx = random.choice([-1,1])
        self.dy =random.choice([-1,1])
        self.velocity = random.randint(1,5)
        
    def update(self):
        self.rect.x += self.dx*self.velocity
        self.rect.y += self.dy*self.velocity

        if self.rect.left <= 0 or self.rect.right >= ww :
            self.dx = -self.dx
        if self.rect.top <=100 or self.rect.bottom >= wh -100 :
            self.dy = -self.dy
        

#player group
myplayergroup=pygame.sprite.Group()
myplayer=Player()
myplayergroup.add(myplayer)

mymonstergroup=pygame.sprite.Group()

mygame=Game(myplayer,mymonstergroup)
mygame.pausegame("Monster Wrangler","Press enter to Play")
mygame.startround()

async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    myplayer.warp()

        display_surface.fill((0,0,0))

        myplayergroup.update()
        myplayergroup.draw(display_surface)

        mymonstergroup.update()
        mymonstergroup.draw(display_surface)

        mygame.update()
        mygame.draw()

        pygame.display.update()
        clock.tick(fps)
        asyncio.sleep(0)

asyncio.run(main())


#pygame.quit()