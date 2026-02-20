#imports all vital libraries for the game
import sys

import pygame
import random
import os
from sys import exit
pygame.init()
global screen
screen = pygame.display.set_mode((1280, 720)) #sets the game window size
pygame.display.set_caption("Fishing Game") #sets the title for the game in the window
FPS = 60 #sets frames per second
Clock = pygame.time.Clock()

global current_save_slot
current_save_slot = None #sets up save slots for later use


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
    def __init__(self,money,weight,held_rod,held_bait,bait_amount,max_weight,weight_upgrade_cost,fish_start_time,wait_time,reaction_start_time,fish_state,cast,fish_progress,bar_height,fish_height,fish_move_speed,fish_target,caught_fish,inventory,fish_display,inventory_page,unique_fish_caught,fishdex_page): #makes player class with stats

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

        self.caught_fish = caught_fish
        self.inventory = inventory
        self.fish_display = fish_display

        self.inventory_page = inventory_page
        self.fishdex_page = fishdex_page

        self.unique_fish_caught = unique_fish_caught

    def get_fishing_speed(self):
        return self.held_rod.fishing_speed #returns the players fishing speed
    def get_fishing_luck(player):
        return player.held_rod.luck + player.held_bait.luck #returns players total luck stat


class Fish():
    def __init__(self,name,rarity,sell_price,weight,weather,time,sprite):
        self.name = name
        self.rarity = rarity
        self.sell_price = sell_price
        self.weight = weight
        self.weather = weather
        self.time = time
        self.sprite = sprite #original sprite

        self.ui_sprite = None #64x64 sprite for UI display
        self.caught_before = False

#Instantiate objects of class Fish. To help with this, ChatGPT AI was used as it would take a very long time to do myself. Code, file paths and digits have been checked!!! The first 3 were done myself.

