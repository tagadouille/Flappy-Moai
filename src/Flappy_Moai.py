import pygame
import sys
import classmoai

pygame.init()

pygame.display.set_caption("Flappy Moai")
screen_x,screen_y = (300,620)#dimension de l'écran
screen = pygame.display.set_mode((screen_x,screen_y))
icon = pygame.image.load("moai.png")#icone de la fenetre
pygame.display.set_icon(icon)#application de l'icone

#font init
font = pygame.font.SysFont("liberation mono",50)
font2 = pygame.font.SysFont("liberation mono",18)

#sprites init
pipe = classmoai.Pipe1(0)
pipe2 = classmoai.Pipe2(0)
player = classmoai.Player((screen_x)//2-100,300,1)
#title screen
menu = pygame.image.load("title screen.jpg")
menuRect = menu.get_rect()

#lose screen 
lose = pygame.image.load("game over.png")
loseRect = lose.get_rect()
valid = pygame.image.load("valid.png")
valid = pygame.transform.scale_by(valid,0.7)#scale
validRect = valid.get_rect()
validRect.x,validRect.y = (screen_x//2 - 100,screen_y//2 + 15)

quitt = pygame.image.load("quit.png")
quitt = pygame.transform.scale_by(quitt,0.7)#scale
quittRect = quitt.get_rect()
quittRect.x,quittRect.y = (screen_x//2 + 20,screen_y//2 + 15)

new_record = pygame.image.load("new record.png")
new_record = pygame.transform.scale_by(new_record,0.6)
new_recordRect = new_record.get_rect()
new_recordRect.x,new_recordRect.y = (150,255)

clock = pygame.time.Clock()
run = True
 
def collision(sprite,group):
    return pygame.sprite.spritecollide(sprite,group,False,pygame.sprite.collide_rect)

point = 0
t = 0
i = 0
hg = 0
title_screen = True

while run == True:
    while title_screen == True:
        screen.blit(menu,menuRect)
    
        pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                title_screen = False
                pygame.display.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            title_screen = False
    t+=1
    if t == 1201:
        t = 2
    screen.blit(pygame.image.load("background.jpg"),(0,0))
    screen.blit(player.image,player.rect)
    
    txt = font.render(str(point),False,(255,255,255))

    pipe.all_pipe1.draw(screen)
    pipe2.all_pipe2.draw(screen)
    floor = pygame.draw.line(screen,"green",(0,screen_y),(screen_x,screen_y),100)
 
    if t == 1:
        pipe.spawn(i)
        pipe2.spawn(i)

    if not (collision(player,pipe.all_pipe1) or collision(player,pipe2.all_pipe2) or player.rect.colliderect(floor)):
        if t%120== 0:
            point += 1
            i+=1
            pipe.spawn(i%len(pipe.y))
            pipe2.spawn(i%len(pipe.y))
            if i == 100:
                i = 0
                
        player.gravit(floor)
        player.jumper(floor)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not player.rect.y < 100:
                if player.jump_remain == 1:
                    player.jump = True
                    player.y_start = player.rect.y
        for pipes in pipe.all_pipe1:
            pipes.forward()
        for pipes in pipe2.all_pipe2:
            pipes.forward()
    else:
        hg += 1
        if hg == 1:
            hg_check = classmoai.highscore(point)
            f = open("score.txt","r",1,"utf-8")
            highscore = classmoai.decrypt(f.read())
            f.close()

        point2 = font2.render(str(point),False,(255,255,255))
        highscore2 = font2.render(str(highscore),False,(255,255,255))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                        
                if (mx >= 55 and mx <= 115) and (my >= 330 and my <= 370):
                    player.rect.x,player.rect.y = ((screen_x)//2-100,300)
                    pipe.all_pipe1.empty()
                    pipe2.all_pipe2.empty()
                    point = 0
                    t = 0
                    i = 0
                    hg = 0
                if (mx >= 176 and mx <= 235) and (my >= 330 and my <= 370):
                    run = False
                    pygame.display.quit()
                    sys.exit()
                    
        screen.blit(lose,loseRect)
        screen.blit(point2,[screen_x//2 - 40,screen_y//2 - 30])
        screen.blit(highscore2,[screen_x//2 + 30,screen_y//2 - 12])
        screen.blit(valid,validRect)
        screen.blit(quitt,quittRect)
        if hg_check == True:
            screen.blit(new_record,new_recordRect)
        
    screen.blit(txt,[screen_x//2,10])
    #retire le premier sprite de la liste de groupe de sprite si il y en a plus de 3
    if len(pipe.all_pipe1.sprites()) > 3:
        pipe.all_pipe1.sprites()[0].kill()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            classmoai.highscore(point)
            pygame.display.quit()
            sys.exit()
            
    if keys[pygame.K_ESCAPE]:
        run = False
        classmoai.highscore(point)
        pygame.display.quit()
        sys.exit()
        
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()
sys.exit()