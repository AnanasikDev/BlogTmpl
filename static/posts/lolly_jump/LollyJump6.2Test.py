#====BEGIN====

#====LIBS====

import pygame
import sys
import random
import time
import math

#----VARS----

sc_w = 1200          # screen width  [first argument]
sc_h = 1000          # screen height [second argument]
FPS = 60

move_right = False
move_left = False
counter = 0
lvl = 0
state_left = 2
state_right = 4
money_boost = 0
money_upgrade = 10

#----RGB----
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
WHITE = [255,255,255]
BLACK = [0,0,0]
PINK = [255, 130, 130]
LIGHT_BLUE = [0, 255,255]
YELLOW = [255,255,0]
PURPURE = [255,0,255]
ORANGE_CARROT = [255, 100, 0]
ORANGE_ORANGE = [255, 130, 0]
GREY = [100, 100, 100]
GREY_2 = [127, 127, 127]
#----------MAIN----------

#settings
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode([sc_w, sc_h])
screen.fill(WHITE)
pygame.display.set_caption('Lolly Jump!')
land = pygame.image.load('LollyLand1.png')
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)
screen.blit(land, [0, 832])
Score_color = BLACK
pygame.display.flip()

#FPS

clock = pygame.time.Clock()

#Spawner's cords

box_cord = (0, 35, 89, 130, 189, 290, 333, 379, 458, 500, 545, 610, 686, 743, 799, 843, 900, 964)
coin_cord = [121]

#Таблица рекордов

scores = open('Scores.txt', 'r+', encoding='UTF-8')
result = []
for line in scores:
    number = line.strip()
    result.append(int(number))
    
#Звуки, музыка

pygame.mixer.music.load('background.mp3')
break_down_sound = pygame.mixer.Sound('Break_down.wav') #Звук ломания коробки
get_coin = pygame.mixer.Sound('get_coin.wav') #Звук получения монеты
pygame.mixer.music.set_volume(0.01)
break_down_sound.set_volume(0.125)
get_coin.set_volume(0.5)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.image_num = 0
        self.image_file = 'LollyPlayer' + str(self.image_num) + '.png'
        self.image = pygame.image.load(self.image_file)
        
    def draw(self):
        screen.blit(self.image, [self.x, self.y])
        pygame.display.flip()
        
#Движение        
    def move(self):                             
        if self.x < 1200-32 and self.x > 0:            
            self.x += self.speed 
        elif self.x >= 1200-32:
            self.x = 1200-33
        elif self.x <= 0:
            self.x = 1     
        if self.speed == abs(self.speed):
            pygame.draw.rect(screen, WHITE, [self.x-11, self.y, 10, 29], 0)
        elif self.speed != abs(self.speed):
            pygame.draw.rect(screen, WHITE, [self.x+21, self.y, 10, 29], 0)              
    
class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image_num = 4
        self.image_file = 'LollyBox' + str(self.image_num) + '.png'
        self.image = pygame.image.load(self.image_file)
        
    def draw(self):
        screen.blit(self.image, [self.x, self.y])
        pygame.display.flip()
        
    def move(self):
        self.y += self.speed
        pygame.draw.rect(screen, WHITE, [self.x, self.y-(26+self.speed), 32, 22+self.speed], 0)

class Coin:
    def __init__(self, x, y, speed, wait, append, boost):
        self.x = x
        self.y = y
        self.speed = speed
        self.wait = wait
        self.append = append
        self.boost = boost
        self.image_num = chance(50, 35, 15)
        self.image_file = 'LollyMoney' + str(self.image_num) + '.png'
        self.image = pygame.image.load(self.image_file)
        
    def draw(self):
        screen.blit(self.image, [self.x, self.y])
        pygame.display.flip()
        
    def move(self):
        self.y += self.speed
        pygame.draw.rect(screen, WHITE, [self.x, self.y-(self.speed*2), 16, self.speed], 0)    
        
    def despawn(self):
        pygame.draw.rect(screen, WHITE, [self.x, self.y-10, 16, 26], 0)
        
class Button:
    def __init__(self, x, y, img_num, cost):
        self.x = x
        self.y = y
        self.img_num = img_num
        self.cost = cost
        self.img_file = 'LollyButtonShop' + str(self.img_num) + '.png'
        self.img = pygame.image.load(self.img_file)
        self.img.set_colorkey(WHITE)
        self.img = pygame.transform.scale(self.img, [80, 120])
        
    def draw(self):
        screen.blit(self.img, [self.x, self.y-70])
        pygame.display.flip()
        
def move_right_wh(move_right):
    if move_right == True:
        player.speed = abs(player.speed)
        for i in range(20):
            player.draw()
            player.move()
            
