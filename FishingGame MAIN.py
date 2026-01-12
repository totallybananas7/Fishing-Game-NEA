#imports all vital libraries for the game
import sys
from multiprocessing.connection import \
    default_family

import pygame
import random
from sys import exit
sys.setrecursionlimit(2000)
pygame.init()
global screen
screen = pygame.display.set_mode((1280, 720)) #sets the game window size

pygame.display.set_caption("Fishing Game") #sets the title for the game in the window
FPS = 60 #sets frames per second
Clock = pygame.time.Clock()

#TIPS:
#USE FORWARD SLASHES FOR FILE PATHS
#REMEMBER FOR LOCATIONS IT GOES DEST:(X,Y)
#WHEN LOADING GAME SPRITES, USE THE .convert_alpha() AT THE END TO CONVERT TO A FILE TYPE PYGAME LIKES MORE
#spritename = pygame.transform.scale(spritename, (x,y)) will scale the sprite size

# Main menu and fadeout

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

def fadeout(fadespeed=1): #defines fadeout function to have a smooth transition and sets the speed of it to 1
    fade = pygame.Surface((1280, 720)) #creates blank surface the size of the screen
    fade.fill((0, 0, 0)) #fills entire surface to black
    for alpha in range(0, 255, fadespeed): #controls how visible the black overlay becomes over time
        fade.set_alpha(alpha) #alpha tells the game how opaque the black surface should be
        screen.blit(fade, (0, 0)) #draws the black overlay onto the screen
        pygame.display.update() #updates the game
        pygame.time.delay(10) #waits 10ms before continuing to the next loop

# Main game
def main_game(): #all game stuff goes in here
    game_running = True #sets main game loop

