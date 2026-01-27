#imports all vital libraries for the game
import sys

import pygame
import random
from sys import exit
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
                     pygame.image.load("Assets/Character sprite sheet/male_4_right_walk.png").convert_alpha(), #9
                     pygame.image.load("Assets/Character sprite sheet/male_holding_rod.png").convert_alpha()] #10

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
    Weight_font = pygame.font.Font("PressStart2P-Regular.ttf", 11)
    Money_font = pygame.font.Font("PressStart2P-Regular.ttf", 14)
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
    npc_left = pygame.image.load("Assets/Shop/Corkah_left.png").convert_alpha()
    space = pygame.image.load("Assets/Shop/space.png").convert_alpha()
    shop_menu = pygame.image.load("Assets/Shop/shop interface.png").convert_alpha()
    back_sell_button = pygame.image.load("Assets/Shop/back_button.png").convert_alpha()
    back_sell_font = pygame.font.Font("PressStart2P-Regular.ttf",20)
    in_shop = False #instantiate variable for checking if in shop
    in_shop_menu = False #instantiate variable for checking if in shop menu
    dim_overlay = pygame.Surface((1280,720))  # creates a new screen the size of the window
    dim_overlay.set_alpha(140)  # sets transparency of the new screen
    dim_overlay.fill((0,0,0))  # sets the new screen to black
    shop_upgrade_font = pygame.font.Font("PressStart2P-Regular.ttf",25)
    shop_bait_font = pygame.font.Font("PressStart2P-Regular.ttf",20)
    weight_shop_sprite = pygame.image.load("Assets/Shop/weight_upgrade.png").convert_alpha()
    can_buy = True #instantiates can buy variable for later in the shop, so you cant buy multiple rods every next frame
    inv_bait_amount_font = pygame.font.Font("PressStart2P-Regular.ttf",10)

    class Rod: #declaring rod class
        def __init__(self, name, sprite, fishing_speed, luck, cost, upgrade_index): #constructor method for rod
            self.name = name
            self.sprite = sprite
            self.fishing_speed = fishing_speed
            self.luck = luck
            self.cost = cost
            self.upgrade_index = upgrade_index

            w, h = sprite.get_size()
            self.hand_sprite = pygame.transform.scale(sprite, (w*1.8, h*1.8))

    class Bait:
        def __init__(self, name, sprite, luck, cost): #creates parent class for bait
            self.name = name
            self.sprite = sprite
            self.luck = luck
            self.cost = cost

    Starter_rod = Rod("Starter rod", pygame.image.load("Assets/Rods/1.Starter_rod.png").convert_alpha(), 0, 1, 0, None) #instantiating objects of class rod
    Hobbyist_rod = Rod("Hobbyist rod", pygame.image.load("Assets/Rods/2.Hobbyist_rod.png").convert_alpha(), 1000, 2, 100, 0)
    Commercial_rod = Rod("Commercial rod", pygame.image.load("Assets/Rods/3.Commercial_rod.png").convert_alpha(), 2000, 3, 200, 1)
    Sturdy_rod = Rod("Sturdy rod", pygame.image.load("Assets/Rods/4.Sturdy_rod.png").convert_alpha(), 3000, 4, 350, 2)
    Rod_of_the_sea = Rod("Rod of the sea", pygame.image.load("Assets/Rods/5.Rod_of_the_sea.png").convert_alpha(), 4000, 5, 600, 3)
    Rod_of_the_ocean = Rod(" Rod of the ocean", pygame.image.load("Assets/Rods/6.Rod_of_the_ocean.png").convert_alpha(), 5000, 7, 1000, 4)
    Amethyst_rod = Rod("Amethyst rod", pygame.image.load("Assets/Rods/7.Amethyst_rod.png").convert_alpha(), 6000, 10, 1500, 5)
    Australium_rod = Rod("Australium rod", pygame.image.load("Assets/Rods/8.Australium_rod.png").convert_alpha(), 7000, 14, 2200, 6)
    Lightsaber_rod = Rod("Lightsaber rod", pygame.image.load("Assets/Rods/9.Lightsaber_rod.png").convert_alpha(), 8000, 20, 3000, 7)
    Hellfire_rod = Rod("Hellfire rod", pygame.image.load("Assets/Rods/10.Hellfire_rod.png").convert_alpha(), 9000, 25, 4000, 8)
    God_rod = Rod("God rod", pygame.image.load("Assets/Rods/11.God_rod.png").convert_alpha(), 10000, 29, 6000, 9)

    shop_upgrade_path = [Hobbyist_rod,Commercial_rod,Sturdy_rod,Rod_of_the_sea,Rod_of_the_ocean,Amethyst_rod,Australium_rod,Lightsaber_rod,Hellfire_rod,God_rod] #so the shop displays the next rod the player can buy, excludes starter rod

    No_bait = Bait("No bait",pygame.image.load("Assets/Rods/out_of_bait.png").convert_alpha(), 0, 0) #all baits
    Worm_bait = Bait("Worm bait",pygame.image.load("Assets/Rods/worm_bait.png").convert_alpha(), 3, 100)
    Glow_bait = Bait("Glow bait",pygame.image.load("Assets/Rods/glow_bait.png").convert_alpha(), 6, 200)
    Chum_bait = Bait("Chum bait",pygame.image.load("Assets/Rods/chum_bait.png").convert_alpha(), 9, 400)
    Rainbow_bait = Bait("Rainbow bait",pygame.image.load("Assets/Rods/rainbow_bait.png").convert_alpha(), 14, 900)

    class Player:
        def __init__(self,money,weight,held_rod,held_bait,bait_amount,max_weight,weight_upgrade_cost,fish_start_time,wait_time,reaction_start_time,fish_state,cast,fish_progress,bar_height,fish_height,fish_move_speed,fish_target): #makes player class with stats

            #player stats and shop
            self.money = money
            self.weight = weight
            self.held_rod = held_rod
            self.held_bait = held_bait
            self.bait_amount = bait_amount
            self.max_weight = max_weight
            self.weight_upgrade_cost = weight_upgrade_cost

            #fishing minigame variables
            self.fish_start_time = fish_start_time
            self.wait_time = wait_time
            self.reaction_start_time = reaction_start_time
            self.fish_state = fish_state
            self.cast = cast
            self.fish_progress = fish_progress
            self.bar_height = bar_height
            self.fish_height = fish_height
            self.fish_move_speed = fish_move_speed
            self.fish_target = fish_target

        def get_fishing_speed(player):
            return player.held_rod.fishing_speed #returns the players fishing speed
        def get_fishing_luck(player):
            return player.held_rod.luck + player.held_bait.luck #returns players total luck stat

    player = Player(20000,0,Starter_rod,No_bait,0,50,100,0,0,0,"idle",False,40,310,345,0,random.randint(45,590)) #instantiate object of class player

    def shop_next_rod(player):
        if player.held_rod.upgrade_index == None: #if the player has the starter rod
            return shop_upgrade_path[0] #next rod to purchase is Hobbyist Rod
        next_rod = player.held_rod.upgrade_index+1 #work out index of next rod to buy
        if next_rod < len(shop_upgrade_path): #prevents index going past length of shop list
            return shop_upgrade_path[next_rod] #returns next rod upgrade
        return None #gives nothing if player has final rod

    def buy_next_rod(player):
        next_rod = shop_next_rod(player) #find next rod the player can buy
        if next_rod and player.money >= next_rod.cost: #if rod exists and the player can afford it
            player.money -= next_rod.cost #take away money from player according to the rods cost
            player.held_rod = next_rod #give player new rod

    def buy_next_weight(player):
        if player.money>=player.weight_upgrade_cost: #if player has enough money
            player.money-=player.weight_upgrade_cost #take away money
            player.weight_upgrade_cost+=100 #buff price by 100
            player.max_weight+=10 #give player +10 max weight

    def buy_bait(player, bait):
        if player.money<bait.cost: #if player cannot afford
            return #do nothing
        player.money-=bait.cost #take away cost
        if player.held_bait == bait: #if the player has the same bait they are buying
            player.bait_amount+=32 #add 32 more bait
        else:
            player.held_bait = bait #change old bait to new bait
            player.bait_amount = 32 #set bait amount to 32


    alert_indicator = pygame.image.load("Assets/Fishing minigame/alert_indicator.png").convert_alpha()
    fishing_minigame_bg = pygame.image.load("Assets/Fishing minigame/fishing_minigame_bar.png").convert_alpha()
    fishing_minigame_fish = pygame.image.load("Assets/Fishing minigame/fishing_minigame_fish.png").convert_alpha()
    bobber = pygame.image.load("Assets/Fishing minigame/bobber.png").convert_alpha()
    fishing_minigame_bar = pygame.image.load("Assets/Fishing minigame/fishing_minigame_move_bar.png").convert_alpha()
    splash = pygame.mixer.Sound("Assets/Fishing minigame/Splash.mp3")  #splash sound effect
    splash.set_volume(0.05)

    def fishing_minigame(player): #begins minigame
        current_time = pygame.time.get_ticks() #gets current tick time
        bottom_y = 680  # this value does not change!! it is the bottom of the bar

        if player.fish_state == "waiting": #if waiting for a fish to bite
            if current_time - player.fish_start_time >= player.wait_time: #checks and compares wait time with time waited
                player.fish_state = "react" #reaction game starts
                player.reaction_start_time = current_time #gets time the reaction game started at
                splash.play(0)  #play sound effect

        elif player.fish_state == "react": #if the reaction game has started
            screen.blit(alert_indicator, (player_x_coordinate + 346, 380))  # displays alert symbol

            if key[pygame.K_SPACE]: #if the player presses space
                player.fish_state = "catching" #begins fishing minigame

            elif current_time - player.reaction_start_time > 1000: #if the player did not press space in time
                print("missed") #debug, prints missed in console
                player.fish_state = "idle" #sets state back to idle (not fishing)
                player.cast = False #stops fishing

        elif player.fish_state == "catching": #if in fishing minigame

            if key[pygame.K_w]: #if player pressing w
                player.bar_height -= 3  # increase progress (remember - is higher)
            else:
                player.bar_height+=3 #decrease height (remember + is lower)

            #boundaries for bar
            if player.bar_height>=590:
                player.bar_height-=3
            elif player.bar_height<=45:
                player.bar_height+=3

            #chooses where fish goes next
            if player.fish_height < player.fish_target:
                player.fish_height += player.fish_move_speed
            elif player.fish_height > player.fish_target:
                player.fish_height -= player.fish_move_speed

            if (
                (player.fish_height<player.fish_target and player.fish_height + player.fish_move_speed>=player.fish_target) #if fish is above where it wants to go, move it down
                or
                (player.fish_height > player.fish_target and player.fish_height - player.fish_move_speed <= player.fish_target) #if fish is below where it wants to go, move it up
            ):
                player.fish_height = player.fish_target
                player.fish_move_speed = random.randint(1,5)  # sets move speed to be random every time it changes direction
                player.fish_target = random.randint(45, 590)  # sets fish's new location to start moving to

                #boundaries for the fish
                if player.fish_height<45:
                    player.fish_height = 45
                elif player.fish_height>590:
                    player.fish_height = 590

            bar_rect = fishing_minigame_bar.get_rect(topleft=(870,player.bar_height)) #creates a hitbox for the moveable bar
            fish_rect = fishing_minigame_fish.get_rect(topleft=(865, player.fish_height))  # creates a hitbox for the moving fish

            if bar_rect.colliderect(fish_rect):
                player.fish_progress+=2 #if bar and fish are touching, increase progress by 2
            else:
                player.fish_progress-=2 #if not touching, decrease progress by 2

            if player.fish_progress >= 620: #if max progress reached
                player.cast = False #exits minigame
                player.fish_state = "idle"

            elif player.fish_progress <= 0: #if all progress lost
                player.cast = False
                player.fish_state = "idle"

            #blitting images
            screen.blit(dim_overlay, (0, 0))
            screen.blit(fishing_minigame_bg, (570, 45))
            screen.blit(fishing_minigame_bar, bar_rect)  # displays moveable rect at rectangle coords
            screen.blit(fishing_minigame_fish, fish_rect)  # displays fish at rectangle coords
            pygame.draw.rect(screen, (0, 255, 0), (910,bottom_y-player.fish_progress,20,player.fish_progress)) #PROGRESS DISPLAY - colour, coordinates, width+height



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


        if in_shop == True: #if in shop
            screen.blit(shop_bg,(0,0)) #display shop bg
            screen.blit(npc_left,(900,385)) #display npc
        else:
            screen.blit(weather_bg, (0, 0)) #if outside, show outside stuff
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

        show_space = False #instantiate variable for displaying interact indicator
        moving = False #checks if moving

        if player.cast == False:
            if key[pygame.K_a]: #if pressing a
                moving = True #player is moving

                if D == True: #if switching from right to left
                    player_sprite_count = 5 #update sprite count to left facing
                    D = False #no longer moving right

                animation_timer +=1 #logic for updating sprite animation
                if animation_timer > animation_speed: #if enough frames have passed to warrant a change in sprite
                    player_sprite_count +=1 #update sprite
                    animation_timer = 0 #reset frame timer

                player_x_coordinate -= player_speed #move player

                if player_x_coordinate < -30: #if too far left
                    player_x_coordinate += player_speed #move player back

                if player_sprite_count > 9: #if end of animation cycle
                    player_sprite_count = 6 #set sprite back

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
                        fadeout(fadespeed=1) #fadeout animation
                        in_shop = True #activates code for in shop
                    elif player_x_coordinate >= 550:  # if player is near the end of the pier
                        print(player.weight,player.max_weight)
                        if player.weight <= player.max_weight: #if player has inv space
                            player.cast = True
                            player.fish_state = "waiting"
                            player.fish_start_time = pygame.time.get_ticks() #gets time
                            player.wait_time = random.randint(11000-player.held_rod.fishing_speed, 11001) #calculates how long player has to wait for fish, based off fishing speed
                            player.fish_move_speed = random.randint(1,5)  # sets move speed to be random every time it changes direction
                            player.fish_target = random.randint(45, 590)  # sets fish's new location to start moving to
                            player.fish_progress = 200  # resets progress
                            player.fish_height = 345  # resets fishes height to center
                            player.bar_height = 310  # resets bar to center

                elif in_shop == True:
                    if 100 <= player_x_coordinate <= 300: #if in shop and near door
                        fadeout(fadespeed=1)
                        in_shop = False #exits shop
                    elif 500 <= player_x_coordinate <= 700:
                        in_shop_menu = True #activates menu


        if moving == False: #if stationary
            if 1<= player_sprite_count <= 4: #if last facing right
                player_sprite_count = 0 #set to stationary right sprite
            elif 6 <= player_sprite_count <= 9: #opposite to above
                player_sprite_count = 5

        if in_shop == False:
            if 170 <= player_x_coordinate <= 260:
                show_space = True #if outside and near door, show space indicator
            elif player_x_coordinate >= 550:  # if player is near the end of the pier
                show_space = True
        elif in_shop == True:
            if 100 <= player_x_coordinate <= 300:
                show_space = True #if inside and near door, show space indicator
            elif 500 <= player_x_coordinate <= 700:
                show_space = True #if inside and near counter, show space indicator


        if in_shop == False:
            player_y_coordinate = 265
            if player.cast == False:
                screen.blit(player_sprites[player_sprite_count],(player_x_coordinate,player_y_coordinate)) #displays sprite

            else:
                screen.blit(player_sprites[10], (player_x_coordinate, player_y_coordinate)) #displays sprite with hand held out
                screen.blit(player.held_rod.hand_sprite,(player_x_coordinate+100,280))
                screen.blit(bobber,(player_x_coordinate+158,285))
                fishing_minigame(player)

        else:
            player_y_coordinate = 395
            screen.blit(player_sprites_scaled[player_sprite_count],(player_x_coordinate,player_y_coordinate)) #displays sprite but scaled up a bit and y changed

        if show_space == True: #if near interactable area
            if in_shop == False:
                screen.blit(space, (player_x_coordinate-70,player_y_coordinate)) #displays space indicator near player
            else:
                screen.blit(space,(player_x_coordinate + 200, player_y_coordinate))  # displays space indicator near player