def move_left_wh(move_left):
    if move_left == True:
        player.speed = -abs(player.speed)
        for i in range(20):
            player.draw()
            player.move()  
            
def chance(a, b, c):
    if a+b+c != 100:
        pygame.quit()
        print('VolumeError: sum of chances must be 100.')
    results = []
    for i in range(a):
        results.append(0)
    for i in range(b):
        results.append(1)
    for i in range(c):
        results.append(2)   
    rand_index = random.randint(0, len(results)-1)
    return(results[rand_index])
    
            
def animate(image_num):
    player.image_num = image_num
    player.image_file = 'LollyPlayer' + str(player.image_num) + '.png'
    player.image = pygame.image.load(player.image_file)
    player.draw()    

def change_money():
    mon.image_num = chance(50, 35, 15)
    mon.image_file = 'LollyMoney' + str(mon.image_num) + '.png'
    mon.image = pygame.image.load(mon.image_file)
    mon.draw()
    
def write(message, x, y, length, height, size, back_color, color, font_type = '18177.otf'):
    #screen.blit(land, [0, 832])
    pygame.draw.rect(screen, back_color, [x, y, length, height], 0)
    font_type = pygame.font.Font(font_type, size)
    text = font_type.render(message, True, color)
    screen.blit(text, [x, y])
    
#def boost_btn_clicked(coins):
#    for mon in coins:
#        mon.boost += 1000
    
mobs = []            
for i in range(0, 26):
    if i <= len(box_cord)-1:
        xx = box_cord[i]
        yy = random.randint(-5600, -200)
        box = Box(xx, yy)
        mobs.append(box)
    else:
        i = 0
    
coins = []
for i in range(2):
    coin_y = random.randint(-2300, -100)
    coin_speed = random.randint(2, 7)
    coin = Coin(coin_cord[0], coin_y, coin_speed, 0, True, money_boost)
    coins.append(coin)
    
bts = [] #Buttons
for i in range(1):
    btn = Button(10, 1000-48, 0, round(500/1.5*(lvl+1)))
    bts.append(btn)
    
#Мобы    
player = Player(600, 803)           
player.draw()    
#Включаем музыку
pygame.mixer.music.play(-1)

