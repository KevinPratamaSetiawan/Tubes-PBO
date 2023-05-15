import pygame
import os
import random
from abc import ABC, abstractmethod

import Save_File

save = Save_File.Save

def Upgrade(name):
    if name == "Fire Orb":
        if Fire_Orb_Stats["current_level"] == 0:
            Fire_Orb_Stats["current_level"] = 1
        elif Fire_Orb_Stats["current_level"] == 1:
            Fire_Orb_Stats["current_level"] = 2
            Fire_Orb_Stats["quantity"] += 1
        elif Fire_Orb_Stats["current_level"] == 2:
            Fire_Orb_Stats["current_level"] = 3
            Fire_Orb_Stats["damage"] += 5
        elif Fire_Orb_Stats["current_level"] == 3:
            Fire_Orb_Stats["current_level"] = 4
            Fire_Orb_Stats["cooldown"] -= 30
        elif Fire_Orb_Stats["current_level"] == 4:
            Fire_Orb_Stats["current_level"] = 5
            Fire_Orb_Stats["damage"] += 20
    elif name == "Ice Orb":
        if Ice_Orb_Stats["current_level"] == 0:
            Ice_Orb_Stats["current_level"] = 1
        elif Ice_Orb_Stats["current_level"] == 1:
            Ice_Orb_Stats["current_level"] = 2
            Ice_Orb_Stats["quantity"] += 1
        elif Ice_Orb_Stats["current_level"] == 2:
            Ice_Orb_Stats["current_level"] = 3
            Ice_Orb_Stats["damage"] += 10
        elif Ice_Orb_Stats["current_level"] == 3:
            Ice_Orb_Stats["current_level"] = 4
            Ice_Orb_Stats["cooldown"] -= 20
        elif Ice_Orb_Stats["current_level"] == 4:
            Ice_Orb_Stats["current_level"] = 5
            Ice_Orb_Stats["damage"] += 20
    elif name == "Fireball":
        if Fireball_Stats["current_level"] == 0:
            Fireball_Stats["current_level"] = 1
        elif Fireball_Stats["current_level"] == 1:
            Fireball_Stats["current_level"] = 2
            Fireball_Stats["cooldown"] -= 50
        elif Fireball_Stats["current_level"] == 2:
            Fireball_Stats["current_level"] = 3
            Fireball_Stats["damage"] += 20
        elif Fireball_Stats["current_level"] == 3:
            Fireball_Stats["current_level"] = 4
            Fireball_Stats["cooldown"] -= 100
        elif Fireball_Stats["current_level"] == 4:
            Fireball_Stats["current_level"] = 5
            Fireball_Stats["quantity"] += 1
    elif name == "Dagger":
        if Dagger_Stats["current_level"] == 0:
            Dagger_Stats["current_level"] = 1
        elif Dagger_Stats["current_level"] == 1:
            Dagger_Stats["current_level"] = 2
            Dagger_Stats["speed"] += 10
        elif Dagger_Stats["current_level"] == 2:
            Dagger_Stats["current_level"] = 3
            Dagger_Stats["damage"] += 5
        elif Dagger_Stats["current_level"] == 3:
            Dagger_Stats["current_level"] = 4
            Dagger_Stats["quantity"] += 1
        elif Dagger_Stats["current_level"] == 4:
            Dagger_Stats["current_level"] = 5
            Dagger_Stats["damage"] += 10
    elif name == "Arrow":
        if Arrow_Stats["current_level"] == 0:
            Arrow_Stats["current_level"] = 1
        elif Arrow_Stats["current_level"] == 1:
            Arrow_Stats["current_level"] = 2
            Arrow_Stats["cooldown"] -= 10
        elif Arrow_Stats["current_level"] == 2:
            Arrow_Stats["current_level"] = 3
            Arrow_Stats["damage"] += 20
        elif Arrow_Stats["current_level"] == 3:
            Arrow_Stats["current_level"] = 4
            Arrow_Stats["speed"] += 20
        elif Arrow_Stats["current_level"] == 4:
            Arrow_Stats["current_level"] = 5
            Arrow_Stats["quantity"] += 1