# Main game loading - sprites and variable set up

    Foreground = pygame.image.load("Assets/Background stuff/foreground.png").convert_alpha()  # loads fg

    weather_list = ["Clear","Raining","Snowing","Fog"] #sets the weathers
    current_weather = weather_list[0] #sets default weather to clear
    weather_duration = random.randint(8000,8001) #creates the weather duration variable used in the while loop between 3 and 7 minutes
    last_weather_tick = pygame.time.get_ticks()

    day = True #sets time to day
    daynight_duration = 16000 #sets how long a day and a night is (600000 is 10 minutes)
    last_clock_tick = pygame.time.get_ticks()

    Sunny_Sky_Day = pygame.image.load("Assets/Background stuff/background_day_sunny.png").convert_alpha()
    Rainy_Sky_Day = pygame.image.load("Assets/Background stuff/background_day_rain.png").convert_alpha()
    FogSnow_Sky_Day = pygame.image.load("Assets/Background stuff/background_day_fog_snow.png").convert_alpha()
    Clear_Sky_Night = pygame.image.load("Assets/Background stuff/background_night.png").convert_alpha()
    Rainy_Sky_Night = pygame.image.load("Assets/Background stuff/background_night_rain.png").convert_alpha()
    FogSnow_Sky_Night = pygame.image.load("Assets/Background stuff/background_night_fog_snow.png").convert_alpha()
    cloud_sunny_1 = pygame.image.load("Assets/Background stuff/cloud_sunny_1.png").convert_alpha()
    cloud_sunny_2 = pygame.image.load("Assets/Background stuff/cloud_sunny_2.png").convert_alpha()
    cloud_sunny_3 = pygame.image.load("Assets/Background stuff/cloud_sunny_3.png").convert_alpha()
    cloud_rainy_1 = pygame.image.load("Assets/Background stuff/cloud_rain_1.png").convert_alpha()
    cloud_rainy_2 = pygame.image.load("Assets/Background stuff/cloud_rain_2.png").convert_alpha()
    cloud_rainy_3 = pygame.image.load("Assets/Background stuff/cloud_rain_3.png").convert_alpha()
    rain_particle = pygame.image.load("Assets/Background stuff/weather_rain.png").convert_alpha()
    snow_particle = pygame.image.load("Assets/Background stuff/weather_snow.png").convert_alpha()
    fog_particle = pygame.image.load("Assets/Background stuff/weather_fog.png").convert_alpha()

    weather_bg = Sunny_Sky_Day
    cloud1 = cloud_sunny_1
    cloud2 = cloud_sunny_2
    cloud3 = cloud_sunny_3
    fog = False
    rain = False
    snow = False

    cloud_1_x = 0  # sets cloud start x pos
    cloud_1_y = random.randint(1, 20)  # sets cloud start y pos
    cloud_2_x = 500
    cloud_2_y = random.randint(25, 45)
    cloud_3_x = 900
    cloud_3_y = random.randint(50, 70)

    class drop(): #creating rain class
        def __init__(self):
            self.x = random.randint(0,1280) #horizontal start point
            self.y = random.randint(-200,-100)#vertical start point
            self.speed = random.randint(10,20)#raindrop speed

        def precipitate(self):
            self.y += self.speed #moves rain based off speed
            if self.y>=740: #resets drop when off screen
                self.x = random.randint(0,1280)
                self.y = random.randint(-200,-100)

        def display(self):
            screen.blit(rain_particle,(self.x,self.y)) #displays particle

    rain_drops = [] #creates a list of falling rain
    for i in range(200): #creates 200 drops
        rain_drops.append(drop()) #adds rain drop

    class snow_drop(): #creating snow class
        def __init__(self):
            self.x = random.randint(0,1280) #horizontal start point
            self.y = random.randint(-200,-100)#vertical start point
            self.speed = random.randint(5,10)#snow speed

        def snow_precipitate(self):
            self.y += self.speed #moves snow based off speed
            if self.y>=740: #resets drop when off screen
                self.x = random.randint(0,1280)
                self.y = random.randint(-200,-100)

        def snow_display(self):
            screen.blit(snow_particle,(self.x,self.y)) #displays particle

    snow_drops = [] #creates a list of falling snow
    for i in range(200): #creates 200 drops
        snow_drops.append(snow_drop()) #adds snow drop

    player_sprites= [pygame.image.load("Assets/Character sprite sheet/male_left_stand.png").convert_alpha(), #creates list of sprites
                     pygame.image.load("Assets/Character sprite sheet/male_1_left_walk.png").convert_alpha(), #list position 1
                     pygame.image.load("Assets/Character sprite sheet/male_2_left_walk.png").convert_alpha(), #2
                     pygame.image.load("Assets/Character sprite sheet/male_3_left_walk.png").convert_alpha(), #3
                     pygame.image.load("Assets/Character sprite sheet/male_4_left_walk.png").convert_alpha(), #4
                     pygame.image.load("Assets/Character sprite sheet/male_right_stand.png").convert_alpha(), #5
                     pygame.image.load("Assets/Character sprite sheet/male_1_right_walk.png").convert_alpha(), #6
                     pygame.image.load("Assets/Character sprite sheet/male_2_right_walk.png").convert_alpha(), #7
                     pygame.image.load("Assets/Character sprite sheet/male_3_right_walk.png").convert_alpha(), #8
                     pygame.image.load("Assets/Character sprite sheet/male_4_right_walk.png").convert_alpha()] #9

    player_sprites_scaled = [] #creates new list for scaled sprites (bigger/smaller ones)
    for sprite in player_sprites: #for each sprite in the player_sprites list
        height = sprite.get_height() #get its height
        width = sprite.get_width() #get its width
        scaled_sprite = pygame.transform.scale(sprite, (width*1.8, height*1.8)) #scale it up by 1.8
        player_sprites_scaled.append(scaled_sprite) #add it to the new scaled list

    player_sprite_count = 5  # creates value to iterate through the animation list above, with the player facing right once spawned
    player_speed = 5
    player_x_coordinate = 100
    animation_timer = 0
    animation_speed = 9 #sets how quick the animations for the player will play
    D = False
    player_y_coordinate = 0

    background_musics= [pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - On the boat.mp3"), #0 Day Clear
                        pygame.mixer.Sound("Assets/Background stuff/Star Wars - Kamino Theme.mp3"), #1 Day Rain
                        pygame.mixer.Sound("Assets/Background stuff/C418 - Sweden - Minecraft Volume Alpha.mp3"), #2 Day Fog
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Diver.mp3"), #3 Day Snow
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Night Diving.mp3"), #4 Night Clear
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - The Blue Hole.mp3"), #5 Night Rain
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Darker Trenches.mp3"), #6 Night Fog
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Ice Level (Preserved Realm).mp3"), #7 Night Snow
                        pygame.mixer.Sound("Assets/Shop/Shop music.mp3")] #8 shop music

    for music in background_musics:
        music.set_volume(0.05) #sets each bg musics volume to 50%

    current_background_music = None #creates variable to store current music playing
    current_background_music_index = -1 #creates variable to store current music playing's position for the bg music's index
    new_background_music_index = 0 #creates variable to store the next music's index in the bg music list

    #creating fonts for the inv and loading images
    board = pygame.image.load("Assets/Menus/board.png").convert_alpha()
    hotbar = pygame.image.load("Assets/Menus/hotbar.png").convert_alpha()
    Weight_font = pygame.font.Font("PressStart2P-Regular.ttf", 10)
    Money_font = pygame.font.Font("PressStart2P-Regular.ttf", 10)
    Clock_font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    Weather_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    Weather_font_colour = "aqua"
    Fishdex_font = pygame.font.Font("PressStart2P-Regular.ttf", 9)

    minutes = [00, 10, 20, 30, 40, 50] #list of possible minutes the clock can display
    minute_hand = 00  # creates value for minute list above, starting at 00
    hour_hand = 6  # sets hour to 6AM
    clock_tick_length = 8333  # 8.33s per ingame 10 minutes, means each full day is 20m long (8333mm is 8.33s)
    minute_display = "00" #sets default minute display to 00
    hour_display = "6" #sets default hour display to 6AM

    inventory_open = False #creates variable used later for checking if the inv is open
    inventory = pygame.image.load("Assets/Menus/inventory.png").convert_alpha() #loads inventory bg
    inventory_font = pygame.font.Font("PressStart2P-Regular.ttf", 20) #loads font for txt in inv

    shop_bg = pygame.image.load("Assets/Shop/background_shop.png").convert_alpha()
    npc_front = pygame.image.load("Assets/Shop/Corkah_front.png").convert_alpha()
    npc_left = pygame.image.load("Assets/Shop/Corkah_left.png").convert_alpha()
    space = pygame.image.load("Assets/Shop/space.png").convert_alpha()
    shop_menu = pygame.image.load("Assets/Shop/shop interface.png").convert_alpha()
    back_button = pygame.image.load("Assets/Shop/back_button.png").convert_alpha()
    in_shop = False

