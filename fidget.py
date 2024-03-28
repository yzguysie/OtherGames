# Fidget Spinner game




#MAKE IT SO IF FAN WAS ON DURING SPINNING SESSION, MULTIPLIER INCREASES ARE CANCELLED
import pygame
from pygame import gfxdraw
pygame.init()
import random
import math
import time
import ui




class Sprite():
    def __init__(self, image, x, y, rotation):
        self.x = x
        self.y = y
        self.ogimage = image
        self.image = self.ogimage
        self.rotation = rotation

    def draw(self):
        self.image = pygame.transform.rotate(self.ogimage, self.rotation)
        window.blit(self.image, (self.x-self.image.get_width()/2, self.y-self.image.get_height()/2))
    

def spin():
    global fidget_spinner_speed
    global fan_on
    fidget_spinner_speed /= 1.5
    fidget_spinner_speed += fidget_spinner_spin_speed/100*random.randint(70,135)



        
def tick_buttons():
    global fidget_spinner_speed
    global fidget_spinner_spin_speed
    global coins
    global upgrade_speed_price
    global decrease_friction_price
    global fidget_spinner_spin_speed
    global fidget_spinner_multiplicative_friction
    global fidget_spinner_constant_friction
    global fan_bought
    global fan_speed
    global fan_on
    global fan_upgrade_price
    global brake_bought
    global brake_on
    global brake_upgrade_price
    global brake_friction
    for button in buttons:
        button.draw()
        if button.get_clicked():
            if button == spin_button:
                spin()

            elif button == upgrade_speed_button:
                if coins >= upgrade_speed_price:
                    coins -= upgrade_speed_price
                    fidget_spinner_spin_speed *= 1.5
                    upgrade_speed_price *= 4
                    upgrade_speed_button.update_text("Upgrade Speed: " + str(upgrade_speed_price))
                    
            elif button == decrease_friction_button:
                if coins >= decrease_friction_price:
                    coins -= decrease_friction_price
                    fidget_spinner_multiplicative_friction /= 1.25
                    fidget_spinner_constant_friction = fidget_spinner_multiplicative_friction*500
                    decrease_friction_price *= 4

                    decrease_friction_button.update_text("Decrease Friction: " + str(decrease_friction_price))
                    

            elif button == fan_button:
                if not fan_bought:
                    if coins >= fan_price:
                        coins -= fan_price
                        fan_bought = True
                        fan_on = False
                        fan_button.update_text("Turn Fan On")
                else:
                    fan_on = not fan_on
                    if fan_on:
                        fan_button.update_text("Turn Fan Off")
                    else:
                        fan_button.update_text("Turn Fan On")

            elif button == fan_upgrade_button:
                if coins >= fan_upgrade_price:
                    coins -= fan_upgrade_price
                    fan_speed *= 1.5
                    fan_upgrade_price *= 5
                    fan_upgrade_button.update_text("Upgrade Fan: " + str(fan_upgrade_price))
        
            elif button == brake_button:
                if not brake_bought:
                    if coins >= brake_cost:
                        coins -= brake_cost
                        brake_bought = True
                        brake_on = False
                        brake_button.update_text("Turn Brake On")
                else:
                    brake_on = not brake_on
                    if brake_on:
                        brake_button.update_text("Turn Brake Off")
                    else:
                        brake_button.update_text("Turn Brake On")

            elif button == brake_upgrade_button:
                if coins >= brake_upgrade_price:
                    coins -= brake_upgrade_price
                    brake_friction *= 1.25
                    brake_upgrade_price *= 15
                    brake_upgrade_button.update_text("Upgrade Brake: " + str(brake_upgrade_price))

            else:
                print("Unknown button clicked")

width, height = 1280, 720
fps = 60

window = pygame.display.set_mode([width, height])
pygame.display.set_caption("Fidget Spinner Game")



white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
light_gray = (225, 230, 240)
dark_gray = (64, 64, 64)
silver = (16,16,20)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

BACKGROUND_COLOR = (dark_gray)
TEXT_COLOR = green
clock = pygame.time.Clock()

fidget_spinner_width, fidget_spinner_height = 350, 350
fidget_spinner_image = pygame.transform.scale(pygame.image.load("fidgetspinnerdefault.png"), (fidget_spinner_width, fidget_spinner_height))
fidget_spinner_rotation = 0


fidget_spinner_speed = 0
fidget_spinner_spin_speed = 1000
fidget_spinner_multiplicative_friction = .5
fidget_spinner_constant_friction = fidget_spinner_multiplicative_friction*500
fidget_spinner = Sprite(fidget_spinner_image, width/2, height/2, fidget_spinner_rotation)



