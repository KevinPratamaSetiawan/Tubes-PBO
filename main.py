#Library
import pygame
import os
import random
from abc import ABC, abstractmethod

#Other File
import Button
import Skill
import Character
import Save_File

#Window
pygame.init()
screen      = pygame.display.set_mode((1280,720))
window_icon = pygame.image.load("Assets/Other/DinoIcont.png")
pygame.display.set_icon(window_icon)
pygame.display.set_caption("just RUN!")

#Variables
clock       = pygame.time.Clock()
game_state  = "Main_Menu"
once        = False

cactus  = [pygame.image.load("Assets/Plants/Cactus1.png"),pygame.image.load("Assets/Plants/Cactus2.png")]
thorn   = [pygame.image.load("Assets/Plants/Thorn1.png"),pygame.image.load("Assets/Plants/Thorn2.png")]
spike   = [pygame.image.load("Assets/Plants/Spike.png"),pygame.image.load("Assets/Plants/Spike2.png")]
bird    = [pygame.image.load("Assets/Bird/Bird1.png"),pygame.image.load("Assets/Bird/Bird2.png")]
t_rex   = [pygame.image.load("Assets/T-Rex/T-RexRun1.png"),pygame.image.load("Assets/T-Rex/T-RexRun2.png")]
hit_effect = pygame.image.load("Assets/Other/HitEffect.png")

weapons     = [Skill.Dagger_Stats,Skill.Ice_Orb_Stats,Skill.Fire_Orb_Stats,Skill.Fireball_Stats,Skill.Arrow_Stats] 
weapon_list = []
projectiles = []
enemies     = []
spawn_rate  = 60

#Dict for Save_File
save = Save_File.Save

player          = Character.Dino()
cloud1          = Character.Cloud(pygame.image.load("Assets/Other/Cloud3.png"))
cloud2          = Character.Cloud(pygame.image.load("Assets/Other/Cloud2.png"))
pause_img       = pygame.image.load("Assets/Button/TopFrame_PauseButton.png")
pause_button    = Button.Button(screen,1244,8,pause_img)

#Variables for Game_Bg
x           = 0
y           = 440
game_speed  = 15 - (15 * (save["Add_GameSpeed"]*0.05))

#Variables for SKC
score           = 0
kill_count      = 0
coin_count      = 0

#Variables for Status_Bar
exp_limit = 100

#Variables for Time
mins    = 0
sec     = 0
mil_sec = 0

#Variables for Hit
collision_immune = False
collision_time = 0

#Function
def Game_Bg(screen):
    global game_speed, x, y
    game_bg_img = pygame.image.load("Assets/Other/ArenaBackground3.png")
    top_menu_img = pygame.image.load("Assets/Other/TopFrame3.png")
    bottom_menu_img = pygame.image.load("Assets/Other/BottomFrame2.png")
        
    screen.blit(top_menu_img,(0,0))
    screen.blit(bottom_menu_img,(0,461))
        
    bg_img_width = game_bg_img.get_width()
    screen.blit(game_bg_img,(x,y))
    screen.blit(game_bg_img,(bg_img_width + x,y))
    if x <= -bg_img_width:
        screen.blit(game_bg_img,(bg_img_width + x,y))
        x=0
    x -= game_speed

def SKC(player):
    global score, game_speed, kill_count, coin_count
    score += 1
        
    if score % 100 == 0:
        player._exp += 10
    if score % 500 == 0:
        game_speed += 1

    font = pygame.font.SysFont("timesnewroman",12)
    score_counter = font.render(str(score),True,(255,255,255))
    kill_counter = font.render(str(kill_count),True,(255,255,255))
    coin_counter = font.render(str(coin_count),True,(255,255,255))
            
    screen.blit(score_counter,(1246-(len(str(score))*6),34))
    screen.blit(kill_counter,(1246-(len(str(kill_count))*6),55))
    screen.blit(coin_counter,(1246-(len(str(coin_count))*6),78))