# MAIN GAME LOOP
    while game_running:

# Weather and time
        current_time = pygame.time.get_ticks() #gets current game tick

        if current_time - last_clock_tick >= clock_tick_length: #if enough time has passed
            last_clock_tick = current_time #resets timer

            minute_hand +=1 #update minute hand every 8.33s

            if minute_hand > 5: #if an ingame hour has passed..
                minute_hand = 00
                minute_display = str(minutes[minute_hand]) #displays clocks minutes as the location of the item in the minutes list based off the minute_hand variable
                hour_hand +=1 #updates hour

                if hour_hand > 23: #if midnight
                    hour_hand = 00 #resets hour count

            minute_display = str(minutes[minute_hand]) #displays clock minutes
            hour_display = str(hour_hand) #displays clock hour

            if 6<= hour_hand < 18: #if between 6am and 6pm, day is true
                day = True
            else:
                day = False

        if current_time - last_weather_tick >= weather_duration: #if the time passed is equal to the random weather duration
            last_weather_tick = current_time #resets timer
            weather_duration = random.randint(180000,420000)  # creates the new weather duration variable between 3 (180000)and 7 (420000) minutes
            new_weather = random.choice(weather_list)
            fog = False
            rain = False
            snow = False
            while new_weather == current_weather: #checks if the weather has changed
                new_weather = random.choice(weather_list) #if it hasn't, it reselects again
            current_weather = new_weather #updates weather

            if current_weather == "Clear": #updating background
                if day == True: #if its day, set sprites to daytime variation
                    weather_bg = Sunny_Sky_Day
                    cloud1 = cloud_sunny_1
                    cloud2 = cloud_sunny_2
                    cloud3 = cloud_sunny_3
                    new_background_music_index = 0 #sets new bg music
                    Weather_font_colour = "aqua" #sets weather display GUI font colour to aqua
                else:
                    weather_bg = Clear_Sky_Night #else its night, updates sprites to nighttime variation
                    cloud1 = cloud_sunny_1
                    cloud2 = cloud_sunny_2
                    cloud3 = cloud_sunny_3
                    new_background_music_index = 4
                    Weather_font_colour = "aqua"

            elif current_weather == "Raining":
                if day == True:
                    weather_bg = Rainy_Sky_Day
                    cloud1 = cloud_rainy_1
                    cloud2 = cloud_rainy_2
                    cloud3 = cloud_rainy_3
                    rain = True
                    new_background_music_index = 1
                    Weather_font_colour = "dodgerblue"
                else:
                    weather_bg = Rainy_Sky_Night
                    cloud1 = cloud_rainy_1
                    cloud2 = cloud_rainy_2
                    cloud3 = cloud_rainy_3
                    rain = True
                    new_background_music_index = 5
                    Weather_font_colour = "dodgerblue"

            elif current_weather == "Fog":
                if day == True:
                    weather_bg = FogSnow_Sky_Day
                    fog = True
                    new_background_music_index = 2
                    Weather_font_colour = "azure3"
                else:
                    weather_bg = FogSnow_Sky_Night
                    fog = True
                    new_background_music_index = 6
                    Weather_font_colour = "azure3"

            elif current_weather == "Snowing":
                if day == True:
                    weather_bg = FogSnow_Sky_Day
                    snow = True
                    new_background_music_index = 3
                    Weather_font_colour = "azure"
                else:
                    weather_bg = FogSnow_Sky_Night
                    snow = True
                    new_background_music_index = 7
                    Weather_font_colour = "azure"


        if in_shop == True:
            screen.blit(shop_bg,(0,0))
            screen.blit(npc_left,(900,385))
        else:
            screen.blit(weather_bg, (0, 0))
            screen.blit(Foreground,(0,0))

        if in_shop == False: #if the player is outside
            if current_weather == "Clear" or current_weather == "Raining":
                screen.blit(cloud1,(cloud_1_x,cloud_1_y))  # displays cloud
                cloud_1_x += 1  # moves cloud 1 pixel left
                if cloud_1_x >= 1280:  # checks to see if cloud to far right off-screen
                    cloud_1_x = 0  # moves cloud back to the start
            if current_weather == "Clear" or current_weather == "Raining":
                screen.blit(cloud2,(cloud_2_x,cloud_2_y))
                cloud_2_x += 0.4
                if cloud_2_x >= 1280:
                    cloud_2_x = 0
            if current_weather == "Clear" or current_weather == "Raining":
                screen.blit(cloud3,(cloud_3_x,cloud_3_y))
                cloud_3_x += 0.8
                if cloud_3_x >= 1280:
                    cloud_3_x = 0
            if fog == True:
                screen.blit(fog_particle,(0,0))
            if rain == True:
                for drop in rain_drops: #for each active rain drop
                    drop.precipitate() #move it
                    drop.display() #display it
            if snow == True:
                for snow_drop in snow_drops:
                    snow_drop.snow_precipitate()
                    snow_drop.snow_display()

            if new_background_music_index != current_background_music_index: #switch music only if it has changed
                if current_background_music != None:
                    current_background_music = current_background_music.fadeout(3000) #fade out current bg music for 3s

                current_background_music = background_musics[new_background_music_index] #selects music
                current_background_music.play(-1) #play new music
                current_background_music_index = new_background_music_index #updates tracker
        else: #if in shop
            if current_background_music_index != 8:
                if current_background_music != None:
                    current_background_music.fadeout(3000)

                current_background_music = background_musics[8] #set music
                current_background_music.play(-1) #play shop music
                current_background_music_index = 8 #update tracker


