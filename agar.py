import pygame
import pygame.gfxdraw
pygame.init()
import math
import random
import time





from configparser import ConfigParser

config = ConfigParser()

# parse existing file
config.read('agar.ini')

# read values from a section
fps = config.getint('settings', 'fps')
speed = config.getfloat('settings', 'speed')

gamemode = config.getint('settings', 'gamemode')
border_width = config.getint('settings', 'border_width')
border_height = config.getint('settings', 'border_height')

virus_count = config.getint('settings', 'virus_count')
virus_mass = config.getint('settings', 'virus_mass')

brown_virus_count = config.getint('settings', 'brown_virus_count')
brown_virus_mass = config.getint('settings', 'brown_virus_mass')


player_start_mass = config.getint('settings', 'player_start_mass')
player_speed = config.getfloat('settings', 'player_speed')
player_min_mass = config.getint('settings', 'player_min_mass')
player_max_cells = config.getint('settings', 'player_max_cells')
player_max_cell_mass = config.getint('settings', 'player_max_cell_mass')
player_decay_rate = config.getfloat('settings', 'player_decay_rate')
player_recombine_time = config.getfloat('settings', 'player_recombine_time')
player_eject_min_mass = config.getint('settings', 'player_eject_min_mass')
player_split_min_mass = config.getint('settings', 'player_split_min_mass')

ejected_size = config.getint('settings', 'ejected_size')
ejected_loss = config.getint('settings', 'ejected_loss')
ejected_speed = config.getint('settings', 'ejected_speed')

bot_count = config.getint('settings', 'bot_count')
bot_start_mass = config.getint('settings', 'bot_start_mass')

minion_count = config.getint('settings', 'minion_count')
minion_start_mass = config.getint('settings', 'minion_start_mass')

# update existing value


width, height = 1280, 720

target_scale = 105

scale = .2
aa_agar = True
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
light_green = (64, 255, 64)
dark_green = (0, 192, 0)
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

objects_to_delete = set()

camera_x = 0
camera_y = 0
drawable_count = 0
frames = 0






font = 'arial'
font_width = int(width/100+1)
dialogue_font = pygame.font.SysFont(font, font_width)
objects = []

pygame.display.set_caption("Agar.io Clone")

smoothness = 15



def calc_center_of_mass(bodies):
        try:
            center_x = 0
            center_y = 0
            weight = 0
            for body_ in bodies:
                center_x += body_.x*body_.mass
                center_y += body_.y*body_.mass
                weight += body_.mass
            return (center_x/weight, center_y/weight)
        except:
            print("divide by 0")
            return (10, 10)

class Drawable:
    def __init__(self, x, y, mass, color):
        global drawable_count
        global objects

        self.x = x
        self.y = y
        self.mass = mass
        self.radius = math.sqrt(mass)
        self.smoothradius = self.radius
        self.color = color
        self.outline_color = (self.color[0]/1.5,self.color[1]/1.5, self.color[2]/1.5)
        self.outline_thickness = 3
        self.id = drawable_count
        drawable_count += 1
        self.consumer = False
        self.consumable = True


    def draw(self):
        
        if round(self.x/scale-camera_x) > - round(abs(self.smoothradius/scale)) and round(self.x/scale-camera_x) < width+round(abs(self.smoothradius/scale)):
            if round(self.y/scale-camera_y) > - round(abs(self.smoothradius/scale)) and round(self.y/scale-camera_y) < height+round(abs(self.smoothradius/scale)):
             
                self.radius = self.mass**(1/2)
                self.outline_thickness = round(math.sqrt(self.smoothradius/scale)/2)
                self.smoothradius += (self.radius - self.smoothradius)/smoothness

                #Draw Outline
                if self.outline_thickness > 0:
                    
                    pygame.gfxdraw.aacircle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale)), self.outline_color)
                    pygame.gfxdraw.filled_circle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale)), self.outline_color)
                
                #Draw Inside
                pygame.gfxdraw.aacircle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale-self.outline_thickness)), self.color)
                pygame.gfxdraw.filled_circle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale-self.outline_thickness)), self.color)


    def tick(self):
        self.check_consume()


    def check_consume(self):
        global objects
        global objects_to_delete
        if self.consumer:
            for obj in all_drawable(agars_ = False):
                if obj.consumable and obj != self:
                    distance_squared = (obj.x-self.x)**2+(obj.y-self.y)**2
                    if distance_squared < (self.radius-obj.radius/3)**2:
                        if self.id not in objects_to_delete and obj.id not in objects_to_delete:
                            if self.mass >= obj.mass*1.3:
                                
                                self.consume(obj)
         
    def consume(self, other):
        self.mass += other.mass
        objects_to_delete.add(other.id)
        
