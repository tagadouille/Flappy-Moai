import pygame
import random

def txt_y():
    var = [i for i in range(200,530) if i%10 == 0]
    var += var*5
    random.shuffle(var)
    return var

def crypt(score):
    scor = str(score)
    ret = ""
    for i in scor:
        ret += str(chr(ord(i) + 3407))
    return ret

def decrypt(crypt):
    ret = ""
    for i in crypt:
        ret += str(chr(ord(i) - 3407))
    return ret
def highscore(score):
    f = open("score.txt","a",1,"utf-8")
    f.close()
    f = open("score.txt","r+",1,"utf-8")
    maxi = int(decrypt(f.read()))
    if maxi < score:
        f.close()
        f = open("score.txt","w",1,"utf-8")
        f.write(crypt(score))
        return True
    else:
        f.close()
        return False
    f.close()
    
ly = txt_y()

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,speed):
        super().__init__()
        self.image = pygame.image.load("moai.png")
        self.image = pygame.transform.scale_by(self.image,0.6)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speed = speed
        self.gravity = 4
        self.jump  = False
        self.jump_remain = 1
        self.y_start = 0
        self.y_end = 0
        self.down = False
        
    def gravit(self,obj):
        if self.rect.colliderect(obj) == True:
            self.jump_remain = 1
            self.rect.y -= self.gravity
            self.gravity = 3
        self.rect.y += self.gravity
        
    def jumper(self,obj):
        if self.jump == True:
           self.down = False
           self.y_end = self.y_start - 10
           self.jump_remain = 0
           self.gravity = -14
        if self.y_end > self.rect.y:
            self.jump = False
            self.gravity = 3
            self.down = True
        if self.down == True:
            self.jump_remain = 1
        
class Pipe():
    def __init__(self):
        self.x = 280
        self.y = ly
    
class Pipe1(pygame.sprite.Sprite,Pipe):
    def __init__(self,i):
        pygame.sprite.Sprite.__init__(self)
        Pipe.__init__(self)
        self.all_pipe1 = pygame.sprite.Group()
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y[i]
        
    def forward(self):
        self.rect.x -= 2
    def spawn(self,i):
        pipe1 = Pipe1(i)
        self.all_pipe1.add(pipe1)
        
class Pipe2(pygame.sprite.Sprite,Pipe):
    def __init__(self,i):
        pygame.sprite.Sprite.__init__(self)
        Pipe.__init__(self)
        self.all_pipe2 = pygame.sprite.Group()
        self.image = pygame.image.load("pipe2.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y[i] - 620 -110
        
    def forward(self):
        self.rect.x -= 2
    def spawn(self,i):
        pipe2 = Pipe2(i)
        self.all_pipe2.add(pipe2)