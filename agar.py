import pygame
import pygame.gfxdraw
pygame.init()
import math
import random
import time





from configparser import ConfigParser

config = ConfigParser()
"""
# parse existing file
config.read('2D Universe Sandbox.ini')

# read values from a section
fps = config.getint('engine', 'fps')
tickrate = config.getint('engine', 'tickrate')
scale = config.getint('engine', 'scale')
trail_update_rate = config.getint('engine', 'trail_update_rate')
settings_preset = config.getint('engine', 'settings_preset')
# update existing value
"""

width, height = 1280, 720
speed = 10
fps = 60

target_scale = 105

scale = 1
aa_agar = True
decay_rate = 0.01
recombine_time = 10
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

yellow = (255, 255, 0)
idk = (255, 0, 255)
idk2 = (0, 255, 255)
brown = (139,69,19)

gray = (128, 128, 128)
dark_gray = (64, 64, 64)
light_gray = (192, 192, 192)
light_blue = (102, 178, 255)
dark_blue = (0, 0, 192)
background_color = black
font_color = green

agar_to_delete = set()
cells_to_delete = set()

camera_x = 0
camera_y = 0

cell_id = 0
agar_id = 0
ejected_id = 0
virus_id = 0
frames = 0
ejected_size = 13
ejected_loss = 15
eject_min_mass = 43
split_min_mass = 43
player_min_mass = 9
ejected_speed = 7
player_speed = 3
player_start_mass = 43
bot_start_mass = 10
player_max_cells = 32
font = 'arial'
font_width = int(width/100+1)
dialogue_font = pygame.font.SysFont(font, font_width)
brown_virus_mass = 200
brown_virus_id = 1

pygame.display.set_caption("Agar.io Clone")

smoothness = 15



def calc_center_of_mass(bodies):
        center_x = 0
        center_y = 0
        weight = 0
        for body_ in bodies:
            center_x += body_.x*body_.mass
            center_y += body_.y*body_.mass
            weight += body_.mass
        return (center_x/weight, center_y/weight)


   