Dagger_Stats = {
    "current_level" : 0,
    "lvl_1_text" : ["lvl 1", "Throwing knife."],
    "lvl_2_text" : ["lvl 2", "+10 speed."],
    "lvl_3_text" : ["lvl 3", "+5 damage."],
    "lvl_4_text" : ["lvl 4", "+1 projectile."],
    "lvl_5_text" : ["lvl 5", "+10 damage."],
    "name" : "Dagger",
    "dict_name" : "Dagger_Stats",
    "damage" : 10,
    "speed" : 10,
    "quantity" : 1,
    "cooldown" : 180,
    "img" : pygame.image.load("Assets/Skill/Dagger.png"),
    "slot_img" : pygame.image.load("Assets/Skill/DaggerSkill1.png"),
    "upgrade_img" : pygame.image.load("Assets/Skill/DaggerSkill.png"),
    "Upgrade" : Upgrade
    }

Ice_Orb_Stats = {
    "current_level" : 0,
    "lvl_1_text" : ["lvl 1", "Quite Freezing !"],
    "lvl_2_text" : ["lvl 2", "+1 projectile."],
    "lvl_3_text" : ["lvl 3", "+10 damage."],
    "lvl_4_text" : ["lvl 4", "-20 cooldown."],
    "lvl_5_text" : ["lvl 5", "+20 damage."],
    "name" : "Ice Orb",
    "dict_name" : "Ice_Orb_Stats",
    "damage" : 5,
    "speed" : 15,
    "quantity" : 1,
    "cooldown" : 120,
    "img" : pygame.image.load("Assets/Skill/IceOrb.png"),
    "slot_img" : pygame.image.load("Assets/Skill/IceOrbSkill1.png"),
    "upgrade_img" : pygame.image.load("Assets/Skill/IceOrbSkill.png"),
    "Upgrade" : Upgrade
    }

Fire_Orb_Stats = {
    "current_level" : 0,
    "lvl_1_text" : ["lvl 1", "Shooting fire orb to the front."],
    "lvl_2_text" : ["lvl 2", "Fires 1 more projectile."],
    "lvl_3_text" : ["lvl 3", "+5 damage"],
    "lvl_4_text" : ["lvl 4", "-30 cooldown."],
    "lvl_5_text" : ["lvl 5", "+20 damage"],
    "name" : "Fire Orb",
    "dict_name" : "Fire_Orb_Stats",
    "damage" : 5,
    "speed" : 15,
    "quantity" : 1,
    "cooldown" : 120,
    "img" : pygame.image.load("Assets/Skill/FireOrb.png"),
    "slot_img" : pygame.image.load("Assets/Skill/FireOrbSkill1.png"),
    "upgrade_img" : pygame.image.load("Assets/Skill/FireOrbSkill.png"),
    "Upgrade" : Upgrade
    }

Fireball_Stats = {
    "current_level" : 0,
    "lvl_1_text" : ["lvl 1", "Big fireball."],
    "lvl_2_text" : ["lvl 2", "Cooldown -50"],
    "lvl_3_text" : ["lvl 3", "Damage +20."],
    "lvl_4_text" : ["lvl 4", "Cooldown -100"],
    "lvl_5_text" : ["lvl 5", "Fires 1 more projectile."],
    "name" : "Fireball",
    "dict_name" : "Fireball_Stats",
    "damage" : 25,
    "speed" : 20,
    "quantity" : 1,
    "cooldown" : 300,
    "img" : pygame.image.load("Assets/Skill/Fireball.png"),
    "slot_img" : pygame.image.load("Assets/Skill/FireballSkill1.png"),
    "upgrade_img" : pygame.image.load("Assets/Skill/FireballSkill.png"),
    "Upgrade" : Upgrade
    }