def new_cell(player, color):
    new_cell = Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), player_start_mass, color, player)
    cells.append(new_cell)
    return new_cell
    

class Player:
    def __init__(self, mode, color):
        self.mode = mode
        self.color = color
        
        self.target = (0, 0)
        self.cells = [new_cell(self, self.color)]
    
    def tick(self):

        self.target = self.get_target()
        for cell in self.cells:
            cell.target = self.target
            cell.tick()

    def split(self):
        for i in range(len(self.cells)):
            if len(self.cells) < player_max_cells:
                cell = self.cells[i]
                cell.split()
    def eject_mass(self):
        for cell in self.cells:
            if cell.mass > player_eject_min_mass:
                cell.eject_mass()

    def get_target(self):
        if self.mode == "player" or self.mode == "minion":
            x, y = pygame.mouse.get_pos()
            target = (x+camera_x)*scale, (y+camera_y)*scale
            
        
        elif self.mode == "bot":
            nearest_agar = get_nearest_agar(self)
            target = nearest_agar.x, nearest_agar.y

        else:
            target = (0, 0)

        return target


        

   
class Cell(Drawable):
   
    def __init__(self, x, y, mass, color, player):
        super().__init__(x, y, mass, color)
        self.consumer = True
        self.consumable = True
        self.extraxspeed = 0
        self.extrayspeed = 0
        self.slow_zone = 10
        self.speed = player_speed
        self.xspeed = 0
        self.yspeed = 0
        self.inertia = 5
        self.smoothradius = self.radius
        self.player = player
        self.target = player.target
        # if self.player != 0:
        #         self.target = Cell(1000, 1000, player_start_mass, green, 0)

        self.time_created = time.time()

    # def draw(self):

    #     self.radius = self.mass**(1/2)
    #     self.smoothradius += (self.radius - self.smoothradius)/smoothness

    #     #Draw Outline
    #     pygame.gfxdraw.aacircle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale)), self.outline_color)
    #     pygame.gfxdraw.filled_circle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale)), self.outline_color)
        
    #     #Draw Inside
    #     pygame.gfxdraw.aacircle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale-self.outline_thickness)), self.color)
    #     pygame.gfxdraw.filled_circle(window, round(self.x/scale-camera_x), round(self.y/scale-camera_y), round(abs(self.smoothradius/scale-self.outline_thickness)), self.color)
        

    def move(self):
        target_x, target_y = self.player.target
        xdiff = target_x-self.x
        ydiff = target_y-self.y

        angle = math.atan2(ydiff, xdiff)
        vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))

        velocity = min(self.slow_zone, math.sqrt(xdiff**2+ydiff**2))*10

        # if self.player == 0:
        #         x, y = pygame.mouse.get_pos()
        #         xdiff = x-int(self.x/scale-camera_x+.5)
        #         ydiff = y-int(self.y/scale-camera_y+.5)
        #         angle = math.atan2(ydiff, xdiff)
        #         vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        #         velocity = min(self.slow_zone, math.sqrt(xdiff**2+ydiff**2))

        # else:
        #         x, y = self.target.x, self.target.y
        #         xdiff = x-int(self.x+.5)
        #         ydiff = y-int(self.y+.5)
        #         angle = math.atan2(ydiff, xdiff)
        #         vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        #         velocity = self.slow_zone




        self.xspeed = velocity*vector[0]/fps*self.speed
        self.yspeed = velocity*vector[1]/fps*self.speed

        # if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                
        #         self.xspeed += (xforce)/fps
        #         self.yspeed += (yforce)/fps
        # else:
        #         self.xspeed = (self.xspeed*self.inertia)+(xforce)/fps_
        #         self.yspeed = (self.yspeed*self.inertia)+(yforce)/fps_


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
        
        if len(self.player.cells) > player_max_cells or self.mass < player_split_min_mass:
                return
        
        self.mass /= 2
        new_cell = Cell(self.x, self.y+.1, self.mass, self.color, self.player)
        cells.append(new_cell)
        self.player.cells.append(new_cell)
        

        if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                extrax = (self.target[0]-self.x)/fps
                extray = (self.target[1]-self.y)/fps
        else:
                extrax = (self.target[0]-self.x)/fps_
                extray = (self.target[1]-self.y)/fps_


       
       
        total_speed = (abs(extrax)**2+abs(extray)**2)**(1/2)
       
        if extrax**2+extray**2 > player_speed**2:
                percent_x = extrax/total_speed
                percent_y = extray/total_speed

               
                       
               
                extrax = player_speed*percent_x
                extray = player_speed*percent_y

        cells[len(cells)-1].extraxspeed = extrax*cells[len(cells)-1].radius**(2/3)
        cells[len(cells)-1].extrayspeed = extray*cells[len(cells)-1].radius**(2/3)

        return new_cell

    def tick(self):
        self.apply_physics()
       
    def apply_physics(self):
        global camera_x
        global camera_y
        if self.mass > player_min_mass:
            if fps_ < fps/smooth_fix_limit or fps_ > fps*smooth_fix_limit:
                self.mass -= self.mass*player_decay_rate/fps
            else:
                self.mass -= self.mass*player_decay_rate/fps_  
       
       
               
        self.move()

       

        self.check_colliding(cells)
        self.check_viruses(brown_viruses)
       
    # def consume(self, agar):
    #     self.mass += agar.mass
    #     objects_to_delete.add(agar.id)

    # def consume_ejected(self, ejected):
    #     self.mass += ejected.mass
    #     objects_to_delete.add(ejected.id)


    def consume_virus(self, virus):
        self.mass += virus.mass
        objects_to_delete.add(virus.id)
        while len(self.player.cells) < player_max_cells and self.mass > player_split_min_mass:
                self.split()
                self.player.cells.append(cells[len(cells)-1])
                self.player.cells[len(self.player.cells)-1].time_created = time.time()-.5
                self.player.cells[len(self.player.cells)-1].extraxspeed = 0
                self.player.cells[len(self.player.cells)-1].extrayspeed = 0


    def consume_brown_virus(self, virus):
        self.mass += virus.mass
        objects_to_delete.add(virus.id)
        while len(self.player.cells) < player_max_cells and self.mass > player_split_min_mass:
                self.split()
                self.player.cells.append(cells[len(cells)-1])
                self.player.cells[len(self.player.cells)-1].time_created = time.time()-.5
                self.player.cells[len(self.player.cells)-1].extraxspeed = 0
                self.player.cells[len(self.player.cells)-1].extrayspeed = 0    
               
   

    def check_viruses(self, viruses):
        for virus in viruses:
            if self.mass*1.3 < virus.mass:
                if (virus.x-self.x)**2+(virus.y-self.y)**2 < (virus.radius-self.radius/3)**2:
                    if self.id not in objects_to_delete and virus.id not in objects_to_delete:
                        virus.consume(self)
            if self.mass > virus.mass*1.3:
                if (virus.x-self.x)**2+(virus.y-self.y)**2 < (self.radius-virus.radius/3)**2:
                    if self.id not in objects_to_delete and virus.id not in objects_to_delete:
                        self.consume_brown_virus(virus)

       
    def eject_mass(self):
        ejected.append(Ejected(self))

    def check_colliding(self, cells):
        global player_recombine_time

       
        for thing in self.player.cells:
           
            if thing.id != self.id:
                sq_distance = ((thing.x-self.x)**2+(thing.y-self.y)**2)
                if sq_distance < (thing.radius+self.radius)**2:
                    if (time.time()-thing.time_created < player_recombine_time*(self.mass**(1/4)/4) or time.time()-self.time_created < player_recombine_time*(self.mass**(1/4)/4)) and thing.player == self.player:
                        if time.time()-thing.time_created > .5 and time.time()-self.time_created > .5:
                            count = 0
                            combined_radius_squared = (thing.radius+self.radius)**2
                            while (thing.x-self.x)**2+(thing.y-self.y)**2 < combined_radius_squared and count < 10:
                                xdiff = thing.x-self.x
                                ydiff = thing.y-self.y

                                combined_mass = self.mass+thing.mass
                                xpush = (xdiff)/(thing.radius+self.radius)/5
                                ypush = (ydiff)/(thing.radius+self.radius)/5
                                thing.x += xpush*(self.mass/combined_mass)
                                thing.y += ypush*(self.mass/combined_mass)
                                self.x -= xpush*(thing.mass/combined_mass)
                                self.y -= ypush*(thing.mass/combined_mass)
                                count += 1
                            if count >= 10:
                                pass
                    else:
                        if (thing.x-self.x)**2+(thing.y-self.y)**2 < (self.radius-thing.radius/3)**2:
                            if self.id not in objects_to_delete and thing.id not in objects_to_delete:
                                if self.player == thing.player:
                                        self.combine(thing)
                                else:
                                        if self.mass >= thing.mass*1.3 and sq_distance < (self.radius-thing.radius/4)**2:
                                                self.combine(thing)
                                        elif thing.mass >= self.mass*1.3 and sq_distance < (thing.radius-self.radius/4)**2:
                                                thing.combine(self)

        for thing in cells:
           
            if thing.player != self.player:
                distance = ((thing.x-self.x)**2+(thing.y-self.y)**2)**(1/2)
                if distance < (thing.radius+self.radius):
                            if self.id not in objects_to_delete and thing.id not in objects_to_delete:
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
                objects_to_delete.add(consumed.id)
                break
                   
               

