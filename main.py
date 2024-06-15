import random
import time
import sys
import pygame
from pygame.locals import *

initialfps = 40
screenWdith = 640
screenHeight = 360
screen = pygame.display.set_mode((screenWdith,screenHeight))
game_sprites = {}
game_sound = {}
player = 'img/player.png'
background = 'img/background.jpg'
apple = ''
message = 'img/message.png'
welcome = 'img/welcome.png'
body = 'img/body.png'

def welcomescreen():
    game_sound['intro'].play()
    while True:
        for event in pygame.event.get():
            if event.type ==QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_DOWN or event.key ==K_LEFT or event.key == K_RIGHT):
                game_sound['intro'].stop()
                return
            else:
                screen.blit(game_sprites['welcome'],(0,0))
                screen.blit(game_sprites['message'],(screenWdith/2 -200,screenHeight/2 - 80))
                if int(time.time() //1)% 2 == 0:
                    screen.blit(pygame.image.load('img/taptobegin.png').convert_alpha(),(-20,0))
                pygame.display.update()
                fpsclock.tick(10)

def maingame():
    score = 0
    fps = initialfps
    playerx = screenWdith/2 -30
    playery = screenHeight/2 - 20
    snakevel = {'x':0,'y':2}
    label = 0
    LIGHT_PURPLE = (200, 162, 200)
    bodycoordinate = [{}]
    applecoordinate=getapple()
    T1 = time.time()
    timediff = 6
    add = 0
    T1obs = time.time()
    obs = [[]]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_DOWN) and label != 1:
                snakevel['x'] = 0
                snakevel['y'] = 2
                label = 0

            elif event.type == KEYDOWN and (event.key == K_UP) and label != 0:
                snakevel['x'] = 0
                snakevel['y'] = -2
                label = 1

            elif event.type == KEYDOWN and (event.key == K_RIGHT) and label != 3:
                snakevel['x'] = 2
                snakevel['y'] = 0
                label = 2

            elif event.type == KEYDOWN and (event.key == K_LEFT) and label !=2:
                snakevel['x'] = -2
                snakevel['y'] = 0
                label = 3
      #  bodycoordinate[0] = {
     #       'x': playerx,
      #      'y': playery
        if Eaten(applecoordinate,playerx,playery):
            game_sound['point'].play()
            applecoordinate = getapple()
            T1 = time.time()
            score+=1
            bodycoordinate.append({})
            add = 2
            if score % 5 == 0:
                fps += 10
                if timediff > 3:
                  timediff -= 1

        if len(bodycoordinate)>1:
            for i in range(len(bodycoordinate) - 1, 0, -1):
                bodycoordinate[i]['x'] = bodycoordinate[i - 1]['x']
                bodycoordinate[i]['y'] = bodycoordinate[i - 1]['y']
        playerx += snakevel['x']
        playery += snakevel['y']
        screen.fill(LIGHT_PURPLE)
       # screen.blit(game_sprites['background'],(0,0))
        screen.blit(game_sprites['player'][label],(playerx,playery))
       # screen.blit(game_sprites['obstacle'],(200,200))
        if label == 0:
            bodycoordinate[0]['x']= playerx - 18
            bodycoordinate[0]['y']= playery - 25 
            screen.blit(pygame.image.load(body).convert_alpha(),(bodycoordinate[0]['x'],bodycoordinate[0]['y']))
        if label == 1:
            bodycoordinate[0]['x']= playerx - 18
            bodycoordinate[0]['y']= playery + 22
            screen.blit(pygame.image.load(body).convert_alpha(),(bodycoordinate[0]['x'],bodycoordinate[0]['y']))
        if label ==2:
            bodycoordinate[0]['x']= playerx - 42.5
            bodycoordinate[0]['y']= playery
            screen.blit(pygame.image.load(body).convert_alpha(),(bodycoordinate[0]['x'],bodycoordinate[0]['y']))
        if label ==3:
            bodycoordinate[0]['x']= playerx + 5
            bodycoordinate[0]['y']= playery
            screen.blit(pygame.image.load(body).convert_alpha(),(bodycoordinate[0]['x'],bodycoordinate[0]['y']))

        screen.blit(pygame.image.load('img/apples.png').convert_alpha(),(applecoordinate[0],applecoordinate[1]))
        if time.time() - T1 > timediff:
            game_sound['teleport'].play()
            applecoordinate = getapple()
            T1 = time.time()
        if isCollide(playerx,playery,bodycoordinate,obs):
            game_sound['losing'].play()
            time.sleep(2)
            return
        digits = displayscore(score)
        screen.blit(game_sprites['number'][digits[0]],(screenWdith/2-20,20))
        if len(digits) >= 2:
            screen.blit(game_sprites['number'][digits[1]],(screenWdith/2 +5,20))
        if len(digits) >= 3:
            screen.blit(game_sprites['number'][digits[2]],(screenWdith/2+30,20))


        if len(bodycoordinate)>1:
            for i in range(0,len(bodycoordinate)):
                screen.blit(pygame.image.load(body).convert_alpha(),(bodycoordinate[i]['x'],bodycoordinate[i]['y']))
        if add>0:
            bodycoordinate.append({})
            add -=1

        if (time.time() - T1obs) > 15:
            T1obs = time.time()
            game_sound['obstacle'].play()
            if len(obs) < 10:
                obs.append(getapple())
                obs.append(getapple())
                obs.append(getapple())
            else:
                for i in range(1,len(obs)):
                    obs[i] = getapple()

        if len(obs)>1:
            for i in range(1,len(obs)):
                screen.blit(game_sprites['obstacle'],(obs[i][0],obs[i][1]))

        pygame.display.update()
        fpsclock.tick(fps)