def Status_Bar(player):
    global exp_limit, game_state, once
    if player._exp >= exp_limit :
        player._exp      -= exp_limit
        exp_limit       +=  (exp_limit*0.1)
        exp_progress    = (player._exp/exp_limit)*1214
        pygame.draw.rect(screen, ("#2789cd"), pygame.Rect((12,12),(exp_progress,15)))
        game_state  = "Upgrade_Weapon"
        once        = False
            
    exp_progress = (player._exp/exp_limit)*1214
    pygame.draw.rect(screen, ("#2789cd"), pygame.Rect((12,12),(exp_progress,15)))

    health_bar = (player._health/player._max_health)*635
    pygame.draw.rect(screen, ("#cf0033"), pygame.Rect((65,491),(health_bar,18)))

    armor_bar = (player._protection/player._max_protection)*635
    pygame.draw.rect(screen, ("#616161"), pygame.Rect((65,513),(armor_bar,18)))

def Time():
    global mins, sec, mil_sec
    if mil_sec >= 30:
        mil_sec = 0
        sec += 1
        if sec >= 60:
            sec = 0
            mins += 1
    font = pygame.font.SysFont("timesnewroman",25)
    if len(str(mins))<2:
        mins_display = font.render("0" + str(mins),True,(255,255,255))
    else:
        mins_display = font.render(str(mins),True,(255,255,255))
    if len(str(sec))<2:
        sec_display = font.render("0" + str(sec),True,(255,255,255))
    else:
        sec_display = font.render(str(sec),True,(255,255,255))

    screen.blit(mins_display,(611,54))
    screen.blit(sec_display,(645,54))
    mil_sec += 1

def LPC(save):
    font1           = pygame.font.SysFont("timesnewroman",9)
    font2           = pygame.font.SysFont("timesnewroman",20)
    check_img       = pygame.image.load("Assets/Other/Check.png")
    list_upgrade    = list(save.values())
    coin_text       = font2.render(str(save["Coins"]),True,(255,255,255))
    price_text      = font1.render(str(save["Price"]),True,(255,255,255)) 
    
    price_pos       =[[388,360],[520,360],[652,360],[785,360],[918,360],[453,516],[586,516],[719,516],[852,516]]
    lvl_pos         = [[347,344],[479,344],[611,344],[744,344],[895,344],[412,500],[545,500],[678,500],[811,500]]
    
    screen.blit(coin_text,(915-len(str(save["Coins"]))*8,183))
    
    for i in range(9):
        screen.blit(price_text,(price_pos[i][0]-len(str(save["Price"]))*4,price_pos[i][1]))
        
    for i in range(9):
        for j in range(list_upgrade[i+6]):
            screen.blit(check_img,(lvl_pos[i][0]+(j*12),lvl_pos[i][1]))
        
def Result():
    font = pygame.font.SysFont("timesnewroman",20)
    time_text     = font.render("Survived for"+" "*11+": ",True,(255,255,255))
    score_text    = font.render("Score"+" "*22+": ",True,(255,255,255))
    kill_text     = font.render("Enemies defeated  : ",True,(255,255,255))
    coin_text     = font.render("Coin earned"+" "*12+": ",True,(255,255,255))
            
    if len(str(mins))<2 and len(str(sec))<2:
        time_result     = font.render("0" + str(mins)+":0"+str(sec),True,(255,255,255))
    elif len(str(mins))<2 and len(str(sec))>=2:
        time_result     = font.render("0" + str(mins)+":"+str(sec),True,(255,255,255))
    elif len(str(sec))<2 and len(str(mins))>=2:
        time_result     = font.render(str(mins)+":0"+str(sec),True,(255,255,255))
    else:
        time_result     = font.render(str(mins)+":"+str(sec),True,(255,255,255))
    score_result    = font.render(str(score),True,(255,255,255))
    kill_result     = font.render(str(kill_count),True,(255,255,255))
    coin_result     = font.render(str(coin_count),True,(255,255,255))
    
    screen.blit(time_text,(455,270))
    screen.blit(score_text,(455,295))
    screen.blit(kill_text,(455,320))
    screen.blit(coin_text,(455,345))
        
    screen.blit(time_result,(775,270))
    screen.blit(score_result,(820-(10*len(str(score))),295))
    screen.blit(kill_result,(820-(10*len(str(kill_count))),320))
    screen.blit(coin_result,(820-(10*len(str(coin_count))),345))

