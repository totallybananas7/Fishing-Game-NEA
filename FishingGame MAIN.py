#imports all vital libraries for the game
import sys

import pygame
import time
import random
from sys import exit
sys.setrecursionlimit(2000)
pygame.init()
global screen
screen = pygame.display.set_mode((1280, 720)) #sets the game window size

pygame.display.set_caption("Fishing Game") #sets the title for the game in the window
FPS = 60 #sets frames per second
Clock = pygame.time.Clock()

# ------------------------------------------------------------------------------------------------------------------
#TIPS:
#USE FORWARD SLASHES FOR FILE PATHS
#REMEMBER FOR LOCATIONS IT GOES DEST:(X,Y)
#WHEN LOADING GAME SPRITES, USE THE .convert_alpha() AT THE END TO CONVERT TO A FILE TYPE PYGAME LIKES MORE

def main_menu_loop():
    Main_menu_running = True
    BG = pygame.image.load("Assets/Menus/Main_menu_background.png").convert_alpha() #loads background image once
    Text_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

    main_menu_background_music = pygame.mixer.Sound("Assets/Menus/Main_menu_background_music.mp3") #sets main menu background music file as a variable
    main_menu_background_music.set_volume(0.05) #sets MMBMF volume to 50%
    main_menu_background_music.play(-1) #plays the MMBMF infinitely

    while Main_menu_running: #all main menu logic here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() #handles X for quit in window
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at", menu_mouse_pos_test) #debugging tool, shows me where I clicked in terminal

            main_menu_font_colourLG = "Yellow"
            main_menu_font_colourNG = "Yellow"
            main_menu_font_colourS = "Yellow"
            main_menu_font_colourEG = "Yellow"

            menu_mouse_pos = pygame.mouse.get_pos()
            x, y = menu_mouse_pos

            if 530<=x<=750 and 279<=y<=325: #checks to see if mouse coords are nearby text
                main_menu_font_colourLG = "Green"
            if 530<=x<=750 and 388<=y<=435:
                main_menu_font_colourNG = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN: #if player clicks on new game button
                    Main_menu_running = False #stops main menu
                    main_menu_background_music.fadeout(6500) #fades music out over 6.5 seconds
                    fadeout() #goes to the fadeout subroutine for a smooth transition
                    main_game() #loads game background

            if 530<=x<=750 and 493<=y<=541:
                main_menu_font_colourS = "Green"
            if 530<=x<=750 and 600<=y<=647:
                main_menu_font_colourEG = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN: #if user clicks exit game button...
                    main_menu_font_colourEG = "Red"
                    pygame.quit()
                    exit()  #quit game

        # draws background
        screen.blit(BG, (0, 0))

        # draws menu text
        screen.blit(Text_font.render("Load Game", False, main_menu_font_colourLG), (555, 294))
        screen.blit(Text_font.render("New Game", False, main_menu_font_colourNG), (565, 403))
        screen.blit(Text_font.render("Settings", False, main_menu_font_colourS), (563, 509))
        screen.blit(Text_font.render("Exit Game", False, main_menu_font_colourEG), (555, 616))

        # updates display
        pygame.display.update()
        Clock.tick(FPS)

# ------------------------------------------------------------------------------------------------------------------
def fadeout(fadespeed=1): #defines fadeout function to have a smooth transition and sets the speed of it to 1
    fade = pygame.Surface((1280, 720)) #creates blank surface the size of the screen
    fade.fill((0, 0, 0)) #fills entire surface to black
    for alpha in range(0, 255, fadespeed): #controls how visible the black overlay becomes over time
        fade.set_alpha(alpha) #alpha tells the game how opaque the black surface should be
        screen.blit(fade, (0, 0)) #draws the black overlay onto the screen
        pygame.display.update() #updates the game
        pygame.time.delay(20) #waits 20ms before continuing to the next loop

def main_game(): #all game stuff goes in here
    game_running = True #sets main game loop

#-----------SPRITE LOADING------------
    Sky = pygame.image.load("Assets/Background stuff/background_day_sunny.png").convert_alpha()  # loads bg
    Foreground = pygame.image.load("Assets/Background stuff/foreground.png").convert_alpha()  # loads fg