while True:
    player.draw()
    #screen.blit(land, [0, 832]) 
    #Отрисовываем очки, лвл, фпс
    
    write("Score: " + str(counter//2), 500, 100, 200, 30, 35, WHITE, Score_color)
    write("Lvl: " + str(lvl), 10, 100, 100, 30, 30, WHITE, BLACK)
    #write("fps: " + str(FPS), 1080, 960, 25, WHITE, BLACK)
    write('Best: ' + str(max(result)), 515, 60, 200, 25, 25, WHITE, BLACK)
    write('+%s' % (str(money_boost)), 20, 1000-55, 50, 20, 15, GREY_2, WHITE)
    write('%s' % (str(btn.cost)), 20, 1000-30, 50, 20, 15, GREY_2, WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            counter = str(counter//2)
            scores.write('\n')
            scores.write(counter)
            scores.close()               
            pygame.quit()   
         
        #Управление   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                animate(1)
                move_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                animate(0)
                move_right = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                animate(1)
                move_left = False                 
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                animate(0)
                move_right = False  
                
        #Магазин и кнопки
        if event.type == pygame.MOUSEBUTTONDOWN:
            curs_cords = pygame.mouse.get_pos()
            if event.button == 1:
                if curs_cords[0] >= 10 and curs_cords[0] <= 90:
                    if curs_cords[1] >= 1000-120 and curs_cords[1] <= 1000:
                        if counter >= btn.cost*2:
                            #boost_btn_clicked(coins)
                            counter -= round(btn.cost*2)
                            money_boost += money_upgrade
                            up_grade_ran = random.randint(0, 2)
                            if up_grade_ran == 1:
                                money_upgrade += random.randint(1, 5)
                            btn.cost += round(100*0.75*lvl)
                           #print('clicked')
                
                
    if move_left:
        player.speed = -abs(player.speed)
        for sp in range(20):
            player.draw()
            player.move()
            if sp % 20 == 0.0:
                counter += 1
                animate(state_left)
                if state_left < 3:
                    state_left += 1
                else:
                    state_left = 2
                    
            if sp % 10 == 0:
                for mob in mobs:
                    mob.draw()
                    mob.move()
                    if mob.y >= 800:               
                        pygame.draw.rect(screen, WHITE, [mob.x, mob.y-5, 32, 32], 0)
                        coin = Coin(mob.x, mob.y+16, 0, 0, False, money_boost)
                        coin.draw()
                        coin.speed = 0
                        coins.append(coin)
                        cord_y = random.randint(-4000, -200)
                        mob.y = cord_y
                        mob.draw()
                        
                    if mob.y >= 790:
                        pygame.mixer.Sound.play(break_down_sound)
                        
                    if player.y <= mob.y+32: 
                        #if player.x >= mob.x and player.x + 32 <= mob.x+32:
                        for i in range(-32, 21):
                            if player.x + i == mob.x:
                                counter = str(counter//2)
                                scores.write('\n')
                                scores.write(counter)
                                if player.speed == abs(player.speed):
                                    animate(6)
                                elif player.speed != abs(player.speed):
                                    animate(7)
                                scores.close()                        
                                pygame.quit()                    
                        
                
        
    if move_right:
        player.speed = abs(player.speed)
        for sp in range(20):
            player.draw()
            player.move() 
            if sp % 20 == 0.0:
                counter += 1
                animate(state_right)
                if state_right < 5:
                    state_right += 1
                else:
                    state_right = 4    
                    
            if sp % 10 == 0:
                for mob in mobs:
                    mob.draw()
                    mob.move()
                    if mob.y >= 800:               
                        pygame.draw.rect(screen, WHITE, [mob.x, mob.y-5, 32, 32], 0)
                        coin = Coin(mob.x, mob.y+16, 0, 0, False, money_boost)
                        coin.draw()
                        coin.speed = 0
                        coins.append(coin)
                        cord_y = random.randint(-4000, -200)
                        mob.y = cord_y
                        mob.draw()
                        
                    if mob.y >= 790:
                        pygame.mixer.Sound.play(break_down_sound)
                        
                    if player.y <= mob.y+32: 
                        #if player.x >= mob.x and player.x + 32 <= mob.x+32:
                        for i in range(-32, 21):
                            if player.x + i == mob.x:
                                counter = str(counter//2)
                                scores.write('\n')
                                scores.write(counter)
                                if player.speed == abs(player.speed):
                                    animate(6)
                                elif player.speed != abs(player.speed):
                                    animate(7)                                
                                scores.close()                        
                                pygame.quit()                    
            
    if counter % 1 == 0 and counter != 0:
        for mob in mobs:
            mob.draw()
            mob.move()
            if mob.y >= 800:               
                pygame.draw.rect(screen, WHITE, [mob.x, mob.y-5, 32, 32], 0)
                coin = Coin(mob.x, mob.y+16, 0, 0, False, money_boost)
                coin.draw()
                coin.speed = 0
                coins.append(coin)
                cord_y = random.randint(-4000, -200)
                mob.y = cord_y
                mob.draw()
                
            if mob.y >= 790:
                pygame.mixer.Sound.play(break_down_sound)
                
            if player.y <= mob.y+32: 
                #if player.x >= mob.x and player.x + 32 <= mob.x+32:
                for i in range(-32, 21):
                    if player.x + i == mob.x:
                        counter = str(counter//2)
                        scores.write('\n')
                        scores.write(counter)
                        if player.speed == abs(player.speed):
                            animate(6)
                        elif player.speed != abs(player.speed):
                            animate(7)
                        scores.close()                        
                        pygame.quit()
                        
                        
        for mon in coins:
            mon.draw()
            mon.move()
            if mon.y >= 815:
                mon.speed = 0
            
            if player.y <= mon.y+16:
                for i in range(-16, 16):
                    if player.x + i == mon.x:
                        if mon.append == True:
                            mon.despawn()
                            pygame.mixer.Sound.play(get_coin)
                            mon.y = random.randint(-5000, -1000)
                            change_money()
                            if mon.image_num == 0:
                                counter += 100+mon.boost
                            if mon.image_num == 1:
                                counter += 175+mon.boost
                            if mon.image_num == 2:
                                counter += 250+mon.boost
                        else:
                            if mon.image_num == 0:
                                counter += 100+mon.boost
                            if mon.image_num == 1:
                                counter += 175+mon.boost
                            if mon.image_num == 2:
                                counter += 250+mon.boost
                                
                            mon.despawn()
                            mon.speed = 0
                            mon.x = 2000
                            mon.draw()
                            
            
            if mon.y >= 815:
                mon.wait += 1
                
                
            if mon.wait % 100 == 0:
                mon.despawn()
                mon.y = random.randint(-5000, -1000)
                mon.draw()
                
        for button in bts:
            screen.blit(land, [0, 832])
            button.draw()
    
                        
    lvl = (counter//2)//500    
    pygame.display.flip()
    #Очки
    counter += 1
    clock.tick(FPS)
    