class Agar(Drawable):

    def __init__(self, x, y, mass, color):
        super().__init__(x, y, mass, color)

    # def draw(self):
    #     global camera_x
    #     global camera_y
    #     pygame.draw.circle(window, self.color, (self.x/scale-camera_x, self.y/scale-camera_y), self.radius/scale)

    # def draw_high_quality(self):
    #     global camera_x
    #     global camera_y
    #     if self.x/scale-camera_x < -self.radius or self.y/scale-camera_y < -self.radius or self.x/scale-camera_x > width+self.radius or self.y/scale-camera_y > height+self.radius:
    #         return
       
    #     pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), self.color)
    #     pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))

    def tick(self):
        global cells
        self.check_colliding(cells)

    def check_colliding(self, cells):
        for thing in cells:
            if self.id not in objects_to_delete:
                if abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2:
                    thing.consume(self)


class Ejected(Drawable):

    def __init__(self, cell):
        
        global camera_x
        global camera_y
        global ejected_size
        global ejected_loss
        global eject_min_size
        global ejected_speed
        super().__init__(cell.x, cell.y, ejected_size, cell.color)
       
       
        cell.mass -= ejected_loss
        x, y = pygame.mouse.get_pos()
        
        self.xspeed = (x-int(cell.x/scale-camera_x+.5))/fps*3
        self.yspeed = (y-int(cell.y/scale-camera_y+.5))/fps*3

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
           
       
        # pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), self.color)
       
        # if len(ejected) < 1000:
        #     pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.smoothradius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))



        self.check_colliding(cells)
        self.check_brown(brown_viruses)

        for mass in ejected:
                if mass.x != self.x and mass.y != self.y:
                        if ((self.x-mass.x)**2+(self.y-mass.y)**2) < (self.radius/2+mass.radius/2)**2 and mass.id not in objects_to_delete and self.id not in objects_to_delete and self.mass >= mass.mass:
                                self.consume(mass)


    def check_colliding(self, cells):
        #if time.time() - self.time_created >= 0.3:
        for thing in cells:
            if self.id not in objects_to_delete:
                if (self.x-thing.x)**2+(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2 and (True or thing.mass > self.mass*1.2):
                    thing.consume(self)

            if thing.id not in objects_to_delete:
                if (self.x-thing.x)**2+(self.y-thing.y)**2 < (self.radius/2+thing.radius)**2 and self.mass > thing.mass*2:
                        self.consume(thing)

    def check_brown(self, brown_viruses):
        for virus in brown_viruses:
            if self.id not in objects_to_delete:
                if (self.x-virus.x)**2+(self.y-virus.y)**2 < (self.radius/2+virus.radius)**2:
                    virus.consume(self)


    # def consume_ejected(self, ejected):
    #     self.mass += ejected.mass
    #     objects_to_delete.add(ejected.id)
    #     self.radius = self.mass**(1/2)
        
    # def consume_cell(self, cell):
    #     self.mass += cell.mass
    #     objects_to_delete.add(cell.id)
    #     self.radius = self.mass**(1/2)



class Virus(Drawable):

    def __init__(self, x, y, mass, color):
        super().__init__(x, y, mass, color)

    def tick(self):
        self.check_colliding(cells)

    # # def draw(self):
    # #     global camera_x
    # #     global camera_y
    # #     pygame.draw.circle(window, self.color, (self.x/scale-camera_x, self.y/scale-camera_y), self.radius/scale)

    # # def draw_high_quality(self):
    # #     global camera_x
    # #     global camera_y

       
    # #     pygame.gfxdraw.filled_circle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), self.color)
    # #     pygame.gfxdraw.aacircle(window, int(self.x/scale-camera_x+.5), int(self.y/scale-camera_y+.5), int(self.radius/scale+.5), (self.color[0]/1.75,self.color[1]/1.75, self.color[2]/1.75))


    def check_colliding(self, cells):
        for thing in cells:
            if self.id not in objects_to_delete:
                if thing.mass >= virus_mass*1.3 and abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/4+thing.radius)**2:
                    thing.consume_virus(self)


