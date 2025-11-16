#imports all vital libraries for the game
import pygame
import time
import random
from sys import exit

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

def main_menu_loop():
    Main_menu_running = True
    BG = pygame.image.load("Assets/Menus/Main_menu_background.png") #loads background image once
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
                    load_game_background_loop() #loads game background

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

def load_game_background_loop():
    game_background_running = True
    Sky = pygame.image.load("Assets/Background stuff/background_day_sunny.png")
    Foreground = pygame.image.load("Assets/Background stuff/foreground.png")

    cloud1 = pygame.image.load("Assets/Background stuff/cloud_sunny_1.png")
    cloud2 = pygame.image.load("Assets/Background stuff/cloud_sunny_2.png")
    cloud3 = pygame.image.load("Assets/Background stuff/cloud_sunny_3.png")

    cloud_1_x = 0 #cloud starts at left most point of sky
    cloud_1_y = random.randint(0,80) #clouds starts at random y level in sky for randomness
    cloud_1_vel = 4 #cloud speed

    cloud_2_trigger = random.randint(300,600)
    cloud_2_x = 0
    cloud_2_y = random.randint(0,80)
    cloud_2_vel = 4

    cloud_3_trigger = random.randint(600,900)
    cloud_3_x = 0
    cloud_3_y = random.randint(0,80)
    cloud_3_vel = 4

    while game_background_running:
        screen.blit(Sky, (0, 0))
        screen.blit(Foreground, (0, 0))

        for event in pygame.event.get(): #tells me where mouse is clicked, allows X to quit game without error
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at", menu_mouse_pos_test)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

#---------------CLOUD CODE---------------------
        screen.blit(cloud1, (cloud_1_x, cloud_1_y)) #spawns first cloud
        cloud_1_x += cloud_1_vel #updates cloud location for velocity

        if cloud_1_x >= 1280: #if too far right...
            cloud_1_x = 0 #sets cloud back to left side
            cloud_1_y = random.randint(0,80) #sets clouds random y level
            cloud_2_trigger = random.randint(300,600)

        if cloud_1_x > cloud_2_trigger: #is cloud 1 far enough to spawn cloud 2?
            screen.blit(cloud2, (cloud_2_x, cloud_2_y))
            cloud_2_x += cloud_2_vel

        if cloud_2_x >= 1280: #if cloud 2 too far right...
            cloud_2_x = 0 #sets cloud 2 back to left side
            cloud_2_y = random.randint(0,80) #sets cloud 2 random y level
            cloud_3_trigger = random.randint(600,900)

        if cloud_2_x > cloud_3_trigger:
            screen.blit(cloud3, (cloud_3_x, cloud_3_y))
            cloud_3_x += cloud_3_vel

        if cloud_3_x >= 1280: #if cloud 3 too far right...
            cloud_3_x = 0 #sets cloud 3 back to left side
            cloud_3_y = random.randint(0,80) #sets cloud 3 random y level
#---------------END OF CLOUD CODE-------------------

        pygame.display.update()
        Clock.tick(FPS)



# run main menu
main_menu_loop()