def Bottom_Display():
    font = pygame.font.SysFont("timesnewroman",22)
    if len(weapon_list) == 1:
        screen.blit(weapon_list[0]["slot_img"],(203,573))
        lvl_1     = font.render("Lvl "+str(weapon_list[0]["current_level"]),True,(255,255,255))
        screen.blit(lvl_1,(215,660))
    elif len(weapon_list) == 2:
        screen.blit(weapon_list[0]["slot_img"],(203,573))
        screen.blit(weapon_list[1]["slot_img"],(308,573))
        lvl_1     = font.render("Lvl "+str(weapon_list[0]["current_level"]),True,(255,255,255))
        screen.blit(lvl_1,(215,660))
        lvl_2     = font.render("Lvl "+str(weapon_list[1]["current_level"]),True,(255,255,255))
        screen.blit(lvl_2,(320,660))
    elif len(weapon_list) == 3:
        screen.blit(weapon_list[0]["slot_img"],(203,573))
        screen.blit(weapon_list[1]["slot_img"],(308,573))
        screen.blit(weapon_list[2]["slot_img"],(413,573))
        lvl_1     = font.render("Lvl "+str(weapon_list[0]["current_level"]),True,(255,255,255))
        screen.blit(lvl_1,(215,660))
        lvl_2     = font.render("Lvl "+str(weapon_list[1]["current_level"]),True,(255,255,255))
        screen.blit(lvl_2,(320,660))
        lvl_3     = font.render("Lvl "+str(weapon_list[2]["current_level"]),True,(255,255,255))
        screen.blit(lvl_3,(425,660))

def Spawn_Weapon(weapon_list):
    if weapon_list["name"] == "Fire Orb":
        projectiles.append(Skill.Fire_Orb(player))
    elif weapon_list["name"] == "Ice Orb":
        projectiles.append(Skill.Ice_Orb(player))
    elif weapon_list["name"] == "Fireball":
        projectiles.append(Skill.Fireball(player))
    elif weapon_list["name"] == "Dagger":
        projectiles.append(Skill.Dagger(player))
    elif weapon_list["name"] == "Arrow":
        projectiles.append(Skill.Arrow(player))

def Hit(obj1, obj2):
    if pygame.Rect.colliderect(obj1._hitbox,obj2._hitbox):
        if obj1._mask.overlap(obj2._mask,[obj2._hitbox.x-obj1._hitbox.x, obj2._hitbox.y-obj1._hitbox.y]):
            if obj1._protection <= 0:
                obj1._health -= obj2._damage
            else :
                if obj1._protection - obj2._damage < 0:
                    obj1._protection -= obj2._damage
                    obj1._health += obj1._protection
                    obj1._protection = 0
                else :
                    obj1._protection -= obj2._damage
            return True

#Mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #Main menu
    if game_state == "Main_Menu":
        if once == False:
            bg_img      = pygame.image.load("Assets/Other/Background3.png")
            start_img   = pygame.image.load("Assets/Button/PLAYButton.png")
            upgrade_img = pygame.image.load("Assets/Button/UPGRADEButton.png")
            exit_img    = pygame.image.load("Assets/Button/EXITButton.png")
    
            screen.blit(bg_img,(0,0))
            start_button    = Button.Button(screen,584,456,start_img)
            upgrade_button  = Button.Button(screen,584,544,upgrade_img)
            exit_button     = Button.Button(screen,584,632,exit_img)
            once            = True

        if start_button.Place():
            screen.fill((00,00,00))
            del start_button
            del upgrade_button
            del exit_button
            game_state  = "Select_Skill"
            once        = False
        elif upgrade_button.Place():
            del start_button
            del upgrade_button
            del exit_button
            game_state  = "Store"
            once        = False
        elif exit_button.Place():
            pygame.quit()
            
    elif game_state == "Store":
        if once == False :
            store_img   = pygame.image.load("Assets/Other/StoreMenu.png")
            storebg_img = pygame.image.load("Assets/Other/StoreMenuBg.png")
            back_img    = pygame.image.load("Assets/Button/BACKButton.png")
            buy_img     = pygame.image.load("Assets/Button/BUYButton.png")
            button_pos  = [[409,360],[541,360],[673,360],[806,360],[939,360],[474,516],[607,516],[740,516],[873,515]]
            buy_button  = []
            
            for a in range(9):
                buy_button.append(Button.Button(screen,button_pos[a][0],button_pos[a][1],buy_img))
            
            back_button = Button.Button(screen,309,174,back_img)
            screen.blit(storebg_img,(0,0))
            once = True
        
        screen.blit(store_img,(284,154))
            
        if buy_button[0].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Health"] == 5:
                pass
            else :
                save["Add_Health"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[1].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Protection"] == 5:
                pass
            else :
                save["Add_Protection"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[2].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Damage"] == 5:
                pass
            else :
                save["Add_Damage"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[3].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_PSpeed"] == 5:
                pass
            else :
                save["Add_PSpeed"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[4].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Quantity"] == 2:
                pass
            else :
                save["Add_Quantity"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[5].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Cooldown"] == 5:
                pass
            else :
                save["Add_Cooldown"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[6].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_GameSpeed"] == 5:
                pass
            else :
                save["Add_GameSpeed"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[7].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Exp"] == 5:
                pass
            else :
                save["Add_Exp"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if buy_button[8].Place():
            if save["Coins"] <= 0 or save["Coins"] - save["Price"] <= 0:
                pass
            elif save["Add_Coin"] == 5:
                pass
            else :
                save["Add_Coin"] += 1
                save["Coins"] -= save["Price"]
                save["Refund"] += save["Price"] * 0.8 //1
                save["Price"] = (save["Price"] * 1.2)//1
                
        if back_button.Place():
            file = open("Save_File.py", "w")
            file.write("Save = ")
            file.writelines(str(save))
            file.close()
            
            del back_button
            del buy_button
            once = False
            game_state = "Main_Menu"
                
        LPC(save)   
    
    elif game_state == "Select_Skill":
        if once == False :
            #Reset Variabel
            weapon_list         = []
            Skill.Fire_Orb_Stats["current_level"]   = 0
            Skill.Fire_Orb_Stats["damage"]          = 10
            Skill.Fire_Orb_Stats["speed"]           = 20
            Skill.Fire_Orb_Stats["quantity"]        = 1
            Skill.Fire_Orb_Stats["cooldown"]        = 30
            
            Skill.Ice_Orb_Stats["current_level"]    = 0
            Skill.Ice_Orb_Stats["damage"]           = 10
            Skill.Ice_Orb_Stats["speed"]            = 20
            Skill.Ice_Orb_Stats["quantity"]         = 1
            Skill.Ice_Orb_Stats["cooldown"]         = 30
            
            Skill.Dagger_Stats["current_level"]     = 0
            Skill.Dagger_Stats["damage"]            = 10
            Skill.Dagger_Stats["speed"]             = 20
            Skill.Dagger_Stats["quantity"]          = 1
            Skill.Dagger_Stats["cooldown"]          = 60
            
            Skill.Arrow_Stats["current_level"]      = 0
            Skill.Arrow_Stats["damage"]             = 10
            Skill.Arrow_Stats["speed"]              = 20
            Skill.Arrow_Stats["quantity"]           = 1
            Skill.Arrow_Stats["cooldown"]           = 70
            
            Skill.Fireball_Stats["current_level"]   = 0
            Skill.Fireball_Stats["damage"]          = 10
            Skill.Fireball_Stats["speed"]           = 20
            Skill.Fireball_Stats["quantity"]        = 1
            Skill.Fireball_Stats["cooldown"]        = 120
            
            select_img = pygame.image.load("Assets/Other/SkillSelectionMenu2.png")
            skill1_img = pygame.image.load("Assets/Skill/DaggerCard.png")
            skill2_img = pygame.image.load("Assets/Skill/IceOrbCard.png")
            skill3_img = pygame.image.load("Assets/Skill/FireOrbCard.png")
            skill4_img = pygame.image.load("Assets/Skill/FireballCard.png")

            skill1_button = Button.Button(screen,400,315,skill1_img)
            skill2_button = Button.Button(screen,680,315,skill2_img)
            skill3_button = Button.Button(screen,400,411,skill3_img)
            skill4_button = Button.Button(screen,680,411,skill4_img)
            
            screen.blit(select_img,(0,0))
            once = True
        
        if skill1_button.Place():
            weapon_list.append(Skill.Dagger_Stats)
            weapon_list[0]["current_level"] = 1
            game_state  = "Start_Game"
            once        = False
            del skill1_button
            del skill2_button
            del skill3_button
            del skill4_button
        elif skill2_button.Place():
            weapon_list.append(Skill.Ice_Orb_Stats)
            weapon_list[0]["current_level"] = 1
            game_state  = "Start_Game"
            once        = False
            del skill1_button
            del skill2_button
            del skill3_button
            del skill4_button
        elif skill3_button.Place():
            weapon_list.append(Skill.Fire_Orb_Stats)
            weapon_list[0]["current_level"] = 1
            game_state  = "Start_Game"
            once        = False
            del skill1_button
            del skill2_button
            del skill3_button
            del skill4_button
        elif skill4_button.Place():
            weapon_list.append(Skill.Fireball_Stats)
            weapon_list[0]["current_level"] = 1
            game_state  = "Start_Game"
            once        = False
            del skill1_button
            del skill2_button
            del skill3_button
            del skill4_button
        
    elif game_state == "Start_Game":
        if once == False :
            player              = Character.Dino()
            projectiles         = []
            enemies             = []
            spawn_rate          = 1
            
            #Variables for Game_Bg
            x                   = 0
            y                   = 440
            game_speed          = 15 - (15 * (save["Add_GameSpeed"]*0.05))
            
            #Variables for SKC
            score               = 0
            kill_count          = 0
            coin_count          = 0
            
            #Variables for Status_Bar
            exp_limit           = 100
            
            #Variables for Time
            mins                = 0
            sec                 = 0
            mil_sec             = 0
            
            #Variables for Hit
            collision_immune    = False
            collision_time      = 0
            
            #Dict for Save_File
            save = Save_File.Save
            
            once                = True
            
        screen.fill((81,223,229))
        Game_Bg(screen)
        SKC(player)
        Status_Bar(player)
        Time()
        
        if pause_button.Place():
            once        = False
            game_state  = "Paused"
        
        cloud1.Spawn(screen)
        cloud2.Spawn(screen)
        cloud1.Update(game_speed)
        cloud2.Update(game_speed)
        
        user_input = pygame.key.get_pressed()
        player.Spawn(screen)
        player.Update(user_input)
        
        Bottom_Display()
        
        if len(enemies)==0:
            if random.randint(0,3)==0:
                    enemies.append(Character.Cactus(cactus))
            elif random.randint(0,3)==1:
                    enemies.append(Character.Thorn(thorn))
            elif random.randint(0,4)==2:
                    enemies.append(Character.Spike(spike))
            elif random.randint(0,3)==2:
                    enemies.append(Character.T_Rex(t_rex))
            elif random.randint(0,3)==3:
                if random.randint(0,2)==0:
                    enemies.append(Character.Bird(bird,125))
                elif random.randint(0,2)==1:
                    enemies.append(Character.Bird(bird,175))
                elif random.randint(0,2)==2:
                    enemies.append(Character.Bird(bird,225))
        
        if len(weapon_list) >= 1:
            if spawn_rate % weapon_list[0]["cooldown"] - (save["Add_Cooldown"]*5) == 0:
                for i in range (weapon_list[0]["quantity"] + save["Add_Quantity"]):
                    Spawn_Weapon(weapon_list[0])
        if len(weapon_list) >= 2:
            if spawn_rate % weapon_list[1]["cooldown"] - (save["Add_Cooldown"]*5) == 0:
                for i in range (weapon_list[1]["quantity"] + save["Add_Quantity"]):
                    Spawn_Weapon(weapon_list[1])
        if len(weapon_list) == 3:
            if spawn_rate % weapon_list[2]["cooldown"] - (save["Add_Cooldown"]*5) == 0:
                for i in range (weapon_list[2]["quantity"] + save["Add_Quantity"]):
                    Spawn_Weapon(weapon_list[2])
        spawn_rate+=1
        
        for enemy in enemies:
            enemy.Spawn(screen)
            enemy.Update(game_speed, enemies)
        
        for projectile in projectiles:
            projectile.Spawn(screen)
            projectile.Update(projectiles)
            
        if len(enemies) >= 1:
            if pygame.time.get_ticks() - collision_time > 1000:
                collision_immune = False
            if collision_immune == False and Hit(player,enemies[0]):
                if player.Death():
                    player.Spawn(screen)
                    once        = False
                    game_state  = "Game_Result"
                collision_immune    = True
                collision_time      = pygame.time.get_ticks()
            if collision_immune == True and pygame.time.get_ticks() - collision_time < 50:
                screen.blit(hit_effect,(0,101))

        if len(projectiles) > 0 and len(enemies) > 0:
            for no in range (len(projectiles)):
                if no >= len(projectiles):
                    pass
                else :
                    Hit(enemies[0],projectiles[no])
                    if projectiles[no]._mask.overlap(enemies[0]._mask,[enemies[0]._hitbox.x-projectiles[no]._hitbox.x, enemies[0]._hitbox.y-projectiles[no]._hitbox.y]) or projectiles[no]._hitbox.x >= 1400:
                        projectiles.pop(no)
            if enemies[0].Death(enemies):
                kill_count += 1
                coin_count += random.randint(0,score//100)
                get_exp = random.randint(1,kill_count*2)
                player._exp +=  get_exp + (get_exp*(save["Add_Exp"]*0.1))
        
    elif game_state == "Upgrade_Weapon":
        if once == False :
            upgrade_img     = pygame.image.load("Assets/Other/UpgradeMenu.png")
            up_card_img     = pygame.image.load("Assets/Other/UpgradeSlot.png")
            skip_img        = pygame.image.load("Assets/Button/SKIPButton.png")
            skip_button     = Button.Button(screen,1010,438,skip_img)
            font            = pygame.font.SysFont("timesnewroman",14)
            up_list         = []
            name            = []
            lvl             = []
            desc            = []
            button          = []
            y_pos           = 60
            new             = 0
            up              = 0
            finish          = 0

            if len(weapon_list) == 3:
                for i in weapon_list:
                    if i["current_level"] == 5:
                        finish += 1
                    elif i["current_level"] > 0 and i["current_level"] < 5:
                        up_list.append(i)
                        up += 1
            elif len(weapon_list) < 3 :
                for i in weapon_list:
                    if i["current_level"] == 5:
                        finish += 1
                    elif i["current_level"] > 0 and i["current_level"] < 5:
                        up_list.append(i)
                        up += 1
                new = 3-up
        
            if new != 0:
                for a in range(new):
                    loop = True
                    while loop:
                        add = weapons[random.randint(0,len(weapons)-1)]
                        if len(up_list) == 0:
                            loop = False
                        elif add["current_level"] == 5 :
                            pass
                        else :
                            for i in weapon_list:
                                if i["name"] != add["name"]:
                                    loop = False
                                else :
                                    loop = True
                                    break
                                
                            for i in up_list:
                                if i["name"] != add["name"]:
                                    loop = False
                                else :
                                    loop = True
                                    break
                    up_list.append(add)
            
            for i in range (len(up_list)):
                if up_list[i]["current_level"] > 0:
                    button.append(Button.Button(screen,836,500+(i*y_pos),up_card_img))
                elif up_list[i]["current_level"] == 0:
                    button.append(Button.Button(screen,836,500+(i*y_pos),up_card_img))

            for i in range (len(up_list)):
                name.append(font.render(up_list[i]["name"],True,(255,255,255)))
                lvl.append(font.render("Lvl "+str(up_list[i]["current_level"]+1),True,(255,255,255)))
                desc.append(font.render(str(list(up_list[i].values())[up_list[i]["current_level"]+1][1]),True,(255,255,255)))
            
            if len(button)== 0 :
                game_state = "Start_Game"
            else :
                screen.blit(upgrade_img,(0,0))
            once = True
        
        if len(button)== 0 :
            pass
        elif skip_button.Place():
            game_state = "Start_Game"
                    
        if len(button)>= 1 :
            if button[0].Place():
                if up_list[0]["current_level"] == 0:
                    weapon_list.append(up_list[0])
                    up_list[0]["Upgrade"](up_list[0]["name"])
                elif up_list[0]["current_level"] >= 1:
                    up_list[0]["Upgrade"](up_list[0]["name"])
                elif up_list[0]["current_level"] == 5:
                    up_list[0]["Upgrade"](up_list[0]["name"])
                game_state = "Start_Game"

        if len(button)>= 2 :
            if button[1].Place():
                if up_list[1]["current_level"] == 0:
                    weapon_list.append(up_list[1])
                    up_list[1]["Upgrade"](up_list[1]["name"])
                elif up_list[1]["current_level"] >= 1:
                    up_list[1]["Upgrade"](up_list[1]["name"])
                elif up_list[1]["current_level"] == 5:
                    up_list[1]["Upgrade"](up_list[1]["name"])
                game_state = "Start_Game"

        if len(button) == 3 :
            if button[2].Place():
                if up_list[2]["current_level"] == 0:
                    weapon_list.append(up_list[2])
                    up_list[2]["Upgrade"](up_list[2]["name"])
                elif up_list[2]["current_level"] >= 1:
                    up_list[2]["Upgrade"](up_list[2]["name"])
                elif up_list[2]["current_level"] == 5:
                    up_list[2]["Upgrade"](up_list[2]["name"])
                game_state = "Start_Game"

        for i in range(len(up_list)):
            screen.blit(up_list[i]["upgrade_img"],(847,511+(i*y_pos)))
            screen.blit(name[i],(889,509+(i*y_pos)))
            screen.blit(lvl[i],(1120,509+(i*y_pos)))
            screen.blit(desc[i],(889,530+(i*y_pos)))
    
    elif game_state == "Paused":
        if once == False:
            pause_menu_img = pygame.image.load("Assets/Other/Pause_Menu.png")
            resume_img = pygame.image.load("Assets/Button/RESUMEButton.png")
            menu_img = pygame.image.load("Assets/Button/MENUButton.png")

            screen.blit(pause_menu_img,(0,0))
            resume_button = Button.Button(screen,580,304,resume_img)
            menu_button = Button.Button(screen,580,390,menu_img)
            once = True
        
        if resume_button.Place():
            game_state = "Start_Game"
            del resume_button
            del menu_button
        elif menu_button.Place():
            game_state = "Game_Result"
            once = False
            del resume_button
            del menu_button
        
    elif game_state == "Game_Result":
        if once == False:
            #Save Result
            if save["Play_Time"] <= (mins*60)+sec :
                save["Play_Time"] = (mins*60)+sec
            if save["Top_Score"] <= score :
                save["Top_Score"] = score
            if save["Most_Kill"] <= kill_count :
                save["Most_Kill"] = kill_count
            save["Coins"] += (coin_count + (coin_count*(save["Add_Coin"]*0.1))//1)
            
            file = open("Save_File.py", "w")
            file.write("Save = ")
            file.writelines(str(save))
            file.close()
            
            result_menu_img = pygame.image.load("Assets/Other/GameOver_Menu.png")
            play_again_img = pygame.image.load("Assets/Button/PLAYAGAINButton.png")
            main_menu_img = pygame.image.load("Assets/Button/MAINMENUButton.png")

            screen.blit(result_menu_img,(0,0))
            play_again_button = Button.Button(screen,698,470,play_again_img)
            main_menu_button = Button.Button(screen,462,470,main_menu_img)
            once = True
        
        Result()
        
        if play_again_button.Place():
            del play_again_button
            del main_menu_button
            once        = False
            game_state  = "Select_Skill"
        elif main_menu_button.Place():
            del play_again_button
            del main_menu_button
            once        = False
            game_state  = "Main_Menu"
            
    clock.tick(30)
    pygame.display.update() 