class Cell:
   
    def __init__(self, x, y, mass, color, player):
        global cell_id
        global camera_x
        global camera_y

        self.extraxspeed = 0
        self.extrayspeed = 0
        self.max_speed = 100
        self.x = x
        self.y = y
        self.xspeed = 0
        self.yspeed = 0
        self.inertia = 5
        self.mass = mass
        self.radius = mass**(1/2)
        self.smoothradius = self.radius
        self.color = color
        self.player = player
        self.id = cell_id
        if self.player != 0:
                self.target = Cell(1000, 1000, player_start_mass, green, 0)

        cell_id += 1
        self.time_created = time.time()

    def draw(self):
        global camera_x
        global camera_y
       

        self.radius = self.mass**(1/2)
        self.smoothradius += (self.radius - self.smoothradius)/smoothness
       

        #print(self.smoothradius)
        pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(abs(self.smoothradius/scale+.5)), self.color)

        #pygame.draw.circle(window, (self.color[0]/1.25,self.color[1]/1.25, self.color[2]/1.25), (int(self.x/scale-camera_x+.75), int(self.y/scale-camera_y+.75)), int(self.radius/scale+.5), width=int(self.radius/scale/20+1))
   
       
        pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(abs(self.smoothradius/scale+.5)), (self.color[0]/1.25,self.color[1]/1.25, self.color[2]/1.25))
        pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(abs(self.smoothradius/scale-.5)), (self.color[0]/1.25,self.color[1]/1.25, self.color[2]/1.25))

    def move(self):
        if self.player == 0:
                x, y = pygame.mouse.get_pos()

                xdiff = x-int(self.x/scale-camera_x+.5)
                ydiff = y-int(self.y/scale-camera_y+.5)

                angle = math.atan2(ydiff, xdiff)
                vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
                velocity = min(self.max_speed, math.sqrt(xdiff**2+ydiff**2))
                self.xspeed = velocity*vector[0]/fps
                self.yspeed = velocity*vector[1]/fps
                # if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                        
                #         self.xspeed += (xforce)/fps
                #         self.yspeed += (yforce)/fps
                # else:
                #         self.xspeed = (self.xspeed*self.inertia)+(xforce)/fps_
                #         self.yspeed = (self.yspeed*self.inertia)+(yforce)/fps_


        else:
                x, y = self.target.x, self.target.y

                xdiff = x-self.x
                ydiff = y-self.y
                if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                        self.xspeed = (xdiff)/fps*10
                        self.yspeed = (ydiff)/fps*10
                else:
                        self.xspeed = (xdiff)/fps_*10
                        self.yspeed = (ydiff)/fps_*10


        # total_speed = (abs(self.xspeed)**2+abs(self.yspeed)**2)**(1/2)
        # if self.xspeed**2+self.yspeed**2 > player_speed**2 or xdiff**2+ydiff**2>self.radius**2:
        #         percent_x = self.xspeed/total_speed
        #         percent_y = self.yspeed/total_speed

               
                       
               
        #         self.xspeed = player_speed*percent_x
        #         self.yspeed = player_speed*percent_y
       
       
       
        self.x += (self.xspeed+self.extraxspeed)/self.radius**(1/2)
        self.y += (self.yspeed+self.extrayspeed)/self.radius**(1/2)

        if self.x > border_width:
            self.x = border_width
        if self.x < -border_width:
            self.x = -border_width

        if self.y > border_height:
            self.y = border_height
        if self.y < -border_height:
            self.y = -border_height

        self.extraxspeed /= 1.05
        self.extrayspeed /= 1.05

    def split(self):
        
        if len(players[self.player]) > player_max_cells:
                return
        self.mass = self.mass/2
        x, y = pygame.mouse.get_pos()
        cells.append(Cell(self.x+1, self.y+1, self.mass, self.color, self.player))
        if self.player == 0:
                if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                        extrax = (x-int(self.x/scale-camera_x+.5))/fps*1
                        extray = (y-int(self.y/scale-camera_y+.5))/fps*1
                else:
                        extrax = (x-int(self.x/scale-camera_x+.5))/fps_*1
                        extray = (y-int(self.y/scale-camera_y+.5))/fps_*1
        else:
                if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                        extrax = (self.target.x-self.x)/fps
                        extray = (self.target.y-self.y)/fps
                else:
                        extrax = (self.target.x-self.x)/fps_
                        extray = (self.target.y-self.y)/fps_


       
       
        total_speed = (abs(extrax)**2+abs(extray)**2)**(1/2)
       
        if extrax**2+extray**2 > player_speed**2:
                percent_x = extrax/total_speed
                percent_y = extray/total_speed

               
                       
               
                extrax = player_speed*percent_x
                extray = player_speed*percent_y

        cells[len(cells)-1].extraxspeed = extrax*cells[len(cells)-1].radius**(2/3)
        cells[len(cells)-1].extrayspeed = extray*cells[len(cells)-1].radius**(2/3)


    def tick(cells):
        pass
       
    def apply_physics(self):
        global camera_x
        global camera_y
        if self.mass > player_min_mass:
            if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                self.mass -= self.mass*decay_rate/fps
            else:
                self.mass -= self.mass*decay_rate/fps_  
       
       
               
        self.move()

       

        self.check_colliding(cells)
        self.check_viruses(brown_viruses)
        self.draw()
       
    def consume(self, agar):
        self.mass += agar.mass
        agar_to_delete.add(agar.id)

    def consume_ejected(self, ejected):
        self.mass += ejected.mass
        ejected_to_delete.add(ejected.id)


    def consume_virus(self, virus):
        self.mass += virus.mass
        viruses_to_delete.add(virus.id)
        while len(players[self.player]) < player_max_cells and self.mass > split_min_mass:
                self.split()
                players[self.player].append(cells[len(cells)-1])
                players[self.player][len(players[self.player])-1].time_created = time.time()-.5
                players[self.player][len(players[self.player])-1].extraxspeed = 0
                players[self.player][len(players[self.player])-1].extrayspeed = 0


    def consume_brown_virus(self, virus):
        self.mass += virus.mass
        brown_viruses_to_delete.add(virus.id)
        while len(players[self.player]) < player_max_cells and self.mass > split_min_mass:
                self.split()
                players[self.player].append(cells[len(cells)-1])
                players[self.player][len(players[self.player])-1].time_created = time.time()-.5
                players[self.player][len(players[self.player])-1].extraxspeed = 0
                players[self.player][len(players[self.player])-1].extrayspeed = 0    
               
   

    def check_viruses(self, viruses):
        for virus in viruses:
            if self.mass*1.3 < virus.mass:
                if (virus.x-self.x)**2+(virus.y-self.y)**2 < (virus.radius-self.radius/3)**2:
                    if self.id not in cells_to_delete and virus.id not in brown_viruses_to_delete:
                        virus.consume_cell(self)
            if self.mass > virus.mass*1.3:
                if (virus.x-self.x)**2+(virus.y-self.y)**2 < (self.radius-virus.radius/3)**2:
                    if self.id not in cells_to_delete and virus.id not in brown_viruses_to_delete:
                        self.consume_brown_virus(virus)

       
    def eject_mass(self):
        ejected.append(ejected_mass(self))

    def check_colliding(self, cells):
        global recombine_time

       
        for thing in players[self.player]:
           
            if thing.id != self.id:
                distance = ((thing.x-self.x)**2+(thing.y-self.y)**2)**(1/2)
                if distance < (thing.radius+self.radius):
                    if (time.time()-thing.time_created < recombine_time*(self.mass**(1/4)/4) or time.time()-self.time_created < recombine_time*(self.mass**(1/4)/4)) and thing.player == self.player:
                        if time.time()-thing.time_created > .5 and time.time()-self.time_created > .5:
                            count = 0
                            combined_radius_squared = (thing.radius+self.radius)**2
                            while (thing.x-self.x)**2+(thing.y-self.y)**2 < combined_radius_squared and count < 10:
                                xdiff = thing.x-self.x
                                ydiff = thing.y-self.y

                               
                                thing.x += (xdiff)/(thing.radius+self.radius)/3
                                thing.y += (ydiff)/(thing.radius+self.radius)/3
                                count += 1
                            if count >= 10:
                                pass
                    else:
                        if (thing.x-self.x)**2+(thing.y-self.y)**2 < (self.radius-thing.radius/3)**2:
                            if self.id not in cells_to_delete and thing.id not in cells_to_delete:
                                if self.player == thing.player:
                                        self.combine(thing)
                                else:
                                        if self.mass >= thing.mass*1.3 and distance < self.radius-thing.radius/4:
                                                self.combine(thing)
                                        elif thing.mass >= self.mass*1.3 and distance < thing.radius-self.radius/4:
                                                thing.combine(self)

        for thing in cells:
           
            if thing.player != self.player:
                distance = ((thing.x-self.x)**2+(thing.y-self.y)**2)**(1/2)
                if distance < (thing.radius+self.radius):
                            if self.id not in cells_to_delete and thing.id not in cells_to_delete:
                                if self.player == thing.player:
                                   
                                        self.combine(thing)
                                else:
                                        if self.mass >= thing.mass*1.3 and distance < self.radius-thing.radius/3:
                                                self.combine(thing)
                                        elif thing.mass >= self.mass*1.3 and distance < thing.radius-self.radius/3:
                                                thing.combine(self)
                           
    def combine(self, consumed):
        combined_mass = self.mass+consumed.mass
       
        #self.x = ((self.x*self.mass)+(consumed.x*consumed.mass))/combined_mass
        #self.y = ((self.y*self.mass)+(consumed.y*consumed.mass))/combined_mass
        self.mass += consumed.mass
        for i in range(len(cells)):
            if cells[i].id == consumed.id:
                cells_to_delete.add(consumed.id)
                break
                   
               

