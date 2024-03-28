import pygame
from pygame import gfxdraw
import random
import time
import math
pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode([width, height])

friction = .5
class Ball():
    
    def __init__(self, x, y, xspeed, yspeed, size, color):
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.size = size
        self.color = color

    

    def draw(self):
        
        pygame.gfxdraw.filled_circle(window, round(self.x), round(self.y), self.size, self.color)
        pygame.gfxdraw.aacircle(window, round(self.x), round(self.y), self.size, self.color)
    def check_bounce(self):
        if self.x > width-self.size:
            self.x = width-self.size
            self.xspeed *= -.7
        if self.x < 0+self.size:
            self.x = 0+self.size
            self.xspeed *= -.7
        if self.y > height-self.size:
            self.y = height-self.size
            self.yspeed *= -.7
        if self.y < 0+self.size:
            self.y = 0+self.size
            self.yspeed *= -.7


amount_size = 14
amount = amount_size*1.4
def make_balls(rows, start):
    rows += 1
    for i in range(rows):
        for j in range(i):
            balls.append(Ball(width/2+amount*(i-j*2-1), start-amount*i*math.sqrt(2), 0, 0, amount_size, (128, 128, 128)))
            
balls = [Ball(width/2, height/2+height/4, 0, 0, amount_size*2, (255, 255, 255)),]

make_balls(10, height/2)

"""ball(width/2, height/2-height/4, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2-amount, height/2-height/4-amount, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2+amount, height/2-height/4-amount, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2-amount*2, height/2-height/4-amount*2, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2+amount*2, height/2-height/4-amount*2, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2, height/2-height/4-amount*2, 0, 0, amount_size, (128, 128, 128)),
         
         ball(width/2+amount*3, height/2-height/4-amount*3, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2+amount, height/2-height/4-amount*3, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2-amount, height/2-height/4-amount*3, 0, 0, amount_size, (128, 128, 128)),
         ball(width/2-amount*3, height/2-height/4-amount*3, 0, 0, amount_size, (128, 128, 128)),
"""



def check_colliding(self, other):
    if (self.x-other.x)**2+(self.y-other.y)**2 < (self.size+other.size)**2:

        firstx = self.xspeed
        firsty = self.yspeed
        secx = other.xspeed
        secy = other.yspeed

        angle = math.atan2(self.y - other.y, self.x - other.x)
        vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        amount = 1
        percent_given = .5
        percent_saved = .5


        # self.xspeed = (math.sqrt((secx*percent_given+firstx*percent_saved)**2+(secy*percent_given+firsty*percent_saved)**2))*vector[0]/amount*(random.randint(9990, 10010)/10000)
        # self.yspeed = (math.sqrt((secx*percent_given+firstx*percent_saved)**2+(secy*percent_given+firsty*percent_saved)**2))*vector[1]/amount*(random.randint(9990, 10010)/10000)
        # other.xspeed = (math.sqrt((secx*percent_saved+firstx*percent_given)**2+(secy*.25+firsty*percent_given)**2))*-vector[0]/amount*(random.randint(9990, 10010)/10000)
        # other.yspeed = (math.sqrt((secx*percent_saved+firstx*percent_given)**2+(secy*.25+firsty*percent_given)**2))*-vector[1]/amount*(random.randint(9990, 10010)/10000)

        diffx = abs(firstx-secx)
        diffy = abs(firsty-secy)
        self.xspeed += diffx*vector[0]
        self.yspeed += diffy*vector[1]
        other.xspeed -= diffx*vector[0]
        other.yspeed -= diffy*vector[1]
        #self.xspeed, other.xspeed = secx*.75+firstx*.25, firstx*.75+secx*.25
        #self.yspeed, other.yspeed = secy*.75+firsty*.25, firsty*.75+secy*.25
        while (self.x-other.x)**2+(self.y-other.y)**2 < (self.size+other.size)**2 and self.xspeed+self.yspeed+other.xspeed+other.yspeed > 0.0001:
            
            self.x += self.xspeed/fps/20
            self.y += self.yspeed/fps/20
            other.x += other.xspeed/fps/20
            other.y += other.yspeed/fps/20
            #print("YAP")
        
        


def draw_balls():
    for ball in balls:
        ball.draw()

def tick_balls():
    
    for ball in balls:
        ball.x += ball.xspeed/fps
        ball.y += ball.yspeed/fps
        ball.xspeed /= (1 + friction/fps)
        ball.yspeed /= (1 + friction/fps)
        if abs(ball.xspeed+ball.yspeed) <= 1:
            ball.xspeed, ball.yspeed = 0, 0
        ball.check_bounce()
    all_pair(balls, check_colliding)

def all_pair(items, func):

    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            func(items[i], items[j])
        
        



clock = pygame.time.Clock()
fps = 60

playing = True
while playing:

    window.fill((0,0,0))
    amount = 50
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            playing = False
            break
       
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break

        
    if pygame.key.get_pressed()[pygame.K_UP]:
        balls[0].yspeed -= amount

    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        balls[0].yspeed += amount

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        balls[0].xspeed += amount

    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        balls[0].xspeed -= amount
                
    tick_balls()
    draw_balls()
    pygame.display.flip()
    clock.tick(fps)
            

pygame.quit()