# Player movement and input

        for event in pygame.event.get(): #handles quitting and debug code
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at",menu_mouse_pos_test)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key = pygame.key.get_pressed() #records the keyboard/mouse for any inputs

        show_space = False
        moving = False

        if key[pygame.K_a]:
            moving = True

            if D == True: #if switching from right to left
                player_sprite_count = 5 #update sprite count to left facing
                D = False #no longer moving right

            animation_timer +=1 #logic for updating sprite animation
            if animation_timer > animation_speed:
                player_sprite_count +=1
                animation_timer = 0

            player_x_coordinate -= player_speed #move player

            if player_x_coordinate < -30: #if too far left
                player_x_coordinate += player_speed #move player back

            if player_sprite_count > 9: #if end of animation cycle
                player_sprite_count = 6

        elif key[pygame.K_d]:
            moving = True
            D = True #moving right

            animation_timer += 1 #logic for updating sprite animation
            if animation_timer > animation_speed:
                player_sprite_count += 1
                animation_timer = 0

            player_x_coordinate += player_speed #move player

            if in_shop == False: #if outside
                if player_x_coordinate>640: #if at end of pier
                    player_x_coordinate -= player_speed #move player back
            elif in_shop == True: #if inside
                if player_x_coordinate > 560: #if at store counter
                    player_x_coordinate -= player_speed #move player back

            if player_sprite_count > 4: #if end of animation cycle
                player_sprite_count = 0


        elif key[pygame.K_SPACE]:
            if in_shop == False:
                if 170 <= player_x_coordinate <= 260: #if not in shop and near door
                    fadeout(fadespeed=1) #fadeout
                    in_shop = True
            elif in_shop == True:
                if 100 <= player_x_coordinate <= 300:
                    fadeout(fadespeed=1)
                    in_shop = False
            elif in_shop == True:
                if 500 <= player_x_coordinate <= 700:
                    screen.blit(shop_menu,(160,90))

        if moving == False: #if stationary
            if 1<= player_sprite_count <= 4: #if last facing right
                player_sprite_count = 0 #set to stationary right sprite
            elif 6 <= player_sprite_count <= 9: #opposite to above
                player_sprite_count = 5

        if in_shop == False:
            if 170 <= player_x_coordinate <= 260:
                show_space = True #if outside and near door, show space indicator
        elif in_shop == True:
            if 100 <= player_x_coordinate <= 300:
                show_space = True #if inside and near door, show space indicator
        elif 500 <= player_x_coordinate <= 700:
            show_space = True #if inside and near counter, show space indicator

        if in_shop == False:
            player_y_coordinate = 265
            screen.blit(player_sprites[player_sprite_count],(player_x_coordinate,player_y_coordinate)) #displays sprite
        else:
            player_y_coordinate = 395
            screen.blit(player_sprites_scaled[player_sprite_count],(player_x_coordinate,player_y_coordinate)) #displays sprite but scaled up a bit and y changed

        if show_space == True: #if near interactable area
            screen.blit(space, (player_x_coordinate+120,player_y_coordinate)) #displays space indicator near player