class agar:

    def __init__(self, x, y, mass, color):
        global agar_id
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = mass**(1/2)
        self.color = color
        self.id = agar_id
        agar_id += 1

    def draw(self):
        global camera_x
        global camera_y
        pygame.draw.circle(window, self.color, (self.x/scale-camera_x, self.y/scale-camera_y), self.radius/scale)

    def draw_high_quality(self):
        global camera_x
        global camera_y
        if self.x/scale-camera_x < -self.radius or self.y/scale-camera_y < -self.radius or self.x/scale-camera_x > width+self.radius or self.y/scale-camera_y > height+self.radius:
            return
       
        pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), self.color)
        pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))


    def check_colliding(self, cells):
        for thing in cells:
            if self.id not in agar_to_delete:
                if abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2:
                    thing.consume(self)


class ejected_mass:

    def __init__(self, cell):

        global camera_x
        global camera_y
        global ejected_size
        global ejected_loss
        global eject_min_size
        global ejected_id
        global ejected_speed

       
       
        cell.mass -= ejected_loss
        self.x = cell.x
        self.y = cell.y
        self.mass = ejected_size
        self.radius = ejected_size**(1/2)
        self.smoothradius = self.radius
        self.color = cell.color
        x, y = pygame.mouse.get_pos()
        x = x
        y = y
        
        self.xspeed = (x-int(cell.x/scale-camera_x+.5))/fps*3
        self.yspeed = (y-int(cell.y/scale-camera_y+.5))/fps*3

        self.id = ejected_id
        ejected_id += 1
        self.time_created = time.time()

        total_speed = (abs(self.xspeed)**2+abs(self.yspeed)**2)**(1/2)
        if total_speed == 0:
            return
        percent_x = self.xspeed/total_speed
        percent_y = self.yspeed/total_speed
       
        self.xspeed = ejected_speed*percent_x
        self.yspeed = ejected_speed*percent_y
       

        count = 0
        while (cell.x-self.x)**2+(cell.y-self.y)**2 < (cell.radius+self.radius)**2 and count < 1000:
            self.x += self.xspeed/10
            self.y += self.yspeed/10
            count += 1
       
    def tick(self):
        self.radius = self.mass**(1/2)
        self.smoothradius += (self.radius - self.smoothradius)/smoothness
        global ejected_size
       
        self.x += self.xspeed
        self.y += self.yspeed

        self.xspeed /= 1.1
        self.yspeed /= 1.1


        if self.x > border_width:
            self.x = border_width
            self.xspeed *= -.5
        if self.x < -border_width:
            self.x = -border_width
            self.xspeed *= -.5
        if self.y > border_height:
            self.y = border_height
            self.yspeed *= -.5
        if self.y < -border_height:
            self.y = -border_height
            self.yspeed *= -.5
           
       
        pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), self.color)
       
        if len(ejected) < 1000:
            pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))



        self.check_colliding(cells)
        self.check_brown(brown_viruses)

        for mass in ejected:
                if mass.x != self.x and mass.y != self.y:
                        if ((self.x-mass.x)**2+(self.y-mass.y)**2) < (self.radius/2+mass.radius/2)**2 and mass.id not in ejected_to_delete and self.id not in ejected_to_delete and self.mass >= mass.mass:
                                self.consume_ejected(mass)


    def check_colliding(self, cells):
        #if time.time() - self.time_created >= 0.3:
        for thing in cells:
            if self.id not in ejected_to_delete:
                if (self.x-thing.x)**2+(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2 and (True or thing.mass > self.mass*1.2):
                    thing.consume_ejected(self)

            if thing.id not in cells_to_delete:
                if (self.x-thing.x)**2+(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2 and self.mass > thing.mass*2:
                        self.consume_cell(thing)

    def check_brown(self, brown_viruses):
        for virus in brown_viruses:
            if self.id not in ejected_to_delete:
                if (self.x-virus.x)**2+(self.y-virus.y)**2 < (self.radius/2+virus.radius)**2:
                    virus.consume_ejected(self)


    def consume_ejected(self, ejected):
        self.mass += ejected.mass
        ejected_to_delete.add(ejected.id)
        self.radius = self.mass**(1/2)
        
    def consume_cell(self, cell):
        self.mass += cell.mass
        cells_to_delete.add(cell.id)
        self.radius = self.mass**(1/2)



class virus:

    def __init__(self, x, y, mass, color):
        global virus_id
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = mass**(1/2)
        self.color = color
        self.id = virus_id
        virus_id += 1

    def tick(self):
        self.check_colliding(cells)
        self.draw_high_quality()

    def draw(self):
        global camera_x
        global camera_y
        pygame.draw.circle(window, self.color, (self.x/scale-camera_x, self.y/scale-camera_y), self.radius/scale)

    def draw_high_quality(self):
        global camera_x
        global camera_y

       
        pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), self.color)
        pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))


    def check_colliding(self, cells):
        for thing in cells:
            if self.id not in viruses_to_delete:
                if thing.mass >= virus_mass*1.3 and abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/4+thing.radius)**2:
                    thing.consume_virus(self)


