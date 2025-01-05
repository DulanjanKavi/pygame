import pygame
pygame.init()
pygame.mixer.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

bg = pygame.image.load('bg.jpg')

clock = pygame.time.Clock()

score=0

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.01)
bulletSound=pygame.mixer.Sound('Game_bullet.mp3')
hitSound=pygame.mixer.Sound('Game_hit.mp3')


class Player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.jumpCount = 20
        self.standing = True
        self.walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
        self.walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
        self.image = pygame.image.load('standing.png')
        #self.hitbox=(self.x+20,self.y+10, 28, 50)
        self.mask=pygame.mask.from_surface(self.image)
        self.isHit=False

    def draw(self, win):
        self.image
        if self.walkCount >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                self.image=self.walkLeft[self.walkCount//3]
                #win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                self.image=self.walkRight[self.walkCount//3]
                #win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                self.image=self.walkRight[0]
                #win.blit(self.walkRight[0],(self.x, self.y))
            else:
                self.image=self.walkLeft[0]
                #win.blit(self.walkLeft[0],(self.x, self.y))
        win.blit(self.image,(self.x,self.y))
       # self.hitbox=(self.x+20,self.y+10, 28, 50)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        self.mask=pygame.mask.from_surface(self.image)

class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.mask = pygame.mask.from_surface(self.image)  # Create mask for bullet
        bulletSound.play()
        bulletSound.set_volume(0.8)
    
    
    def draw(self):
        pygame.draw.circle(win,self.color,(self.x, self.y),self.radius)

class Enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkcount=0
        self.vel=3
        self.path=[self.x,self.end]
        #self.hitbox=(self.x+20,self.y, 28, 60)
        self.image=self.walkRight[0]
        self.mask=pygame.mask.from_surface(self.image)
        self.helth=5
        self.visible=True

    def draw(self,win):
        if self.visible==True:
            self.move()

            if self.walkcount>33:
                self.walkcount=0
            
            if self.vel>0:
                self.image=self.walkRight[self.walkcount//11]
                #win.blit(self.walkRight[self.walkcount//11],(self.x, self.y))
                self.walkcount+=1
            else:
                self.image=self.walkLeft[self.walkcount//11]
                #win.blit(self.walkLeft[self.walkcount//11],(self.x, self.y))
                self.walkcount+=1
        #self.hitbox=(self.x+20,self.y, 28, 60)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

        pygame.draw.rect(win,(255,0,0),(self.x,self.y-10,50,10))
        pygame.draw.rect(win,(0,120,0),(self.x,self.y-10,(self.helth*10),10))
        win.blit(self.image,(self.x, self.y))
        self.mask=pygame.mask.from_surface(self.image)
    
    def move(self):
        if self.vel>0:
            if self.x<self.path[1]-self.vel:
                self.x+=self.vel
            else:
                self.vel*=-1
                self.walkcount=0
        else:
            if self.x>self.path[0]+self.vel:
                self.x+=self.vel
            else:
                self.vel*=-1
                self.walkcount=0
    
    def hit(self):
        if self.visible==True:
            global score
            score+=1
            self.helth-=1
            hitSound.play()
            hitSound.set_volume(0.8)
            if self.helth<=0:
                self.visible=0

        
    


def redrawGameWindow():
    win.blit(bg, (0,0))
    text=font.render("Score: "+ str(score),1,(0,0,0,))
    win.blit(text,(310,10))
    player.draw(win)
    if goblin.visible==True:
        goblin.draw(win)
    for builet in builets:
        builet.draw()
    
    pygame.display.update()



#mainloop
font = pygame.font.SysFont("comicsans",30,True)
player = Player(200, 410, 64,64)
goblin = Enemy(100,410,64,64,450)

builets =[]
run = True

pygame.mixer.music.play(-1)

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # Determine the direction the player is facing
                if player.left:
                    facing = -1
                else:
                    facing = 1

                # Limit the number of bullets on the screen
                if len(builets) < 5:
                    builets.append(Projectile((player.x + player.width // 2), round(player.y + player.height // 2), 6, (0, 0, 0), facing))

    for builet in builets:
        if builet.x < 500 and builet.x > 0:
            builet.x += builet.vel
        else:
            builets.pop(builets.index(builet))
        
        # Check for collision between bullet and enemy
        offset = (builet.x - goblin.x, builet.y - goblin.y)
        if goblin.mask.overlap(builet.mask, offset) and goblin.visible==True:
            print("Bullet hit the enemy!")
            goblin.hit()
            builets.pop(builets.index(builet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_RIGHT] and player.x < 500 - player.width - player.vel:
        player.x += player.vel
        player.right = True
        player.left = False
        player.standing = False
    else:
        player.standing = True
        player.walkCount = 0
        
    if not(player.isJump):
        if keys[pygame.K_UP]:
            player.isJump = True
            player.walkCount = 0
    else:
        if player.jumpCount >= -20:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.05 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 20
    
    # Check for collision between player and enemy
    offset = (goblin.x - player.x, goblin.y - player.y)
    if player.mask.overlap(goblin.mask, offset) and goblin.visible==True:
        print("Collision detected!")
        if player.isHit==False:
            score-=5
            player.isHit=True
    else:
        player.isHit=False
            
    redrawGameWindow()

pygame.quit()