class BrownVirus(Drawable):
    def __init__(self, x, y, mass, color):
        super().__init__(x, y, mass, color)
        self.consumer = True
        self.spit_rate = 120
        self.startmass = mass
        self.smoothradius = self.radius

    def tick(self):
        if self.mass > self.startmass:
            self.spit()
        
        elif random.randint(0, fps) == 0:
            self.spit() 

        self.check_consume()
            




    def spit(self):
        spit_mult = 1
        spit_mass = 1
        rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        angle = random.uniform(0, 360)
        vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        spatted_x = self.x+(self.radius+spit_mass*2)*vector[0]
        spatted_y = self.y+(self.radius+spit_mass*2)*vector[1]
        spatted = Agar(spatted_x, spatted_y, spit_mass, rand_color)
        # xspeed=spatted.x-self.x
        # yspeed=spatted.y-self.y
        # count = 0
        # while (spatted.x-self.x)**2+(spatted.y-self.y)**2 < (self.radius+spatted.radius+3)**2 and count < 10000:
        #     spatted.x += xspeed
        #     spatted.y += yspeed
        #     count += 1
        # if count > 9000:
        #     print("WARN: Spit took too long!")
        agars.add(spatted)
        self.mass -= spit_mass/spit_mult
        self.mass = max(self.mass, self.startmass)
       

       

    def colliding(self, thing):
        return abs(self.x-thing.x)**2+abs(self.y-thing.y)**2 < (self.radius/4+thing.radius)**2


    # def consume_ejected(self, thing):
    #     self.mass += thing.mass
    #     objects_to_delete.add(thing.id)

    # def consume_cell(self, cell):
    #     self.mass += cell.mass
    #     objects_to_delete.add(cell.id)
       