Arrow_Stats = {
    "current_level" : 0,
    "lvl_1_text" : ["lvl 1", "Arrow init."],
    "lvl_2_text" : ["lvl 2", "Cooldown -10"],
    "lvl_3_text" : ["lvl 3", "Damage +20."],
    "lvl_4_text" : ["lvl 4", "Speed +20"],
    "lvl_5_text" : ["lvl 5", "Fires 1 more projectile."],
    "name" : "Arrow",
    "dict_name" : "Arrow_Stats",
    "damage" : 10,
    "speed" : 20,
    "quantity" : 1,
    "cooldown" : 70,
    "img" : pygame.image.load("Assets/Skill/Arrow.png"),
    "slot_img" : pygame.image.load("Assets/Skill/ArrowSkill1.png"),
    "upgrade_img" : pygame.image.load("Assets/Skill/ArrowSkill.png"),
    "Upgrade" : Upgrade
    }

class Fire_Orb:
    def __init__(self,player):
        self._stats = Fire_Orb_Stats
        self._img = self._stats["img"]
        self._damage = (self._stats["damage"] + (self._stats["damage"]*(save["Add_Damage"]*0.1)))//1
        self._hitbox = self._img.get_rect(center=( player._hitbox.x + random.randint(95, 120),player._hitbox.y + random.randint(30, 60)))
        self._mask = pygame.mask.from_surface(self._img)

    def Update(self,projectiles):
        self._hitbox.x += self._stats["speed"] + (self._stats["speed"]*(save["Add_PSpeed"]*0.2))//1

    def Spawn(self,screen):
        screen.blit(self._img,self._hitbox)

class Fireball:
    def __init__(self,player):
        self._stats = Fireball_Stats
        self._img = self._stats["img"]
        self._damage = (self._stats["damage"] + (self._stats["damage"]*(save["Add_Damage"]*0.1)))//1
        self._hitbox = self._img.get_rect(center=( player._hitbox.x + random.randint(95, 120),player._hitbox.y + random.randint(30, 60)))
        self._mask = pygame.mask.from_surface(self._img)

    def Update(self,projectiles):
        self._hitbox.x += self._stats["speed"] + (self._stats["speed"]*(save["Add_PSpeed"]*0.2))//1

    def Spawn(self,screen):
        screen.blit(self._img,self._hitbox)

class Ice_Orb:
    def __init__(self,player):
        self._stats = Ice_Orb_Stats
        self._img = self._stats["img"]
        self._damage = (self._stats["damage"] + (self._stats["damage"]*(save["Add_Damage"]*0.1)))//1
        self._hitbox = self._img.get_rect(center=( player._hitbox.x + random.randint(95, 120),player._hitbox.y + random.randint(30, 60)))
        self._mask = pygame.mask.from_surface(self._img)

    def Update(self,projectiles):
        self._hitbox.x += self._stats["speed"] + (self._stats["speed"]*(save["Add_PSpeed"]*0.2))//1

    def Spawn(self,screen):
        screen.blit(self._img,self._hitbox)

class Dagger:
    def __init__(self,player):
        self._stats = Dagger_Stats
        self._img = self._stats["img"]
        self._damage = (self._stats["damage"] + (self._stats["damage"]*(save["Add_Damage"]*0.1)))//1
        self._hitbox = self._img.get_rect(center=( player._hitbox.x + random.randint(95, 120),player._hitbox.y + random.randint(30, 60)))
        self._mask = pygame.mask.from_surface(self._img)

    def Update(self,projectiles):
        self._hitbox.x += self._stats["speed"] + (self._stats["speed"]*(save["Add_PSpeed"]*0.2))//1

    def Spawn(self,screen):
        screen.blit(self._img,self._hitbox)

class Arrow:
    def __init__(self,player):
        self._stats = Arrow_Stats
        self._img = self._stats["img"]
        self._damage = (self._stats["damage"] + (self._stats["damage"]*(save["Add_Damage"]*0.1)))//1
        self._hitbox = self._img.get_rect(center=( player._hitbox.x + random.randint(95, 120),player._hitbox.y + random.randint(30, 60)))
        self._mask = pygame.mask.from_surface(self._img)

    def Update(self,projectiles):
        self._hitbox.x += self._stats["speed"] + (self._stats["speed"]*(save["Add_PSpeed"]*0.2))//1

    def Spawn(self,screen):
        screen.blit(self._img,self._hitbox)