upgrade_speed_price = 50
decrease_friction_price = 100

fan_bought = False
fan_on = False
fan_speed = 3500
fan_price = 2500
fan_upgrade_price = 10000

brake_bought = False
brake_on = False
brake_cost = 5000
brake_upgrade_price = 10000
brake_friction = .5

button_height = height/25
buttons = []

spin_button = ui.button(window, width/2-button_height*1.25, height-button_height*2, button_height*2.5, button_height, "Spin")
upgrade_speed_button = ui.button(window, width-button_height*10, button_height, button_height*7.5, button_height, "Upgrade Speed: " + str(upgrade_speed_price))
decrease_friction_button = ui.button(window, width-button_height*10, button_height*2, button_height*7.5, button_height, "Decrease Friction: " + str(decrease_friction_price))
fan_button = ui.button(window, width-button_height*10, button_height*3, button_height*5, button_height, "Buy Fan: " + str(fan_price))
fan_upgrade_button = ui.button(window, width-button_height*10, button_height*4, button_height*5, button_height, "Upgrade Fan: " + str(fan_upgrade_price))
brake_button = ui.button(window, width-button_height*10, button_height*5, button_height*5, button_height, "Buy Brake: " + str(brake_cost))
brake_upgrade_button = ui.button(window, width-button_height*10, button_height*6, button_height*5, button_height, "Upgrade Brake: " + str(brake_upgrade_price))
buttons.append(spin_button)
buttons.append(upgrade_speed_button)
buttons.append(decrease_friction_button)
buttons.append(fan_button)
buttons.append(fan_upgrade_button)
buttons.append(brake_button)
buttons.append(brake_upgrade_button)



coins = 5000

font = 'arial'
font_width = int(width/100+1)

dialogue_font = pygame.font.SysFont(font, font_width)

spinning = False
spins = 0
multiplier = 1

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
                spin()


    window.fill(BACKGROUND_COLOR)


    tick_buttons()

    if fan_bought and fan_on and fidget_spinner_speed < fan_speed:
        fidget_spinner_speed += (fan_speed-fidget_spinner_speed)/fps*2


    
    
    if fidget_spinner_speed > fidget_spinner_constant_friction*2/fps:

        while fidget_spinner.rotation > 360:
            spins += 1
            fidget_spinner.rotation -= 360
            
        while fidget_spinner.rotation < -360:
            spins += 1
            fidget_spinner.rotation += 360
        spinning = True
        fidget_spinner.rotation += fidget_spinner_speed/fps

        fidget_spinner_speed -= fidget_spinner_constant_friction*(fidget_spinner_speed/abs(fidget_spinner_speed))/fps
        fidget_spinner_speed -= fidget_spinner_speed*fidget_spinner_multiplicative_friction/fps

        if brake_bought and brake_on and abs(fidget_spinner_speed) > 0:
            print(brake_friction)
            fidget_spinner_speed -= brake_friction*2500*(fidget_spinner_speed/abs(fidget_spinner_speed))/fps
            fidget_spinner_speed -= fidget_spinner_speed*brake_friction/fps
    else:
        if spinning:          
                
            coins += spins*multiplier
            print(coins)
            spins = 0
        spinning = False

    if spins >= 25 and multiplier < 2:
        multiplier = 2
    if spins >= 50 and multiplier < 3:
        multiplier = 3
    if spins >= 100 and multiplier < 4:
        multiplier = 4
    if spins >= 250 and multiplier < 5:
        multiplier = 5
    if spins >= 1000 and multiplier < 10:
        multiplier = 10

    if spins >= 5000 and multiplier < 25:
        multipler = 25

    if spins >= 25000 and multiplier < 100:
        multipler = 100



    dialogue = dialogue_font.render("Coins: " + str(coins), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40))
    dialogue = dialogue_font.render("Spins: " + str(spins), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40*2))
    dialogue = dialogue_font.render("Coin multiplier: " + str(multiplier), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40*3))
    
    dialogue = dialogue_font.render("Upgrade speed price: " + str(upgrade_speed_price), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40*4))
    dialogue = dialogue_font.render("Decrease friction price: " + str(decrease_friction_price), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40*5))
    dialogue = dialogue_font.render("RPM: " + str(int(fidget_spinner_speed/6)), True, TEXT_COLOR)
    window.blit(dialogue, (0, height/40*6))
    
    
    fidget_spinner.draw()



    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