def game_tick():
    global camera_x
    global camera_y
    global cell_time
    global agar_time
    global virus_time
    global ejected_time
   
    target_camera_x, target_camera_y = calc_center_of_mass(player.cells)
    target_camera_x = target_camera_x/scale-width/2
    target_camera_y = target_camera_y/scale-height/2
    camera_x += (target_camera_x-camera_x)/1
    camera_y += (target_camera_y-camera_y)/1

    timer_start = time.time()

    # #Cells
    # for thing in cells:
    #     player_font_color = blue
    #     player_font_width = int(thing.radius/scale/2+1)
    #     #dialogue_font = pygame.font.SysFont(font, player_font_width)
    #     thing.apply_physics()
    #     #dialogue = dialogue_font.render(player_names[thing.player], aa_text, player_font_color)
    #     #dialogue_rect = dialogue.get_rect(center=(int(thing.x/scale-camera_x+.5), int(thing.y/scale-camera_y+.5)))
    #     #window.blit(dialogue, dialogue_rect)
    #     #dialogue = dialogue_font.render(str(int(thing.mass)), aa_text, player_font_color)
    #     #dialogue_rect = dialogue.get_rect(center=(int(thing.x/scale-camera_x+.5), int(thing.y/scale-camera_y+player_font_width)))
    #     #window.blit(dialogue, dialogue_rect)
       
    # cell_time += time.time()-timer_start


    #Bot AI (I think idk I wrote this like 2 yrs ago)
    # for bot in players:
    #     if bot != players[player]: #Make sure not to control player, only bots
    #         for cell in bot:
    #             target_cell = cell.target
    #             #Bots will split for their target if they can, (only if they are in two or less pieces - should add this, also why is this done for each cell wtf)
                
    #             if target_cell.mass*2.6 < cell.mass and target_cell.id not in objects_to_delete:
    #                     if (cell.x-target_cell.x)**2+(cell.y-target_cell.y)**2 < cell.radius**2*2:
    #                         for bruh in bot:
    #                                 bruh.split()
    #                         break

    # timer_start = time.time()

    # #AGARS
   
    # for thing in agars_to_draw:
    #     thing.check_colliding(cells)

    # # for thing in agars:
    # #     if aa_agar:
    # #         thing.draw_high_quality()
    # #     if thing.id not in agar_to_delete:
    # #         thing.draw()

       
       
    # agar_time += time.time()-timer_start


    # timer_start = time.time()
    # for thing in ejected:
    #     thing.tick()
    # ejected_time += time.time()-timer_start

    # timer_start = time.time()
    # for thing in viruses:
    #     thing.tick()
   


    # for thing in brown_viruses:
    #     thing.tick()

    #virus_time += time.time()-timer_start
    all_objs = list(all_drawable())
    all_objs.sort(key=lambda x: x.radius)
    for thing in all_objs:
        if type(thing) != Cell:
            thing.tick()
    for player_ in players:
        player_.tick()
    for obj in all_objs:
        obj.draw()