# ---------- loading cloud sprites -----------
    cloud1 = pygame.image.load("Assets/Background stuff/cloud_sunny_1.png").convert_alpha()  # loads cloud
    cloud_1_x = 0  # sets cloud start x pos
    cloud_1_y = random.randint(1, 25)  # sets cloud start y pos
    cloud2 = pygame.image.load("Assets/Background stuff/cloud_sunny_2.png").convert_alpha()
    cloud_2_x = 500
    cloud_2_y = random.randint(35, 65)
    cloud3 = pygame.image.load("Assets/Background stuff/cloud_sunny_3.png").convert_alpha()
    cloud_3_x = 1000
    cloud_3_y = random.randint(75, 95)
# ---------- loading cloud sprites end -----------

# ---------- loading player sprites --------------


# -----------SPRITE LOADING END-----------

    #------------ MAIN GAME LOOP ---------------
    while game_running:
        screen.blit(Sky, (0, 0))
        screen.blit(Foreground, (0, 0))

# ---------- loading cloud sprites -----------
        screen.blit(cloud1, (cloud_1_x, cloud_1_y))  # displays cloud
        cloud_1_x += 1  # moves cloud 1 pixel left
        if cloud_1_x >= 1280:  # checks to see if cloud to far right off screen
            cloud_1_x = 0  # moves cloud back to the start

        screen.blit(cloud2, (cloud_2_x, cloud_2_y))
        cloud_2_x += 0.4
        if cloud_2_x >= 1280:
            cloud_2_x = 0

        screen.blit(cloud3, (cloud_3_x, cloud_3_y))
        cloud_3_x += 0.8
        if cloud_3_x >= 1280:
            cloud_3_x = 0
# ------------ loading cloud sprites -----------

        for event in pygame.event.get():  # tells me where mouse is clicked, allows X to quit game without error
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at", menu_mouse_pos_test)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



def player_movement():

    player_sprites= [pygame.image.load("Assets/Character sprite sheet/male_left_stand.png").convert_alpha(), #creates list of sprites
                    pygame.image.load("Assets/Character sprite sheet/male_1_left_walk.png").convert_alpha(), #1
                    pygame.image.load("Assets/Character sprite sheet/male_2_left_walk.png").convert_alpha(), #2
                    pygame.image.load("Assets/Character sprite sheet/male_3_left_walk.png").convert_alpha(), #3
                    pygame.image.load("Assets/Character sprite sheet/male_4_left_walk.png").convert_alpha(), #4
                    pygame.image.load("Assets/Character sprite sheet/male_right_stand.png").convert_alpha(), #5
                    pygame.image.load("Assets/Character sprite sheet/male_1_right_walk.png").convert_alpha(), #6
                    pygame.image.load("Assets/Character sprite sheet/male_2_right_walk.png").convert_alpha(), #7
                    pygame.image.load("Assets/Character sprite sheet/male_3_right_walk.png").convert_alpha(), #8
                    pygame.image.load("Assets/Character sprite sheet/male_4_right_walk.png").convert_alpha()] #9

    p_sprite_count = 5 #creates value to iterate through the animation list above, with the player facing right once spawned
    player_speed = 30
    player_x_coordinate = 100

    run = True
    while run:
        for event in pygame.event.get(): #handles quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            key = pygame.key.get_pressed() #records the keyboard/mouse for any inputs

            if key[pygame.K.d]: #if D is pressed...
                player_sprite_count += 1 #update sprite by one
                if player_sprite_count > 9: #if sprite has done a full walk cycle...
                    player_sprite_count = 6 #set back to first step of cycle

            elif key[pygame.K.a]:
                player_sprite_count += 1
                if player_sprite_count > 4:
                    player_sprite_count = 1

            else: #if the player is not moving...
                if player_sprite_count >= 1:
                    if player_sprite_count <=4:
                        player_sprite_count = 0
                elif player_sprite_count >=6:
                    if player_sprite_count <=9:
                        player_sprite_count = 5

            screen.blit(player_sprites[p_sprite_count], (player_x_coordinate, 300))

    pygame.display.update()
    Clock.tick(FPS)







# run main menu
main_menu_loop()
