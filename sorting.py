import pygame
from pygame import gfxdraw
pygame.init()
import random
import math
import ui
import copy

width, height = 1280, 720
fps = 60


window = pygame.display.set_mode([width, height])
pygame.display.set_caption("Sorting image")



white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
light_gray = (192, 192, 192)
dark_gray = (64, 64, 64)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)

liner = 255
lineg = 255
lineb = 255

BACKGROUND_COLOR = (black)
clock = pygame.time.Clock()



def random_arr(arrlength, arrmax, arrmin):
    arr = []
    for i in range(arrlength):
        arr.append(random.randint(arrmin, arrmax))

    return arr

def bubble_sort_step(arr):
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            temp = arr[i+1];
            arr[i+1] = arr[i]
            arr[i] = temp
            
            if i % speed == 0:
                draw_frame(arr)

def selection_sort_step(arr):
    first_unsorted = sorted_amount(arr)
    smallest = arr[first_unsorted]
    smallest_i = first_unsorted
    i = first_unsorted
    while i < len(arr):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_i = i
        i+= 1
    temp = arr[first_unsorted]
    arr[first_unsorted] = arr[smallest_i]
    arr[smallest_i] = temp
    
def bogo_sort_step(arr):
    rand1 = random.randint(0, len(arr)-1)
    rand2 = random.randint(0, len(arr)-1)
    temp = arr[rand1]
    arr[rand1] = arr[rand2]
    arr[rand2] = temp
        
def insertion_sort_step(arr):
        index = sorted_amount(arr)+1
        while index > 0:
            if arr[index] < arr[index-1]:
                temp = arr[index]
                arr[index] = arr[index-1]
                arr[index-1] = temp
                if index % speed == 0:
                    draw_frame(arr)
            index -= 1

def merge_sort_step(a, index):
    global arr
    if len(a) > 1:
        mid = len(a)//2
        L = a[:mid]
        R = a[mid:]
        #a = copy.deepcopy(L[:]+R[:])
        merge_sort_step(L, index)
        merge_sort_step(R, index + mid)
        ab = copy.deepcopy(L[:]+R[:])
        i = j = k = 0
        
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            ab[k] = a[k]
            if k % speed == 0 and len(a) > speed:
                ar = arr[0:index]+ab+arr[index+len(ab):]
                draw_frame(ar)
                
            k += 1
        
        while i < len(L):
            
            a[k] = L[i]
            i += 1
            ab[k] = a[k]
            k += 1
            if k % speed == 0 and len(a) > speed:
                ar = arr[0:index]+ab+arr[index+len(ab):]
                draw_frame(ar)

        while j < len(R):
            a[k] = R[j]
            j += 1
            ab[k] = a[k]
            k += 1
            if k % speed == 0 and len(a) > speed:
                ar = arr[0:index]+ab+arr[index+len(ab):]
                draw_frame(ar)

        if len(a) > speed:
            arr = arr[0:index]+ab+arr[index+len(ab):]
            draw_frame(arr)





        
                
def sorted(arr):
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            return False;
    return True;

def sorted_amount(arr):
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            return i
    return len(arr)-1;

def draw_arr(arr):
    for i in range(len(arr)):
        elem_width = width/len(arr)
        if elem_width < 1:
            if i % round(1/elem_width) == 0:
                elem_width = 1
        if elem_width >= 1:
            element_rect = pygame.Rect(width*(i/len(arr)), height-(height*(arr[i]/arrmax)), elem_width, (height*(arr[i]/arrmax)))
            pygame.draw.rect(window, (liner, lineg, lineb), element_rect)


def shuffle(arr, amount):
    for i in range(amount):
        rand1 = random.randint(0, len(arr)-1)
        rand2 = random.randint(0, len(arr)-1)
        temp = arr[rand1]
        arr[rand1] = arr[rand2]
        arr[rand2] = temp

    return arr

def tick_buttons(events):
    global arr
    global sort
    global sliders
    for button in buttons:
        button.draw(window)
        if button.get_clicked():
            if button == reset_button:
                arr = random_arr(arrlength, arrmax, arrmin)
            elif button == toggle_sort_button:
                sort += 1
                if sort > 4:
                    sort = 1
            else:
                print("Unknown button clicked")

    for slider in sliders:
        global liner
        global lineg
        global lineb
        global speed
        slider.tick(events)
        slider.draw(window)
        if slider == red_slider:
            liner = slider.get_value()
        elif slider == green_slider:
            lineg = slider.get_value()
        elif slider == blue_slider:
            lineb = slider.get_value()
        elif slider == speed_slider:
            speed = round(slider.get_value())
    

sort = 3
speed = 5

buttons = []

button_height = height/25
reset_button = ui.Button(width-button_height*2, button_height*.2, width/20, button_height, "Reset")
toggle_sort_button = ui.Button(width-button_height*6, button_height*.2, width/15, button_height, "Toggle Sort")

buttons.append(reset_button)
buttons.append(toggle_sort_button)

sliders = []
slider_width = width/15*2
slider_height = height/25*2

red_slider = ui.Slider(width/2, height/2, slider_width, slider_height, (0, 255), 1, "red", 255)
red_slider.set_theme("red")
blue_slider = ui.Slider(width/2+slider_width, height/2, slider_width, slider_height, (0, 255), 1, "blue", 255)
blue_slider.set_theme("blue")
green_slider = ui.Slider(width/2, height/2+slider_height, slider_width, slider_height, (0, 255), 1, "green", 255)
green_slider.set_theme("green")
speed_slider = ui.Slider(width-slider_width, height-slider_height, slider_width, slider_height, (1, 50), 1, "speed", 1)

# sliders.append(red_slider)
# sliders.append(blue_slider)
# sliders.append(green_slider)
sliders.append(speed_slider)

arrlength = int(width/4)
arrmax = int(height/4)
arrmin = 0

steps_per_frame = 1
arr = random_arr(arrlength, arrmax, arrmin)
def draw_frame(arr):
    global playing
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                pygame.quit()
                break

            if event.key == pygame.K_RETURN:
                #arr = shuffle(arr, 20)
                arr = random_arr(arrlength, arrmax, arrmin)
    window.fill(BACKGROUND_COLOR)
    draw_arr(arr)
    tick_buttons(events)
    pygame.display.flip()
    clock.tick(fps)

playing = True
while playing:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            playing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break

            if event.key == pygame.K_RETURN:
                #arr = shuffle(arr, 20)
                arr = random_arr(arrlength, arrmax, arrmin)
    window.fill(BACKGROUND_COLOR)

    draw_arr(arr)
    if not sorted(arr):
        for i in range(steps_per_frame):
            if sort == 1:
                bubble_sort_step(arr)
            elif sort == 2:
                selection_sort_step(arr)
            elif sort == 3:
                merge_sort_step(arr, 0)
            else:
                bogo_sort_step(arr)
    
    tick_buttons(events)



    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