# Inventory/GUI

        if key[pygame.K_e]: #if the player opens the inventory
            inventory_open = True

        if inventory_open == True:
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

        elif in_shop_menu == True:
            screen.blit(dim_overlay,(0,0)) #displays gui stuff
            screen.blit(shop_menu,(160,90))
            screen.blit(back_sell_button,(25,645))
            screen.blit(back_sell_button,(1160,645))
            screen.blit(back_sell_font.render("Back",False,"red"), (30,656))
            screen.blit(back_sell_font.render("Sell",False,"green"), (1165,656))

            next_rod = shop_next_rod(player) #figures out which rod is the next to be bought with the subroutines outside the while loop

            shop_mouse_pos = pygame.mouse.get_pos() #get mouse pos
            x, y = shop_mouse_pos

            if next_rod != None: #if they can get a new rod
                screen.blit(next_rod.sprite, (200,150)) #show next rod's sprite, name and cost
                screen.blit(shop_upgrade_font.render(next_rod.name, False, "Black"),(270,155))
                screen.blit(shop_upgrade_font.render(f"Cost: {next_rod.cost}",False, "Black"), (700,155))

            screen.blit(Worm_bait.sprite, (185,410)) #displays all bait sprites, names and costs
            screen.blit(shop_bait_font.render(Worm_bait.name, False, "Black"), (240,400))
            screen.blit(shop_bait_font.render(f"Cost: {Worm_bait.cost}",False, "Black"), (240,430))
            screen.blit(Glow_bait.sprite, (670,410))
            screen.blit(shop_bait_font.render(Glow_bait.name, False, "Black"), (725, 400))
            screen.blit(shop_bait_font.render(f"Cost: {Glow_bait.cost}", False, "Black"), (725, 430))
            screen.blit(Chum_bait.sprite, (190,550))
            screen.blit(shop_bait_font.render(Chum_bait.name, False, "Black"), (245,540))
            screen.blit(shop_bait_font.render(f"Cost: {Chum_bait.cost}", False, "Black"), (245,570))
            screen.blit(Rainbow_bait.sprite, (670,550))
            screen.blit(shop_bait_font.render(Rainbow_bait.name, False, "Black"), (725,540))
            screen.blit(shop_bait_font.render(f"Cost: {Rainbow_bait.cost}", False, "Black"), (725,570))
            screen.blit(weight_shop_sprite, (200,275))
            screen.blit(shop_upgrade_font.render("Max weight +10kg", False, "Black"), (270,280))
            screen.blit(shop_upgrade_font.render(f"Cost: {player.weight_upgrade_cost}", False, "Black"), (700,280))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 30<=x<=110 and 650<=y<=690: #if press close button
                    in_shop_menu = False #leave shop GUI
                if 990<=x<=1100 and 130<=y<=190: #if press buy new rod button
                    if can_buy == True:
                        buy_next_rod(player)
                        can_buy = False #stops player buying multiple rods each frame
                if 990<=x<=1110 and 265<=y<=320: #if press buy max weight
                    if can_buy == True:
                        buy_next_weight(player)
                        can_buy = False
                if 515<=x<=625 and 400<=y<=455: #if buy worm bait
                    if can_buy == True:
                        buy_bait(player,Worm_bait)
                        can_buy = False
                if 990<=x<=1100 and 400<=y<=455: #if buy glow bait
                    if can_buy == True:
                        buy_bait(player, Glow_bait)
                        can_buy = False
                if 515<=x<=625 and 535<=y<=590: #if buy chum bait
                    if can_buy == True:
                        buy_bait(player, Chum_bait)
                        can_buy = False
                if 990<=x<=1100 and 535<=y<=590: #if buy rainbow bait
                    if can_buy == True:
                        buy_bait(player, Rainbow_bait)
                        can_buy = False


            if event.type == pygame.MOUSEBUTTONUP: #if player lets go of mouse
                can_buy = True #player can buy something again


        else:
            ingame_clock = hour_display+":"+minute_display

            screen.blit(board,(1080,650)) #bottom right (weight)
            screen.blit(Weight_font.render(f"Weight: {player.weight}kg/{player.max_weight}kg", False, "yellow"), (1087, 677))

            screen.blit(board,(1080,5)) #top right (time)
            screen.blit(Clock_font.render(ingame_clock, False, "yellow"),(1100,25))

            screen.blit(board,(1080,75)) #second top right (weather)
            screen.blit(Weather_font.render(current_weather, False, Weather_font_colour), (1105, 97))

            screen.blit(board,(1080,145)) #third top right (fishdex)
            screen.blit(Fishdex_font.render("Fishdex placeholder", False, "yellow"),(1092,170))

        #these are out of the loop so they are always displayed, even if in shop/inv GUI
        screen.blit(board,(10,5)) #top left (money)
        screen.blit(Money_font.render(f"Money: £{player.money}", False, "yellow"), (20, 32))
        screen.blit(hotbar,(576,650)) #bottom middle (hotbar)
        screen.blit(player.held_rod.sprite, (590,665))
        screen.blit(player.held_bait.sprite, (650, 665))
        screen.blit(inv_bait_amount_font.render(f"{player.bait_amount}", False, "white"), (676,663))

        pygame.display.update()
        Clock.tick(FPS)

# run main menu
main_menu_loop()