# Inventory/GUI

        if key[pygame.K_e]: #if the player opens the inventory
            inventory_open = True

        if inventory_open == True:
            dim_overlay = pygame.Surface((1280, 720)) #creates a new screen the size of the window
            dim_overlay.set_alpha(140) #sets transparency of the new screen
            dim_overlay.fill((0, 0, 0)) #sets the new screen to black
            screen.blit(dim_overlay, (0, 0)) #puts the faded new screen to make the background darker to bring more contrast to inv

            #displays inv and text
            screen.blit(inventory,(160,90))
            screen.blit(inventory_font.render("Money:", False, "yellow"), (175,107))
            screen.blit(inventory_font.render("Weight:", False, "yellow"), (480,107))
            screen.blit(inventory_font.render("Fishdex:", False, "yellow"), (780,107))
            screen.blit(inventory_font.render("Fish:", False, "yellow"), (175,145))
            screen.blit(inventory_font.render("Quantity:", False, "yellow"), (480,145))
            screen.blit(inventory_font.render("Sell Price:", False, "yellow"), (780, 145))

            inv_mouse_pos = pygame.mouse.get_pos() #gets mouse pos
            x, y = inv_mouse_pos #gets x and y variables of mouse pos
            if 1075<=x<=1110 and 100<=y<=130: #if near the X button
                if event.type == pygame.MOUSEBUTTONDOWN: #if mouse clicked
                    inventory_open = False #inv is closed

        else:
            ingame_clock = hour_display+":"+minute_display

            screen.blit(board,(1080,650)) #bottom right (weight)
            screen.blit(Weight_font.render("Weight placeholder", False, "yellow"), (1087, 677))

            screen.blit(board,(1080,5)) #top right (time)
            screen.blit(Clock_font.render(ingame_clock, False, "yellow"),(1100,25))

            screen.blit(board,(1080,75)) #second top right (weather)
            screen.blit(Weather_font.render(current_weather, False, Weather_font_colour), (1105, 97))

            screen.blit(board,(1080,145)) #third top right (fishdex)
            screen.blit(Fishdex_font.render("Fishdex placeholder", False, "yellow"),(1092,170))

            screen.blit(board,(10,5)) #top left (money)
            screen.blit(Money_font.render("Money placeholder", False, "yellow"), (20, 32))

        screen.blit(hotbar,(576,650)) #bottom middle (hotbar)

        pygame.display.update()
        Clock.tick(FPS)

# run main menu
main_menu_loop()