class brown_virus:
    def __init__(self, x, y, mass, color):
        global brown_virus_id
        self.x = x
        self.y = y
        self.mass = mass
        self.startmass = mass
        self.radius = mass**(1/2)
        self.smoothradius = self.radius
       
        self.color = color
        self.id = brown_virus_id
        brown_virus_id += 1

    def tick(self):
        if self.mass > self.startmass:
            self.spit()
        
        elif random.randint(0, fps) == 0:
             self.spit() 
            
        self.draw_high_quality()




    def spit(self):
        spit_mult = 1
        spit_mass = 2
        rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        spatted = agar(self.x+random.randint(-100, 100)/100.0, self.y+random.randint(-100, 100)/100.0, spit_mass, rand_color)
        xspeed=spatted.x-self.x
        yspeed=spatted.y-self.y
        count = 0
        while (spatted.x-self.x)**2+(spatted.y-self.y)**2 < (self.radius+spatted.radius+3)**2 and count < 10000:
            spatted.x += xspeed
            spatted.y += yspeed
            count += 1
        if count > 9000:
            print("WARN: Spit took too long!")
        agars.add(spatted)
        self.mass -= spit_mass/spit_mult
        self.mass = max(self.mass, self.startmass)
       

       
    def draw(self):
        global camera_x
        global camera_y
        pygame.draw.circle(window, self.color, (self.x/scale-camera_x, self.y/scale-camera_y), self.radius/scale)

    def draw_high_quality(self):
        global camera_x
        global camera_y
        self.radius = self.mass**(1/2)
        self.smoothradius += (self.radius - self.smoothradius)/20
        pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), self.color)
        pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))

    def colliding(self, thing):
        return abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/4+thing.radius)**2


    def consume_ejected(self, thing):
        self.mass += thing.mass
        ejected_to_delete.add(thing.id)

    def consume_cell(self, cell):
        self.mass += cell.mass
        cells_to_delete.add(cell.id)
       


