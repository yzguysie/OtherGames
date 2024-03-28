
import pygame
from pygame import gfxdraw
pygame.init()
import random
import math


width, height = 1280, 720
fps = 20


window = pygame.display.set_mode([width, height])
pygame.display.set_caption("Evolution sim")



white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
light_gray = (192, 192, 192)
dark_gray = (64, 64, 64)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

BACKGROUND_COLOR = (black)
clock = pygame.time.Clock()



class Blob():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.sense = 50
        self.target = None
        self.speed = 2
        self.energy = 1
        self.xspeed = 0
        self.yspeed = 0
        self.wait_time = 1.25
        self.color = (127, 127, 127)

    def tick(self):
        self.draw()
        if self.energy > 0 and self.wait_time <= 0:
            self.target = self.get_nearest_food()
            self.move()
            self.energy -= .1*((self.speed/5)**2)/fps + .1*(self.sense/75)/fps

        self.wait_time -= 1/fps
        if len(blobs)*len(foods) < 10000:
            
            for food in foods:
                if self.is_touching(food) and food not in foods_to_delete:
                    self.consume(food)
        else:
            if self.target != None and self.is_touching(self.target) and self.target not in foods_to_delete:
                self.consume(self.target)
        if self.energy >= 2:
            self.replicate()
        if self.energy <= 0:
            blobs_to_delete.add(self)

        if self.x > width:
            self.xspeed *= -1
            self.x = width

        if self.x < 0:
            self.xspeed *= -1
            self.x = 0

        if self.y > height:
            self.yspeed *= -1
            self.y = height

        if self.y < 0:
            self.yspeed *= -1
            self.y = 0

        

    def draw(self):
        pygame.gfxdraw.filled_circle(window, round(self.x), round(self.y), round(self.size), (self.color[0]*min(1, self.energy), self.color[1]*min(1, self.energy), self.color[2]*min(1, self.energy)))
        pygame.gfxdraw.circle(window, round(self.x), round(self.y), round(self.sense), (self.color[0]*min(1, self.energy), self.color[1]*min(1, self.energy), self.color[2]*min(1, self.energy)))

    def get_nearest_food(self):
        lowest = None
        lowest_distance = -1
        for blob in blobs:
            if self.size > blob.size*1.2:
                distance = (blob.x-self.x)**2+(blob.y-self.y)**2
                if distance < self.sense**2:
                    if lowest == None or distance < lowest_distance:
                        lowest = blob
                        lowest_distance = distance
        if lowest != None:
            return lowest
                    
        for food in foods:
            distance = (food.x-self.x)**2+(food.y-self.y)**2
            if (food.x-self.x)**2+(food.y-self.y)**2 < self.sense**2:
                if lowest == None or distance < lowest_distance:
                    lowest = food
                    lowest_distance = distance
        return lowest

    def is_touching(self, target):
        return (self.x-target.x)**2+(self.y-target.y)**2 <= self.size**2+target.size**2
    def replicate(self):
        color_diff = 50
        self.energy -= 1
        child = Blob(self.x+5, self.y-5)
        child.speed = self.speed*random.uniform(.8, 1.25)
        child.sense = self.sense*random.uniform(.8, 1.25)
        child.color = (max(0, min(255, self.color[0]+random.randint(-color_diff, color_diff))), max(0, min(255, self.color[1]+random.randint(-color_diff, color_diff))), max(0, min(255, self.color[2]+random.randint(-color_diff, color_diff))))
        #child.size = self.size*random.uniform(.8, 1.25)
        
        blobs.append(child)

    def consume(self, food):
        self.energy += food.energy
        self.wait_time = .25
        foods_to_delete.add(food)
        
    def move(self):
        if self.target == None:
            if self.xspeed > self.speed or self.xspeed < -self.speed:
                self.xspeed = 0

            if self.yspeed > self.speed or self.yspeed < -self.speed:
                self.yspeed = 0
            self.xspeed += random.uniform(round(-self.speed/3), round(self.speed/3))
            self.yspeed += random.uniform(round(-self.speed/3), round(self.speed/3))
            xdiff = (self.xspeed)*10
            ydiff = (self.yspeed)*10

        else:
            xdiff = self.target.x-int(self.x+.5)
            ydiff = self.target.y-int(self.y+.5)
           
            self.xspeed = (xdiff)
            self.yspeed = (ydiff)

        total_speed = (abs(self.xspeed)**2+abs(self.yspeed)**2)**(1/2)
        if self.xspeed**2+self.yspeed**2 > self.speed**2 or xdiff**2+ydiff**2>self.size**2:
                percent_x = self.xspeed/total_speed
                percent_y = self.yspeed/total_speed

               
                       
               
                self.xspeed = self.speed*percent_x
                self.yspeed = self.speed*percent_y
                """
                amount = 3
                if xdiff < self.speed*amount:
                    self.xspeed = xdiff/amount
                if ydiff < self.speed*amount:
                    self.yspeed = ydiff/amount
                if xdiff > -self.speed*amount:
                    self.xspeed = -xdiff/amount
                if ydiff > -self.speed*amount:
                    self.yspeed = -ydiff/amount

                """
       
       
        self.x += (self.xspeed)/self.size**(1/2)/fps*60
        self.y += (self.yspeed)/self.size**(1/2)/fps*60
        