smooth_fix_limit = 3

window = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()

cells = []

ejected = []

viruses = []
brown_viruses = []
#players = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],]
#players = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
#players = [[], [], []]
players = []
player = Player("player", light_blue)
players.append(player)
for i in range(bot_count):
    players.append(Player("bot", red))
for i in range(minion_count):
    players.append(Player("minion", green))
player_names = ["Player", "Bot 1", "Bot 2", "Bot 3", "Bot 4", "Bot 5", "Bot 6", "Bot 7", "Bot 8", "Bot 9", "Bot 10"]
#player_cell = cells.append(Cell(0, 0, player_start_mass, light_blue, player.cells[0]))

#cells.append(cell(1000, 1000, 100, red, 1))
#cells.append(cell(-1000, -1000, 100, blue, 2))
fps_ = 60

# for player in player.cells:
#         player.cells = [cell for cell in cells if cell.player == player]



def near_cells(thing):
    for cell in cells:
        if abs(cell.x-thing.x) < cell.radius+20:
            if abs(cell.y-thing.y) < cell.radius+20:
                if (cell.x-thing.x)**2+(cell.y-thing.y)**2 < (cell.radius+20)**2:
                    return True

    return False

def all_drawable(agars_ = True, ejected_ = True, viruses_ = True, brown_viruses_ = True, cells_ = True):
    if agars_:
        for agar in agars:
            yield agar
    if ejected_:
        for e in ejected:
            yield e
    if viruses_:
        for virus in viruses:
            yield virus
    if brown_viruses_:
        for brown_virus in brown_viruses:
            yield brown_virus
    if cells_:
        for cell in cells:
            yield cell