def game_tick():
    global camera_x
    global camera_y
    global cell_time
    global agar_time
    global virus_time
    global ejected_time
   
    target_camera_x, target_camera_y = calc_center_of_mass(players[player])
    target_camera_x = target_camera_x/scale-width/2
    target_camera_y = target_camera_y/scale-height/2
    camera_x += (target_camera_x-camera_x)/1
    camera_y += (target_camera_y-camera_y)/1

    timer_start = time.time()
    #Cells
    for thing in cells:
        player_font_color = blue
        player_font_width = int(thing.radius/scale/2+1)
        #dialogue_font = pygame.font.SysFont(font, player_font_width)
        thing.apply_physics()
        #dialogue = dialogue_font.render(player_names[thing.player], aa_text, player_font_color)
        #dialogue_rect = dialogue.get_rect(center=(int(thing.x/scale-camera_x+.5), int(thing.y/scale-camera_y+.5)))
        #window.blit(dialogue, dialogue_rect)
        #dialogue = dialogue_font.render(str(int(thing.mass)), aa_text, player_font_color)
        #dialogue_rect = dialogue.get_rect(center=(int(thing.x/scale-camera_x+.5), int(thing.y/scale-camera_y+player_font_width)))
        #window.blit(dialogue, dialogue_rect)
       
    cell_time += time.time()-timer_start

    dialogue_font = pygame.font.SysFont(font, font_width)


    for thing2 in players:
        if thing2 != players[player]:
            for thing in thing2:
                balls = thing.target

                if balls.mass*2.6 < thing.mass and balls.id not in cells_to_delete:
                        if (thing.x-balls.x)**2+(thing.y-balls.y)**2 < thing.radius**2*2:
                            for bruh in thing2:
                                    bruh.split()
                            break

    timer_start = time.time()

    #AGARS
   
    for thing in agars_to_draw:
        thing.check_colliding(cells)

    for thing in agars:
        if aa_agar:
            thing.draw_high_quality()
        if thing.id not in agar_to_delete:
            thing.draw()

       
       
    agar_time += time.time()-timer_start


    timer_start = time.time()
    for thing in ejected:
        thing.tick()
    ejected_time += time.time()-timer_start

    timer_start = time.time()
    for thing in viruses:
        thing.tick()
   


    for thing in brown_viruses:
        thing.tick()

    virus_time += time.time()-timer_start