Blue_Tang = Fish("Blue tang", "Common", 5, random.uniform(0.4, 0.8), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Bluetang.png").convert_alpha())
Clownfish = Fish("Clownfish", "Common", 5, random.uniform(0.3, 0.6), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Clownfish.png").convert_alpha())
Ornate_Wrasse = Fish("Ornate Wrasse", "Common", 7, random.uniform(0.8, 1), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Ornate_Wrasse.png").convert_alpha())
Yellowback_Fusilier = Fish("Yellowback Fuselier", "Common", 7, random.uniform(1, 1.2), {"Clear", "Rain"},{True, False}, pygame.image.load("Assets/Fish/Yellowback_Fusilier.png").convert_alpha())
Arctic_Cod = Fish("Arctic Cod", "Common", 8, random.uniform(2, 3), {"Snow", "Rain"}, {True, False},pygame.image.load("Assets/Fish/Arctic_Cod.png").convert_alpha())
Haddock = Fish("Haddock", "Common", 8, random.uniform(1.5, 2.5), {"Clear", "Rain"}, {True},pygame.image.load("Assets/Fish/Haddock.png").convert_alpha())
Comber = Fish("Comber", "Common", 7, random.uniform(0.6, 1.0), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Comber.png").convert_alpha())
Herring = Fish("Herring", "Common", 6, random.uniform(0.3, 0.6), {"Clear", "Rain", "Fog"}, {True, False},pygame.image.load("Assets/Fish/Herring.png").convert_alpha())
Whiteleg_Shrimp = Fish("White Shrimp", "Common", 5, random.uniform(0.1, 0.3), {"Fog", "Snow"}, {False},pygame.image.load("Assets/Fish/Whiteleg_Shrimp.png").convert_alpha())

Emperor_Angelfish = Fish("Emperor Angelfish", "Rare", 18, random.uniform(1.5, 2.5), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Emperor_Angelfish.png").convert_alpha())
Lagoon_Triggerfish = Fish("Lagoon Triggerfish", "Rare", 20, random.uniform(2.0, 3.0), {"Clear", "Rain"}, {True},pygame.image.load("Assets/Fish/Lagoon_Triggerfish.png").convert_alpha())
White_Trevally = Fish("White Trevally", "Rare", 22, random.uniform(4.0, 6.0), {"Clear", "Rain"}, {True, False},pygame.image.load("Assets/Fish/White_Trevally.png").convert_alpha())
Coral_Trout = Fish("Coral Trout", "Rare", 25, random.uniform(3.0, 5.0), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Coral_Trout.png").convert_alpha())
Pacific_Fanfish = Fish("Pacific Fanfish", "Rare", 24, random.uniform(1.2, 2.0), {"Fog", "Rain"}, {True},pygame.image.load("Assets/Fish/Pacific_Fanfish.png").convert_alpha())
Titan_Triggerfish = Fish("Titan Triggerfish", "Rare", 28, random.uniform(4.0, 6.5), {"Rain", "Snow"}, {True, False},pygame.image.load("Assets/Fish/Titan_Triggerfish.png").convert_alpha())
Cardinal = Fish("Cardinal Fish", "Rare", 16, random.uniform(0.4, 0.8), {"Fog", "Snow"}, {False},pygame.image.load("Assets/Fish/Cardinal.png").convert_alpha())

Yellowfin_Tuna = Fish("Yellowfin Tuna", "Epic", 60, random.uniform(30, 50), {"Clear", "Rain"}, {True, False},pygame.image.load("Assets/Fish/Yellowfin_Tuna.png").convert_alpha())
Albacore = Fish("Albacore", "Epic", 55, random.uniform(20, 35), {"Clear", "Rain"}, {True},pygame.image.load("Assets/Fish/Albacore.png").convert_alpha())
Humboldt_Squid = Fish("Humboldt Squid", "Epic", 65, random.uniform(15, 30), {"Fog", "Rain"}, {False},pygame.image.load("Assets/Fish/Humbolt_Squid.png").convert_alpha())
Harlequin_Hind = Fish("Harlequin Hind", "Epic", 70, random.uniform(20, 40), {"Clear", "Fog"}, {True},pygame.image.load("Assets/Fish/Harlequin_Hind.png").convert_alpha())
Red_Lionfish = Fish("Red Lionfish", "Epic", 75, random.uniform(1.0, 1.8), {"Fog", "Snow"}, {False},pygame.image.load("Assets/Fish/Red_Lionfish.png").convert_alpha())

Marlin = Fish("Marlin", "Legendary", 300, random.uniform(200, 400), {"Clear", "Rain"}, {True},pygame.image.load("Assets/Fish/Marlin.png").convert_alpha())
Shortfin_Mako = Fish("Shortfin Mako", "Legendary", 500, random.uniform(300, 500), {"Clear", "Rain"}, {True, False},pygame.image.load("Assets/Fish/Shortfin_Mako.png").convert_alpha())
Thresher_Shark = Fish("Thresher Shark", "Legendary", 500, random.uniform(350, 600), {"Rain", "Fog"}, {False},pygame.image.load("Assets/Fish/Thresher_Shark.png").convert_alpha())
Vampire_Squid = Fish("Vampire Squid", "Legendary", 250, random.uniform(8, 15), {"Fog", "Snow"}, {False},pygame.image.load("Assets/Fish/Vampire_Squid.png").convert_alpha())

#create list with all fish
All_Fish = [Blue_Tang,Clownfish,Ornate_Wrasse,Yellowback_Fusilier,Arctic_Cod,Haddock,Comber,Herring,Whiteleg_Shrimp,Emperor_Angelfish,Lagoon_Triggerfish,White_Trevally,Coral_Trout,Pacific_Fanfish, Titan_Triggerfish, Cardinal,Yellowfin_Tuna,Albacore,Humboldt_Squid,Harlequin_Hind,Red_Lionfish,Marlin,Shortfin_Mako,Thresher_Shark,Vampire_Squid]
fishdex_list = All_Fish

#TIPS:
#USE FORWARD SLASHES FOR FILE PATHS
#REMEMBER FOR LOCATIONS IT GOES DEST:(X,Y)
#WHEN LOADING GAME SPRITES, USE THE .convert_alpha() AT THE END TO CONVERT TO A FILE TYPE PYGAME LIKES MORE
#spritename = pygame.transform.scale(spritename, (x,y)) will scale the sprite size

# Main menu and fadeout

def main_menu_loop():
    Main_menu_running = True
    BG = pygame.image.load("Assets/Menus/Main_menu_background.png").convert_alpha() #loads background image once
    fontsize20 = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    pygame.mixer.music.load("Assets/Menus/Main_menu_background_music.mp3") #sets main menu background music file as a variable
    pygame.mixer.music.set_volume(0.05) #sets MMBMF volume to 50%
    pygame.mixer.music.play(-1) #plays the MMBMF infinitely

    while Main_menu_running: #all main menu logic here
        main_menu_font_colourLG = "Yellow"
        main_menu_font_colourNG = "Yellow"
        main_menu_font_colourS = "Yellow"
        main_menu_font_colourEG = "Yellow"

        x, y = pygame.mouse.get_pos()
        if 530 <= x <= 750 and 279 <= y <= 325:
            main_menu_font_colourLG = "Green"
        if 530 <= x <= 750 and 388 <= y <= 435:
            main_menu_font_colourNG = "Green"
        if 530 <= x <= 750 and 493 <= y <= 541:
            main_menu_font_colourS = "Green"
        if 530 <= x <= 750 and 600 <= y <= 647:
            main_menu_font_colourEG = "Green"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 530 <= x <= 750 and 279 <= y <= 325:
                    save_menu_loop()
                if 530 <= x <= 750 and 388 <= y <= 435:
                    empty_slot = find_empty_save() #checks to see if any files are available
                    if empty_slot != None: #if there is one available
                        global current_save_slot
                        current_save_slot = empty_slot #assigns number
                        Main_menu_running = False #stops main menu
                        pygame.mixer.music.fadeout(6500) #fades music out over 6.5 seconds
                        fadeout() #goes to the fadeout subroutine for a smooth transition
                        player = Player(0, 0, Starter_rod, No_bait, 0, 50, 100, 0, 0, 0, "idle", False, 40, 310, 345, 0,random.randint(45, 590), None, [], 0, 0, 0, 0)  # instantiate object of class player
                        hour_hand = 6
                        minute_hand = 0
                        current_weather = "Clear"
                        main_game(player,hour_hand,minute_hand,current_weather) #loads game background
                    else:
                        print("ALL SLOTS FULL")
                        pass
                if 530 <= x <= 750 and 493 <= y <= 541: #settings button logic
                    pass
                if 530 <= x <= 750 and 600 <= y <= 647: #quit button logic
                    pygame.quit()
                    exit()  # quit game

        # draws background
        screen.blit(BG, (0, 0))

        # draws menu text
        screen.blit(fontsize20.render("Load Game", False, main_menu_font_colourLG), (555, 294))
        screen.blit(fontsize20.render("New Game", False, main_menu_font_colourNG), (565, 403))
        screen.blit(fontsize20.render("Settings", False, main_menu_font_colourS), (563, 509))
        screen.blit(fontsize20.render("Exit Game", False, main_menu_font_colourEG), (555, 616))

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
def main_game(player,hour_hand,minute_hand,current_weather): #all game stuff goes in here
    game_running = True #sets main game loop

    fontsize6 = pygame.font.Font("PressStart2P-Regular.ttf", 6)
    fontsize10 = pygame.font.Font("PressStart2P-Regular.ttf", 10)
    fontsize15 = pygame.font.Font("PressStart2P-Regular.ttf", 15)
    fontsize17 = pygame.font.Font("PressStart2P-Regular.ttf", 17)
    fontsize18 = pygame.font.Font("PressStart2P-Regular.ttf", 18)
    fontsize20 = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    fontsize21 = pygame.font.Font("PressStart2P-Regular.ttf", 21)
    fontsize25 = pygame.font.Font("PressStart2P-Regular.ttf", 25)
    fontsize30 = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    fontsize50 = pygame.font.Font("PressStart2P-Regular.ttf", 50)

# Main game loading - sprites and variable set up

    Foreground = pygame.image.load("Assets/Background stuff/foreground.png").convert_alpha()  # loads fg

    weather_list = ["Clear","Rain","Snow","Fog"] #sets the weathers
    weather_duration = random.randint(180000,420000) #creates the weather duration variable used in the while loop between 3 and 7 minutes
    last_weather_tick = pygame.time.get_ticks()

    day = True #sets time to day
    prev_day = day
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
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - The Blue Hole.mp3"), #1 Day Rain
                        pygame.mixer.Sound("Assets/Background stuff/C418 - Sweden - Minecraft Volume Alpha.mp3"), #2 Day Fog
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Diver.mp3"), #3 Day Snow
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Night Diving.mp3"), #4 Night Clear
                        pygame.mixer.Sound("Assets/Background stuff/Eterna Forest.mp3"), #5 Night Rain
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Darker Trenches.mp3"), #6 Night Fog
                        pygame.mixer.Sound("Assets/Background stuff/Dave the Diver OST - Ice Level (Preserved Realm).mp3"), #7 Night Snow
                        pygame.mixer.Sound("Assets/Shop/shop music.mp3")] #8 shop music

    for music in background_musics:
        music.set_volume(0.05) #sets each bg musics volume to 50%

    current_background_music = None #creates variable to store current music playing
    current_background_music_index = -1 #creates variable to store current music playing's position for the bg music's index
    new_background_music_index = 0 #creates variable to store the next music's index in the bg music list

    #creating fonts for the inv and loading images
    board = pygame.image.load("Assets/Menus/board.png").convert_alpha()
    hotbar = pygame.image.load("Assets/Menus/hotbar.png").convert_alpha()
    Weather_font_colour = "aqua"

    minutes = [00, 10, 20, 30, 40, 50] #list of possible minutes the clock can display
    clock_tick_length = 8333  # 8.33s per ingame 10 minutes, means each full day is 20m long (8333mm is 8.33s)
    minute_display = "00" #sets default minute display to 00
    hour_display = "6" #sets default hour display to 6AM

    inventory_open = False #creates variable used later for checking if the inv is open
    inventory = pygame.image.load("Assets/Menus/inventory.png").convert_alpha() #loads inventory bg

    shop_bg = pygame.image.load("Assets/Shop/background_shop.png").convert_alpha()
    npc_left = pygame.image.load("Assets/Shop/Corkah_left.png").convert_alpha()
    space = pygame.image.load("Assets/Shop/space.png").convert_alpha()
    shop_menu = pygame.image.load("Assets/Shop/shop interface.png").convert_alpha()
    back_sell_button = pygame.image.load("Assets/Shop/back_button.png").convert_alpha()
    in_shop = False #instantiate variable for checking if in shop
    in_shop_menu = False #instantiate variable for checking if in shop menu
    dim_overlay = pygame.Surface((1280,720))  # creates a new screen the size of the window
    dim_overlay.set_alpha(140)  # sets transparency of the new screen
    dim_overlay.fill((0,0,0))  # sets the new screen to black
    weight_shop_sprite = pygame.image.load("Assets/Shop/weight_upgrade.png").convert_alpha()
    can_buy = True #instantiates can buy variable for later in the shop, so you cant buy multiple rods every next frame

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
            player.weight_upgrade_cost+=50 #buff price by 100
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

    def retrieve_fish(player,current_weather,day):
        roll = random.randint(1, 300) #chooses random num
        roll += player.get_fishing_luck() #combines it with player luck stat

        if roll > 300: #if too high
            roll = 300 #set to max

        #choose what rarity to return based off role
        if roll <= 180:
            rarity_index = 0 #common (around 60%)
        elif roll <= 270:
            rarity_index = 1 #rare (around 30%)
        elif roll <= 297:
            rarity_index = 2 #epic (around 9%)
        else:
            rarity_index = 3 #legendary (around 1%)

        rarity = ["Common", "Rare", "Epic", "Legendary"]

        while rarity_index>=0: #while fish has not been chosen yet
            possible_fish = [] #empty list of fish that are possible to catch at current game mechanics (rarity, time, weather)
            for fish in All_Fish: #for every fish in the game
                if fish.rarity == rarity[rarity_index]: #if rarity is the same
                    if current_weather in fish.weather: #if weather req is the same
                        if day in fish.time: #if time req is the same
                            possible_fish.append(fish) #add fish to possible fish to be caught

            if len(possible_fish) > 0: #if a fish is found
                caught_fish = random.choice(possible_fish) #choose one of the elegible fish at random
                return caught_fish

            else:
                rarity_index -= 1 #drop to lower rarity

    def fishing_minigame(player): #begins minigame
        current_time = pygame.time.get_ticks() #gets current tick time
        bottom_y = 680  # this value does not change!! it is the bottom of the bar

        if player.fish_state == "waiting": #if waiting for a fish to bite
            if current_time - player.fish_start_time >= player.wait_time: #checks and compares wait time with time waited
                player.fish_state = "react" #reaction game starts
                player.reaction_start_time = current_time #gets time the reaction game started at
                splash.play(0)  #play sound effect
                if player.bait_amount > 0:
                    player.bait_amount -= 1  # 1 bait is used up
                    if player.bait_amount == 0:
                        player.held_bait = No_bait

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
            if player.bar_height>=590: #if too low
                player.bar_height-=3 #increase bar height by 3
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
                player.fish_state = "won"


            elif player.fish_progress <= 0: #if all progress lost
                player.cast = False
                player.fish_state = "idle"

            # blitting images
            screen.blit(dim_overlay, (0, 0))
            screen.blit(fishing_minigame_bg, (570, 45))
            screen.blit(fishing_minigame_bar, bar_rect)  # displays moveable rect at rectangle coords
            screen.blit(fishing_minigame_fish, fish_rect)  # displays fish at rectangle coords
            pygame.draw.rect(screen, (0, 255, 0), (910, bottom_y - player.fish_progress, 20,player.fish_progress))  # PROGRESS DISPLAY - colour, coordinates, width+height
            screen.blit(fontsize10.render("Hold the W key to move the bar up", False, "yellow"), (945, 375))
            screen.blit(fontsize10.render("Let go to move the bar down", False, "yellow"), (945, 400))


        elif player.fish_state == "won":
            caught_fish=retrieve_fish(player,current_weather,day) #gets the caught fish from the subroutine retrieve fish
            player.caught_fish = caught_fish #sets the caught fish into player class
            player.weight += caught_fish.weight #adds the fish's weight to the player's weight
            player.inventory.append(caught_fish) #adds caught fish to inventory array
            player.fish_state = "show_fish" #turns on variable to show what the player caught
            player.show_fish = pygame.time.get_ticks() #gets the time the fish was caught

            if caught_fish.caught_before == False: #if the fish hasn't been caught before
                caught_fish.caught_before = True #it has now been caught
                player.unique_fish_caught+=1 #updates counter

            player.cast = False
            print(f"New fish caught: {player.caught_fish.name}, New fish caught weight: {player.caught_fish.weight:.2f}, New fish caught rarity: {player.caught_fish.rarity}") #debug, shows what i caught and its stats

    FISH_BOX_SIZE = 64 #sprites will show as 64x64 in the fishdex
    for fish in All_Fish:
        sprite = fish.sprite #og fish sprite
        original_width = sprite.get_width()
        original_height = sprite.get_height()
        scale_factor = min(FISH_BOX_SIZE/original_width, FISH_BOX_SIZE/original_height) #calc scale factor so sprite fits in box
        new_width = int(original_width*scale_factor) #creates new width
        new_height = int(original_height*scale_factor) #creates new height
        fish.ui_sprite = pygame.transform.scale(sprite,(new_width,new_height)) #scales fish up to 64x64

    fishdex_menu = pygame.image.load("Assets/Menus/fishdex.png").convert_alpha()
    fishdex_open = False

    paused = False
    dim_overlay_pause = pygame.Surface((1280, 720))  # creates a new screen the size of the window
    dim_overlay_pause.set_alpha(200)  # sets transparency of the new screen 200
    dim_overlay_pause.fill((0, 0, 0))

    text_board = pygame.image.load("Assets/Menus/text_board.png")

    def save_game(player, All_Fish, current_weather, hour_hand, minute_hand, current_save_slot):
        caught_fish = []
        for fish in All_Fish:
            if fish.caught_before == True:
                caught_fish.append(fish.name)
        held_fish = []
        for fish in player.inventory:
            held_fish.append(fish.name)

        SaveFile = f"SaveFile{current_save_slot}.txt"
        TextFile = open(SaveFile,"w") #opens file
        TextFile.write(f"{player.money}\n")
        TextFile.write(f"{player.held_rod.name}\n")
        TextFile.write(f"{player.held_bait.name}\n")
        TextFile.write(f"{player.bait_amount}\n")
        TextFile.write(f"{player.weight}\n")
        TextFile.write(f"{player.max_weight}\n")
        TextFile.write(f"{player.weight_upgrade_cost}\n")
        TextFile.write(f"{player.unique_fish_caught}\n")
        TextFile.write(f"{held_fish}\n")
        TextFile.write(f"{caught_fish}\n")
        TextFile.write(f"{hour_hand}\n")
        TextFile.write(f"{minute_hand}\n")
        TextFile.write(f"{current_weather}\n")
        TextFile.close()


# MAIN GAME LOOP
    while game_running:

        for event in pygame.event.get():  # handles quitting and debug code
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at", menu_mouse_pos_test)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if player.fish_state == "idle":
                        paused = not paused
                        if paused:
                            screen.blit(dim_overlay_pause, (0, 0)) #dim as pause mode is entered
                        current_background_music.set_volume(0.0 if paused else 0.05)
                    else:
                        pass

                if event.key == pygame.K_e: #if its e
                    inventory_open = not inventory_open #flips state of inventory_open
                    if inventory_open == True: #if it is true
                        player.inventory_page = 0 #page inv on is the first one

                if event.key == pygame.K_f:
                    fishdex_open = not fishdex_open
                    if fishdex_open == True:
                        player.fishdex_page = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if paused:
                    if 530 <= x <= 750 and 269 <= y <= 320:  # if mouse near button
                        paused = False
                        current_background_music.set_volume(0.05)
                    elif 530 <= x <= 750 and 369 <= y <= 420: #settings button
                        pass
                    elif 530 <= x <= 750 and 470 <= y <= 520: #save button
                        save_game(player, All_Fish, current_weather, hour_hand, minute_hand,current_save_slot)
                    elif 530 <= x <= 750 and 570 <= y <= 620:
                        save_game(player, All_Fish, current_weather, hour_hand, minute_hand,current_save_slot)
                        main_menu_loop()
                        game_running = False

                elif inventory_open or fishdex_open:
                    if 1075 <= x <= 1110 and 100 <= y <= 130:  # if near the X button
                        inventory_open = False  # inv is closed
                        fishdex_open = False
                    if 1075 <= x <= 1110 and 135 <= y <= 170:  # if click on up arrow
                        if player.inventory_page > 0:  # prevent going on a page smaller than 0
                            player.inventory_page -= 1  # go up a page
                        if player.fishdex_page > 0:
                            player.fishdex_page -= 1

                    if 1075 <= x <= 1110 and 585 <= y <= 620:  # if click on down arrow
                        if inventory_open == True:
                            if (player.inventory_page + 1) * 9 < len(inventory_summary_list):  # if there are fish on the next page
                                player.inventory_page += 1  # go to next page
                        if fishdex_open == True:
                            if (player.fishdex_page + 1) < 7:  # if they are trying to click on empty page
                                player.fishdex_page += 1

        if not paused:

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
                if day != prev_day: #if the time of day has swapped, update bg
                    if current_weather == "Clear":
                        if day == True:
                            weather_bg = Sunny_Sky_Day
                        else:
                            weather_bg = Clear_Sky_Night
                    if current_weather == "Rain":
                        if day == True:
                            weather_bg = Rainy_Sky_Day
                        else:
                            weather_bg = Rainy_Sky_Night
                    if current_weather == "Fog":
                        if day == True:
                            weather_bg = FogSnow_Sky_Day
                        else:
                            weather_bg = FogSnow_Sky_Night
                    if current_weather == "Snow":
                        if day == True:
                            weather_bg = FogSnow_Sky_Day
                        else:
                            weather_bg = FogSnow_Sky_Night


            if current_time - last_weather_tick >= weather_duration: #if the time passed is equal to the random weather duration
                last_weather_tick = current_time #resets timer
                weather_duration = random.randint(180000,420000)  # creates the new weather duration variable between 3 (180000)and 7 (420000) minutes
                new_weather = random.choice(weather_list) #chooses new weather
                while new_weather == current_weather: #if it is the same
                    new_weather=random.choice(weather_list) #choose again
                current_weather = new_weather #set current weather

                fog = False
                rain = False
                snow = False

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

                elif current_weather == "Rain":
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

                elif current_weather == "Snow":
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
                if current_weather == "Clear" or current_weather == "Rain":
                    screen.blit(cloud1,(cloud_1_x,cloud_1_y))  # displays cloud
                    cloud_1_x += 1  # moves cloud 1 pixel left
                    if cloud_1_x >= 1280:  # checks to see if cloud to far right off-screen
                        cloud_1_x = 0  # moves cloud back to the start
                if current_weather == "Clear" or current_weather == "Rain":
                    screen.blit(cloud2,(cloud_2_x,cloud_2_y))
                    cloud_2_x += 0.4
                    if cloud_2_x >= 1280:
                        cloud_2_x = 0
                if current_weather == "Clear" or current_weather == "Rain":
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
                        current_background_music.fadeout(3000) #fade out current bg music for 3s

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
                            else:
                                screen.blit(fontsize20.render("Max weight reached!",False,"Red"),(player_x_coordinate+200,300))

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

            if inventory_open == True:
                screen.blit(dim_overlay, (0, 0)) #puts the faded new screen to make the background darker to bring more contrast to inv

                #displays inv and text
                screen.blit(inventory,(160,90))
                screen.blit(fontsize20.render(f"Money: £{player.money}", False, "yellow"), (175,107))
                screen.blit(fontsize20.render(f"Weight: {player.weight:.0f}kg", False, "yellow"), (480,107))
                screen.blit(fontsize20.render("Fishdex:", False, "yellow"), (780,107))
                screen.blit(fontsize20.render("Fish:", False, "yellow"), (175,145))
                screen.blit(fontsize20.render("Quantity:", False, "yellow"), (480,145))
                screen.blit(fontsize20.render("Sell Price:", False, "yellow"), (780, 145))

                inventory_summary = {} #creates emtpy dictionary
                for fish in player.inventory: #for each fish inside the players inv
                    if fish.name not in inventory_summary: #if fish's name isnt in it
                        inventory_summary[fish.name] = {"fish":fish, "quantity":1} #add it with a quantity of 1
                    else:
                        inventory_summary[fish.name]["quantity"]+=1 #otherwise add another to the quantity

                inventory_summary_list = list(inventory_summary.values()) #.values() returns just values of the item, list() converts the dictionary into a normal list
                #calculates what fish to show
                start = player.inventory_page*9 #calculate starting index
                end = start+9 #calculate ending index
                visible_fish = inventory_summary_list[start:end] #take only fish entries from current page
                text_y_pos = 185
                for entry in visible_fish: #for each fish in the fish that will be displayed
                    fish = entry["fish"] #get fish object from entry dictionary
                    quantity = entry["quantity"] #how many fish of this name does the player own?
                    total_price = fish.sell_price*quantity #how much does it all sell for?
                    screen.blit(fontsize20.render(f"{fish.name}   x{quantity}", False, "yellow"), (175,text_y_pos)) #show stats
                    screen.blit(fontsize20.render(f"{total_price}", False, "yellow"), (775,text_y_pos))
                    text_y_pos+=50 #for the next fish, blit info 50 pixels down

            elif fishdex_open == True:
                screen.blit(dim_overlay, (0,0)) #dims screen
                screen.blit(fishdex_menu,(160,90)) #displays fishdex menu
                screen.blit(fontsize20.render(f"Fishdex progression: {player.unique_fish_caught}/25", False, "yellow"), (175,107)) #shows progression as text

                fish_per_page = 4 #sets amount of fish per page to 4
                start = player.fishdex_page*fish_per_page #first fish index for this page
                end = start+fish_per_page #last fish index for this page
                visible_fish = fishdex_list[start:end] #the 4 fish to display on this page

                box_locations = [(210,165),(650,165),(210,395),(650,395)] #positions of the fish boxes
                for i in range(len(visible_fish)): #loop through the 4 fish to display on this page
                    fish=visible_fish[i] #get current fish
                    box_x, box_y = box_locations[i] #get box position
                    pygame.draw.rect(screen, "black", (box_x, box_y, 384,200),6) #draw box fish border (black, coordinates, width/height, thickness)

                    if fish.caught_before: #if the fish has been caught
                        sprite_rect = fish.ui_sprite.get_rect(center=(box_x+185, box_y+50)) #display its sprite
                        weather_text = ", ".join(fish.weather) #sets weather to a string instead of list to print

                        if fish.time == {True}: #sets time text to show day/night intead of True/False
                            time_text = "Day"
                        elif fish.time == {False}:
                            time_text = "Night"
                        else:
                            time_text = "Day and Night"

                        if fish.rarity == "Common": #sets rarity text to colour associated with rarity
                            colour = "grey"
                        elif fish.rarity == "Rare":
                            colour = "blue"
                        elif fish.rarity == "Epic":
                            colour = "purple"
                        elif fish.rarity == "Legendary":
                            colour = "orange"

                        #shows fish details
                        screen.blit(fish.ui_sprite,sprite_rect)
                        screen.blit(fontsize15.render(fish.name, False, "yellow"), (box_x+10,box_y+100))
                        screen.blit(fontsize15.render(f"Rarity: {fish.rarity}", False, colour), (box_x + 10, box_y + 125))
                        screen.blit(fontsize15.render(f"Weather req: {weather_text}", False, "yellow"), (box_x+10,box_y+150))
                        screen.blit(fontsize15.render(f"Time req: {time_text}", False, "yellow"), (box_x+10, box_y+175))

                    #shows hidden fish details if they have not caught it
                    else:
                        screen.blit(fontsize18.render("?", False, "grey"), (box_x+185,box_y+50))
                        screen.blit(fontsize15.render("Not caught", False, "red"), (box_x+10,box_y+100))
                        screen.blit(fontsize15.render("Rarity: ???", False, "white"), (box_x+10,box_y+125))
                        screen.blit(fontsize15.render("Weather req: ???", False, "white"), (box_x + 10,box_y + 150))
                        screen.blit(fontsize15.render("Time req: ???", False, "white"), (box_x + 10,box_y + 175))


            elif in_shop_menu == True:
                screen.blit(dim_overlay,(0,0)) #displays gui stuff
                screen.blit(shop_menu,(160,90))
                screen.blit(back_sell_button,(25,645))
                screen.blit(back_sell_button,(1160,645))
                screen.blit(fontsize20.render("Back",False,"red"), (30,656))
                screen.blit(fontsize20.render("Sell",False,"green"), (1165,656))

                next_rod = shop_next_rod(player) #figures out which rod is the next to be bought with the subroutines outside the while loop

                shop_mouse_pos = pygame.mouse.get_pos() #get mouse pos
                x, y = shop_mouse_pos

                if next_rod != None: #if they can get a new rod
                    screen.blit(next_rod.sprite, (200,150)) #show next rod's sprite, name and cost
                    screen.blit(fontsize25.render(next_rod.name, False, "Black"),(270,155))
                    screen.blit(fontsize25.render(f"Cost: {next_rod.cost}",False, "Black"), (700,155))

                screen.blit(Worm_bait.sprite, (185,410)) #displays all bait sprites, names and costs
                screen.blit(fontsize20.render(Worm_bait.name, False, "Black"), (240,400))
                screen.blit(fontsize20.render(f"Cost: {Worm_bait.cost}",False, "Black"), (240,430))
                screen.blit(Glow_bait.sprite, (670,410))
                screen.blit(fontsize20.render(Glow_bait.name, False, "Black"), (725, 400))
                screen.blit(fontsize20.render(f"Cost: {Glow_bait.cost}", False, "Black"), (725, 430))
                screen.blit(Chum_bait.sprite, (190,550))
                screen.blit(fontsize20.render(Chum_bait.name, False, "Black"), (245,540))
                screen.blit(fontsize20.render(f"Cost: {Chum_bait.cost}", False, "Black"), (245,570))
                screen.blit(Rainbow_bait.sprite, (670,550))
                screen.blit(fontsize20.render(Rainbow_bait.name, False, "Black"), (725,540))
                screen.blit(fontsize20.render(f"Cost: {Rainbow_bait.cost}", False, "Black"), (725,570))
                screen.blit(weight_shop_sprite, (200,275))
                screen.blit(fontsize25.render("Max weight +10kg", False, "Black"), (270,280))
                screen.blit(fontsize25.render(f"Cost: {player.weight_upgrade_cost}", False, "Black"), (700,280))

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
                    if 1160<=x<=1250 and 645<=y<=690:
                        for fish in player.inventory:
                            player.money+=fish.sell_price
                            player.weight = 0
                        player.inventory.clear()

                if event.type == pygame.MOUSEBUTTONUP: #if player lets go of mouse
                    can_buy = True #player can buy something again


            else:
                ingame_clock = str(hour_display).zfill(2)+":"+str(minute_display).zfill(2) #zfill if string is 1 character long it puts a 0 at the start of the string until is as long as parameter put in (2)

                screen.blit(board,(1080,650)) #bottom right (weight)
                screen.blit(fontsize17.render("Weight:", False, "yellow"), (1087, 657))
                screen.blit(fontsize17.render(f"{player.weight:.0f}kg/{player.max_weight}kg", False, "yellow"), (1087, 687))

                screen.blit(board,(1080,5)) #top right (time)
                screen.blit(fontsize30.render(ingame_clock, False, "yellow"),(1100,25))

                screen.blit(board,(1080,75)) #second top right (weather)
                screen.blit(fontsize20.render(current_weather, False, Weather_font_colour), (1105, 97))

                screen.blit(board,(1080,145)) #third top right (fishdex)
                screen.blit(fontsize21.render(f"{player.unique_fish_caught}/25", False, "yellow"),(1088,167))
                screen.blit(fontsize15.render("Fish", False, "yellow"), (1179, 160))
                screen.blit(fontsize15.render("Caught", False, "yellow"), (1179,178))

            #these are out of the loop so they are always displayed, even if in shop/inv GUI
            screen.blit(board,(10,5)) #top left (money)
            screen.blit(fontsize17.render(f"{player.money} gold", False, "yellow"), (20, 30))
            screen.blit(hotbar,(576,650)) #bottom middle (hotbar)
            screen.blit(player.held_rod.sprite, (590,665))
            screen.blit(player.held_bait.sprite, (650, 665))
            screen.blit(fontsize10.render(f"{player.bait_amount}", False, "white"), (676,663))

            if player.fish_state == "show_fish": #if player has caught a fish
                current_time = pygame.time.get_ticks() #get time
                if current_time - player.show_fish <2000: #for the next 2 seconds, show the fish sprite and name of the fish they caught
                    screen.blit(board,(10,656))

                    box_x, box_y = 15,656 #top left of 64x64 area
                    fish_sprite = player.caught_fish.ui_sprite #gets prescaled UI version of fish sprite
                    fish_rect = fish_sprite.get_rect(center=(box_x+32, box_y+32)) #create a rect for the sprite and center it inside the 64x64 box
                    screen.blit(fish_sprite,fish_rect) #draw at calculated position

                    screen.blit(fontsize6.render(f"{player.caught_fish.name}",False,"yellow"), (80,680))
                else:
                    player.fish_state = "idle"

        if paused:
            resumecolour = "Yellow"
            settingscolour = "Yellow"
            savegamecolour = "Yellow"
            quitgamecolour = "Yellow"

            menu_mouse_pos = pygame.mouse.get_pos()
            x, y = menu_mouse_pos

            if 530 <= x <= 750 and 269 <= y <= 320:  # if mouse near button
                resumecolour = "Green"  # change text colour

            if 530 <= x <= 750 and 369 <= y <= 420:
                settingscolour = "Green"

            if 530 <= x <= 750 and 470 <= y <= 520:
                savegamecolour = "Green"

            if 530 <= x <= 750 and 570 <= y <= 620:
                quitgamecolour = "Green"

            screen.blit(text_board, (516, 220))
            screen.blit(text_board, (516, 320))
            screen.blit(text_board, (516, 420))
            screen.blit(text_board, (516, 520))
            screen.blit(fontsize50.render("PAUSED", False, "red"), (500, 130))
            screen.blit(fontsize20.render("Resume game", False, resumecolour), (535, 286))
            screen.blit(fontsize20.render("Settings", False, settingscolour), (563, 386))
            screen.blit(fontsize20.render("Save game", False, savegamecolour), (554, 486))
            screen.blit(fontsize20.render("Quit game", False, quitgamecolour), (554, 586))


        pygame.display.update()
        Clock.tick(FPS)

def save_menu_loop():
    save_menu_running = True
    BGS = pygame.image.load("Assets/Menus/Save_menu_background.png").convert_alpha()
    fontsize20 = pygame.font.Font("PressStart2P-Regular.ttf", 20)

    while save_menu_running == True:
        global current_save_slot
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # handles X for quit in window
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_pos_test = pygame.mouse.get_pos()
                print("Mouse clicked at", menu_mouse_pos_test)  # debugging tool, shows me where I clicked in terminal

            S1 = "Yellow"
            S2 = "Yellow"
            S3 = "Yellow"
            back = "Yellow"

            menu_mouse_pos = pygame.mouse.get_pos()
            x, y = menu_mouse_pos

            if 530<=x<=750 and 279<=y<=325: #checks to see if mouse coords are nearby text
                S1 = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_save_slot = 1
                    player, hour_hand, minute_hand, current_weather = load_game(All_Fish, current_save_slot)
                    pygame.mixer.music.fadeout(6500) #fades music out over 6.5 seconds
                    fadeout() #goes to the fadeout subroutine for a smooth transition
                    main_game(player,hour_hand,minute_hand,current_weather)
            if 530<=x<=750 and 388<=y<=435:
                S2 = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_save_slot = 2
                    player, hour_hand, minute_hand, current_weather = load_game(All_Fish,current_save_slot)
                    pygame.mixer.music.fadeout(6500) #fades music out over 6.5 seconds
                    fadeout() #goes to the fadeout subroutine for a smooth transition
                    main_game(player,hour_hand,minute_hand,current_weather)

            if 530<=x<=750 and 493<=y<=541:
                S3 = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_save_slot = 3
                    player, hour_hand, minute_hand, current_weather = load_game(All_Fish,current_save_slot)
                    pygame.mixer.music.fadeout(6500) #fades music out over 6.5 seconds
                    fadeout() #goes to the fadeout subroutine for a smooth transition
                    main_game(player,hour_hand,minute_hand,current_weather)

            if 530<=x<=750 and 600<=y<=647:
                back = "Green"
                if event.type == pygame.MOUSEBUTTONDOWN: #if user clicks back button...
                    save_menu_running = False

            # draws background
            screen.blit(BGS, (0, 0))

            # draws menu text
            screen.blit(fontsize20.render("Save 1", False, S1), (555, 294))
            screen.blit(fontsize20.render("Save 2", False, S2), (565, 403))
            screen.blit(fontsize20.render("Save 3", False, S3), (563, 509))
            screen.blit(fontsize20.render("Back", False, back), (555, 616))

            # updates display
            pygame.display.update()
            Clock.tick(FPS)

def find_empty_save():
    for file in range(1,4): #for save file 1,2 and 3
        filename = f"SaveFile{file}.txt"
        if not os.path.exists(filename): #checks if the file exists
            return file #returns first emtpy slot
    return None #no empty slots left

def load_game(All_Fish, current_save_slot):
    #if this is a new game (either selected by new game button or clicking a save file in saves menu without data) load base player stats (empty inv/fishdex/bait/rod, no money, base weight/weight cost), clear weather, 6AM time
    #if it is an old save (selected through saves menu) the previous player stats, weather and time are loaded
    filename = f"SaveFile{current_save_slot}.txt"
    if not os.path.exists(filename): #if a file doesn't exist in that slot, load default gear/time/money/stats/fishdex/inventory...
        player = Player(0, 0, Starter_rod, No_bait, 0, 50, 100, 0, 0, 0, "idle", False, 40, 310, 345, 0,random.randint(45, 590), None, [], 0, 0, 0, 0)  # instantiate object of class player
        hour_hand = 6
        minute_hand = 0
        current_weather = "Clear"
        return player, hour_hand, minute_hand, current_weather
    else: #loading an existing save file...
        filename = open(filename, "r") #opens file
        money = int(filename.readline()) #taking stats
        held_rod = filename.readline().strip()
        held_bait = filename.readline().strip()
        bait_amount = int(filename.readline())
        weight = float(filename.readline())
        max_weight = int(filename.readline())
        weight_upgrade_cost = int(filename.readline())
        unique_fish_caught = int(filename.readline())
        held_fish = eval(filename.readline())
        caught_fish = eval(filename.readline())
        hour_hand = int(filename.readline())
        minute_hand = int(filename.readline())
        current_weather = filename.readline().strip()
        filename.close()

        #converting rods and baits back into the object from the string loaded from the file
        for rod in [Starter_rod, Hobbyist_rod, Commercial_rod, Sturdy_rod, Rod_of_the_sea, Rod_of_the_ocean, Amethyst_rod, Australium_rod, Lightsaber_rod, Hellfire_rod, God_rod]:
            if rod.name == held_rod:
                held_rod = rod
        for bait in [No_bait, Worm_bait, Glow_bait, Chum_bait, Rainbow_bait]:
            if bait.name == held_bait:
                held_bait = bait

        player = Player(money,weight,held_rod,held_bait,bait_amount,max_weight,weight_upgrade_cost,0,0,0,"idle",False,40,310,345,0,random.randint(45,590),None,[],0,0,unique_fish_caught,0)
        player.inventory = []
        for fish in All_Fish:
            if fish.name in held_fish:
                player.inventory.append(fish)
            if fish.name in caught_fish:
                fish.caught_before = True
            else:
                fish.caught_before = False

        return player, hour_hand, minute_hand, current_weather
# run main menu
main_menu_loop()