def all_consumable():
    for e in ejected:
        yield e
    for v in viruses:
        yield v
    for brown_virus in brown_viruses:
         yield brown_virus
    for cell in cells:
         yield cell
    
    
    
    
    
    

agars = set()

#agars_to_draw = set()






#border_width = 400
#border_height = 400

agar_min_mass = 1
agar_max_mass = 4

max_agar_count = 3000


last_time = time.time()

for i in range(int(max_agar_count/2)):
    rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    agars.add(Agar(random.randint(-border_width, border_width), random.randint(-border_height, border_height), random.randint(agar_min_mass, agar_max_mass), rand_color))

for i in range(int(virus_count)):
    viruses.append(Virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), virus_mass, green))

for i in range(int(brown_virus_count)):
    brown_viruses.append(BrownVirus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), brown_virus_mass, brown))



cell_time = 0
agar_time = 0
virus_time = 0
ejected_time = 0
computational_time = 0
total_time = time.time()
tick_time = 0
playing = True

def distance_squared(self, other):
    return (self.x-other.x)**2+(self.y-other.y)**2

def get_nearest_agar(player):
    mindist = 2147483646
    minagar = Agar(0, 0, 1, green)
    for cell in player.cells:
        for agar in agars:
            if distance_squared(cell, agar) < mindist:
                mindist = distance_squared(cell, agar)
                minagar = agar
    return minagar
     