smooth_fix_limit = 3

window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()

cells = []

ejected = []

viruses = []
brown_viruses = []
players = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],]
players = [[], [], []]
player_names = ["Player", "Bot 1", "Bot 2", "Bot 3", "Bot 4", "Bot 5", "Bot 6", "Bot 7", "Bot 8", "Bot 9", "Bot 10"]
player_cell = cells.append(Cell(0, 0, player_start_mass, green, 0))

#cells.append(cell(1000, 1000, 100, red, 1))
#cells.append(cell(-1000, -1000, 100, blue, 2))
fps_ = 60

for i in range(len(players)):
        players[i] = [cell for cell in cells if cell.player == i]



def near_cells(thing):
    for cell in cells:
        if abs(cell.x-thing.x) < cell.radius+20:
            if abs(cell.y-thing.y) < cell.radius+20:
                if (cell.x-thing.x)**2+(cell.y-thing.y)**2 < (cell.radius+20)**2:
                    return True

    return False



agars = set()

agars_to_draw = set()


ejected_to_delete = set()

viruses_to_delete = set()

brown_viruses_to_delete = set()
border_width = 750
border_height = 750

agar_min_mass = 1
agar_max_mass = 4

max_agar_count = 3000

virus_count = 30
brown_virus_count = 10
last_time = time.time()
virus_mass = 100

for i in range(int(max_agar_count/2)):
    rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    agars.add(agar(random.randint(-border_width, border_width), random.randint(-border_height, border_height), random.randint(agar_min_mass, agar_max_mass), rand_color))

for i in range(int(virus_count)):
    viruses.append(virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), virus_mass, green))

for i in range(int(brown_virus_count)):
    brown_viruses.append(brown_virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), brown_virus_mass, brown))


player = 0

cell_time = 0
agar_time = 0
virus_time = 0
ejected_time = 0
computational_time = 0
total_time = time.time()
tick_time = 0
playing = True