def getapple():
    applex = random.randint(10,screenWdith-30)
    appley = random.randint(10,screenHeight-30) 
    apple = [applex,appley]
    return  apple

def Eaten(applecoordinate,playerx,playery):
    for i in range(applecoordinate[0]-12,applecoordinate[0]+12):
        if i == playerx:
            for j in range(applecoordinate[1]-8,applecoordinate[1]+8):
                if j == playery:
                    return True
def isCollide(playerx,playery,bodycordinate,obs):
    if playery <= 1 or playery >= screenHeight -25 or playerx <= 1 or playerx >= screenWdith -25:
        return True 
    if len(bodycordinate)>1: 
        for i in range(1,len(bodycordinate)):
            if playerx in range(int(bodycordinate[i]['x'])-2,int(bodycordinate[i]['x'])+2) and playery in range(int(bodycordinate[i]['y'])-2,int(bodycordinate[i]['y'])+2):
                return True
    for i in range(1,len(obs)):
        if playerx in range(obs[i][0]-5,obs[i][0]+5) and playery in range(obs[i][1]-5,obs[i][1]+5):
            return True
def displayscore(score):
    digits = []
    if score > 0:
        while score > 0:
            tmp = score % 10
            digits.append(tmp)
            score = score // 10
        digits.reverse()
    else:
        digits.append(0)
    return digits
    

if __name__ == "__main__":
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("SAURAV SUBEDI")
    game_sprites['number'] = (
        pygame.image.load('img/0.png').convert_alpha(),
        pygame.image.load('img/1.png').convert_alpha(),
        pygame.image.load('img/2.png').convert_alpha(),
        pygame.image.load('img/3.png').convert_alpha(),
        pygame.image.load('img/4.png').convert_alpha(),
        pygame.image.load('img/5.png').convert_alpha(),
        pygame.image.load('img/6.png').convert_alpha(),
        pygame.image.load('img/7.png').convert_alpha(),
        pygame.image.load('img/8.png').convert_alpha(),
        pygame.image.load('img/9.png').convert_alpha(),
    )

    game_sprites['message'] = pygame.image.load(message).convert_alpha()
    game_sprites['welcome'] = pygame.image.load(welcome).convert_alpha()
    game_sprites['background'] = pygame.image.load(background).convert_alpha()
    game_sprites['obstacle'] = pygame.image.load('img/obstacle.png').convert_alpha()
    game_sprites['player'] = (
        pygame.image.load(player).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(player),180),
        pygame.transform.rotate(pygame.image.load(player),90),
        pygame.transform.rotate(pygame.image.load(player),-90)
    )
    game_sound['point'] = pygame.mixer.Sound('sound/point.wav')
    game_sound['losing'] = pygame.mixer.Sound('sound/losing.wav')
    game_sound['intro'] = pygame.mixer.Sound('sound/intro.wav')
    game_sound['teleport'] = pygame.mixer.Sound('sound/teleport.mp3')
    game_sound['obstacle'] = pygame.mixer.Sound('sound/obstacle.mp3')
    while True:
        welcomescreen()
        maingame()