aa_text = True
while playing:
    start = time.time()
   
    #cProfile.run('re.compile("game_tick()")')

    cells.sort(key=lambda x: x.mass, reverse=False)
    # if frames % 15 == 1:
    #     agars_to_draw = [agar for agar in agars if near_cells(agar)]
    # if len(player.cells) == 0:
    #     new_cell = Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), player_start_mass, light_blue, player)
    #     cells.append(new_cell)
    #     player.cells.append(new_cell)
    for p in players:
        if len(p.cells) == 0:
            if p.mode == "player":
                new_cell = Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), player_start_mass, light_blue, p)
            elif p.mode == "minion":
                new_cell = Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), minion_start_mass, green, p)
            else:
                new_cell = Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), bot_start_mass, red, p)
            cells.append(new_cell)
            p.cells.append(new_cell)
             

    # for thing in players[player]:
    #     thing.color = light_blue
   
    window.fill(background_color)
    # for player in players:
    #     player.cells = [cell for cell in cells if cell.player == player]

    if len(viruses) < virus_count:
        viruses.append(Virus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), virus_mass, green))

    if len(brown_viruses) < brown_virus_count:
        brown_viruses.append(BrownVirus(random.randint(-border_width, border_width), random.randint(-border_height, border_height), brown_virus_mass, brown))
   
    if len(agars) < max_agar_count:
        if frames%int(len(agars)/15000*fps+1) == 0:
            rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            agars.add(Agar(random.randint(-border_width, border_width), random.randint(-border_height, border_height), random.randint(agar_min_mass, agar_max_mass), rand_color))

    target_scale = 0
    for thing in player.cells:
        target_scale += thing.radius**(1/4)/10
       

    target_scale/= max(len(player.cells)**(1/1.5), 1)

    scale += (target_scale-scale)/smoothness*2

    total_mass = sum(cell.mass for cell in player.cells)

    #Bot AI Target finding
    # for thing in players:
    #     if thing != player:
    #         biggest = thing.cells[len(thing.cells)-1]

    #         # for thing2 in cells:
    #         #     if thing2.mass*1.3<biggest.mass and thing2.player != biggest.player:
    #         #         for buggin in thing:
    #         #             buggin.target = thing2
    #         target = get_nearest_agar(biggest)
    #         for cell in thing.cells:
    #             cell.target = target
                

                   
               
   
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
                player.split()

            if event.key == pygame.K_w:
                player.eject_mass()

            if event.key == pygame.K_f:
                for p in players:
                    if p.mode == "minion":
                        p.split()
            if event.key == pygame.K_g:
                for p in players:
                    if p.mode == "minion":
                        p.eject_mass()
            if event.key == pygame.K_F11:
                if width == 1920:
                        width, height = 1280, 720
                if width == 1280:
                        width, height = 1920, 1080
                window = pygame.display.set_mode([width, height])
    if pygame.key.get_pressed()[pygame.K_e]:
        for thing in player.cells:
            if thing.mass > player_eject_min_mass and thing.mass > ejected_loss:
                thing.eject_mass()
    if pygame.key.get_pressed()[pygame.K_z]:
        for i in range(len(player.cells)):
            if len(player.cells) < player_max_cells and player.cells[i].mass >= player_split_min_mass:
                player.cells[i].split()
                player.cells.append(cells[len(cells)-1])


    # if pygame.key.get_pressed()[pygame.K_f]:
    #     for [player_ in players if player_.mode == "minion"]]:
    #         for i in range(len(player_.cells[player])):
    #             if len(player_.cells[player]) < player_max_cells and player.cells[player][i].mass >= player_split_min_mass:
    #                 player.cells[player][i].split()
    #                 player.cells[player].append(cells[len(cells)-1])
                

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
    # dialogue = dialogue_font.render("AGARS CALCULATING: " + str(len(agars_to_draw)), aa_text, font_color)
    # dialogue_rect = dialogue.get_rect(center=(100, 200))
    # window.blit(dialogue, dialogue_rect)

    start_time = time.time()
    pygame.display.flip()
    flipping_time = time.time()-start_time
    computational_time += time.time()-start

   
    clock.tick(fps)
    if frames % int(fps/2) == 0:
        fps_ = int(1/(time.time()-start)+0)
        last_time = time.time()
    frames += 1

    objects_to_delete = set(objects_to_delete)

    agars = set([agar for agar in agars if agar.id not in objects_to_delete])
    ejected = [ejected_mass for ejected_mass in ejected if ejected_mass.id not in objects_to_delete]
    cells = [cell for cell in cells if cell.id not in objects_to_delete]
    viruses = [virus for virus in viruses if virus.id not in objects_to_delete]
    brown_viruses = [brown_virus for brown_virus in brown_viruses if brown_virus.id not in objects_to_delete]
    objects = [obj for obj in objects if obj.id not in objects_to_delete]
    for cell in cells:
        if cell.mass > player_max_cell_mass:
            cell.split()
    for i in range(len(players)):
        thing = player.cells
        if len(thing) < 1:
             cells.append(Cell(random.randint(-border_width, border_width), random.randint(-border_height, border_height), player_start_mass, red, players[i]))
    for p in players:
        p.cells = [cell for cell in p.cells if cell.id not in objects_to_delete]
   

pygame.quit()


print("Cell time: " + str(cell_time))
print("Ejected time: " + str(ejected_time))
print("Virus time: " + str(virus_time))
print("Agar time: " + str(agar_time))
print("Total time: " + str(time.time()-total_time))
print("Computational time: " + str(computational_time))
print("Flipping time: " + str(flipping_time))

print("Tick time: " + str(tick_time))