class Food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 3
        self.energy = (self.size/5)*(self.size/5)

    def tick(self):
        self.draw()
        pass
    def draw(self):
        pygame.gfxdraw.filled_circle(window, round(self.x), round(self.y), self.size, green)
    

font = 'arial'
font_width = int(width/100+1)

dialogue_font = pygame.font.SysFont(font, font_width)
    
blobs_to_delete = set()
blobs = []
blobs.append(Blob(width/2, height/2))
foods_to_delete = set()

foods = []
for i in range(50):
    foods.append(Food(random.randint(0, width), random.randint(0, height)))

frames = 0
playing = True
while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break

            if event.key == pygame.K_SPACE:
                blobs.append(Blob(random.randint(0, width), random.randint(0, height)))


    window.fill(BACKGROUND_COLOR)
    food_spawn_rate = (7500/(240+frames/fps))
    for blob in blobs:
        blob.tick()

    for food in foods:
        food.tick()
        
    if round(fps/food_spawn_rate) == 0 or frames % round(fps/food_spawn_rate) == 0:
        if round(fps/food_spawn_rate) == 0:
            for i in range(round(1/(fps/food_spawn_rate))):
                foods.append(Food(random.randint(0, width), random.randint(0, height)))
        else:
            foods.append(Food(random.randint(0, width), random.randint(0, height)))
        
        pass
    
    if len(blobs) > 0:
        total = 0
        for blob in blobs:
            total += blob.speed
        average_speed = total/len(blobs)

        total = 0
        for blob in blobs:
            total += blob.sense
        average_sense = total/len(blobs)

        total = 0
        for blob in blobs:
            total += blob.size
        average_size = total/len(blobs)
        
        
        dialogue = dialogue_font.render("average sense: " + str(average_sense), True, white)
        window.blit(dialogue, (0, 50))
        dialogue = dialogue_font.render("average speed: " + str(average_speed), True, white)
        window.blit(dialogue, (0, 25))
        dialogue = dialogue_font.render("average size: " + str(average_size), True, white)
        window.blit(dialogue, (0, 75))
        
    dialogue = dialogue_font.render("population: " + str(len(blobs)), True, white)
    window.blit(dialogue, (0, 0))

    dialogue = dialogue_font.render("food spawn rate: " + str(food_spawn_rate), True, white)
    window.blit(dialogue, (0, 100))
    blobs = [blob for blob in blobs if blob not in blobs_to_delete]
    foods = [food for food in foods if food not in foods_to_delete]

    pygame.display.flip()
    clock.tick(fps)

    frames += 1

pygame.quit()