aa_text = True
while playing:
    start = time.time()
   
    #cProfile.run('re.compile("game_tick()")')

    cells.sort(key=lambda x: x.mass, reverse=False)
    if frames % 15 == 1:
        agars_to_draw = [agar for agar in agars if near_cells(agar)]
    for i in range(len(players)):
        thing = players[i]
        if len(thing) < 1:
             cells.append(Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), bot_start_mass, red, i))

    for thing in players[player]:
        thing.color = light_blue
   
    window.fill(background_color)
    for i in range(len(players)):
        players[i] = [cell for cell in cells if cell.player == i]

    if len(viruses) < virus_count:
        viruses.append(virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), virus_mass, green))

    if len(brown_viruses) < brown_virus_count:
        brown_viruses.append(brown_virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), brown_virus_mass, brown))
   
    if len(agars) < max_agar_count:
        if frames%int(len(agars)/15000*fps+1) == 0:
            rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            agars.add(agar(random.randint(-border_width, border_width), random.randint(-border_height, border_height), random.randint(agar_min_mass, agar_max_mass), rand_color))

    target_scale = 0
    for thing in players[player]:
        target_scale += thing.radius**(1/4)/10
       

    target_scale/= len(players[player])**(1/1.5)

    scale += (target_scale-scale)/smoothness*2

    total_mass = sum(cell.mass for cell in players[player])


    for thing in players:
        if thing[0].player != player:
            biggest = thing[len(thing)-1]

            for thing2 in cells:
                if thing2.mass*1.3<biggest.mass and thing2.player != biggest.player:
                    for buggin in thing:
                        buggin.target = thing2
                    #print("sacs")

                   
               
   
    if scale > 1:
        aa_agar = False
    else:
        aa_agar = True
   
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            playing = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break

            if event.key == pygame.K_SPACE:
                for i in range(len(players[player])):
                    if len(players[player]) < player_max_cells and players[player][i].mass >= split_min_mass:
                        players[player][i].split()
                        players[player].append(cells[len(cells)-1])

            if event.key == pygame.K_w:
                for thing in players[player]:
                    if thing.mass > eject_min_mass and thing.mass > ejected_loss:
                        thing.eject_mass()
            if event.key == pygame.K_f:
                pass
            if event.key == pygame.K_F11:
                if width == 1920:
                        width, height = 1280, 720
                if width == 1280:
                        width, height = 1920, 1080
    if pygame.key.get_pressed()[pygame.K_e]:
        for thing in players[player]:
            if thing.mass > eject_min_mass and thing.mass > ejected_loss:
                thing.eject_mass()
    if pygame.key.get_pressed()[pygame.K_z]:
        for i in range(len(players[player])):
            if len(players[player]) < player_max_cells and players[player][i].mass >= split_min_mass:
                players[player][i].split()
                players[player].append(cells[len(cells)-1])
               

    start_tick_time = time.time()
    game_tick()
    tick_time += time.time()-start_tick_time


    dialogue = dialogue_font.render("Mass: " + str(int(total_mass+.5)), aa_text, font_color)
    window.blit(dialogue, (0, 0))
    dialogue = dialogue_font.render("FPS: " + str(fps_), aa_text, font_color)
    dialogue_rect = dialogue.get_rect(center=(100, 100))
    window.blit(dialogue, dialogue_rect)
   
    dialogue = dialogue_font.render("CELLS: " + str(len(cells)), aa_text, font_color)
    dialogue_rect = dialogue.get_rect(center=(100, 125))
    window.blit(dialogue, dialogue_rect)
    dialogue = dialogue_font.render("PLAYERS: " + str(len(players)), aa_text, font_color)
    dialogue_rect = dialogue.get_rect(center=(100, 150))
    window.blit(dialogue, dialogue_rect)
    dialogue = dialogue_font.render("AGARS: " + str(len(agars)), aa_text, font_color)
    dialogue_rect = dialogue.get_rect(center=(100, 175))
    window.blit(dialogue, dialogue_rect)
    dialogue = dialogue_font.render("AGARS CALCULATING: " + str(len(agars_to_draw)), aa_text, font_color)
    dialogue_rect = dialogue.get_rect(center=(100, 200))
    window.blit(dialogue, dialogue_rect)

    start_time = time.time()
    pygame.display.flip()
    flipping_time = time.time()-start_time
    computational_time += time.time()-start

   
    clock.tick(fps)
    if frames % int(fps/2) == 0:
        fps_ = int(1/(time.time()-start)+0)
        last_time = time.time()
    frames += 1

    agar_to_delete = set(agar_to_delete)

    agars = set([agar for agar in agars if agar.id not in agar_to_delete])
    ejected = [ejected_mass for ejected_mass in ejected if ejected_mass.id not in ejected_to_delete]
    cells = [cell for cell in cells if cell.id not in cells_to_delete]
    viruses = [virus for virus in viruses if virus.id not in viruses_to_delete]
    brown_viruses = [brown_virus for brown_virus in brown_viruses if brown_virus.id not in brown_viruses_to_delete]
    for i in range(len(players)):
        thing = players[i]
        if len(thing) < 1:
             cells.append(Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), player_start_mass, red, i))
    for i in range(len(players)):
        players[i] = [cell for cell in cells if cell.player == i]
   

pygame.quit()


print("Cell time: " + str(cell_time))
print("Ejected time: " + str(ejected_time))
print("Virus time: " + str(virus_time))
print("Agar time: " + str(agar_time))
print("Total time: " + str(time.time()-total_time))
print("Computational time: " + str(computational_time))
print("Flipping time: " + str(flipping_time))

print("Tick time: " + str(tick_time))

