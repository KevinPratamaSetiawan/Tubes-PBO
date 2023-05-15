import pygame
import os
import random
from abc import ABC, abstractmethod

import Save_File
  
class Dino :
    _save = Save_File.Save
    _x_position = 50
    _y_position = 348
    _y_duck_position = 380
    _jump_velocity = 8
    
    def __init__(self):
        self._run_img = [pygame.image.load("Assets/Dino/DinoRun1.png"),pygame.image.load("Assets/Dino/DinoRun2.png")]
        self._duck_img = [pygame.image.load("Assets/Dino/DinoDuck1.png"),pygame.image.load("Assets/Dino/DinoDuck2.png")]
        self._jump_img = [pygame.image.load("Assets/Dino/DinoStart.png")]
        self._dead_img = [pygame.image.load("Assets/Dino/DinoDead.png")]

        self._dino_run = True
        self._dino_jump = False
        self._dino_duck = False
        self._dino_dead = False

        self._max_health = 100 + (self._save["Add_Health"] * 20)
        self._health = self._max_health
        self._max_protection = 100 + (self._save["Add_Protection"] * 10)
        self._protection = self._max_protection
        self._exp = 0
        self._step_count = 0
        self._jump_vel = self._jump_velocity
        self.__img = self._run_img[self._step_count]
        self._hitbox = self.__img.get_rect()
        self._hitbox.x = self._x_position
        self._hitbox.y = self._y_position
        self._mask = pygame.mask.from_surface(self.__img)

    def Update(self,user_input):
        if self._dino_run:
            self.Running_Dino()
        if self._dino_jump:
            self.Jumping_Dino()
        if self._dino_duck:
            self.Ducking_Dino()

        if self._step_count >= 10:
            self._step_count = 0

        if user_input[pygame.K_UP] and not self._dino_jump:
            self._dino_run = False
            self._dino_jump = True
            self._dino_duck = False
            self._dino_dead = False
        elif user_input[pygame.K_DOWN] and not self._dino_jump:
            self._dino_run = False
            self._dino_jump = False
            self._dino_duck = True
            self._dino_dead = False
        elif not (self._dino_jump or user_input[pygame.K_DOWN]):
            self._dino_run = True
            self._dino_jump = False
            self._dino_duck = False
            self._dino_dead = False

    def Running_Dino(self):
        self.__img = self._run_img[self._step_count//5]
        self._hitbox = self.__img.get_rect()
        self._hitbox.x = self._x_position
        self._hitbox.y = self._y_position
        self._mask = pygame.mask.from_surface(self.__img)
        self._step_count += 1

    def Jumping_Dino(self):
        self.__img = self._jump_img[0]
        self._mask = pygame.mask.from_surface(self.__img)
        if self._dino_jump :
            self._hitbox.y -= self._jump_vel * 4
            self._jump_vel -= 0.8
        if self._jump_vel < -self._jump_velocity:
            self._dino_jump = False
            self._jump_vel = self._jump_velocity

    def Ducking_Dino(self):
        self.__img = self._duck_img[self._step_count//5]
        self._hitbox = self.__img.get_rect()
        self._hitbox.x = self._x_position
        self._hitbox.y = self._y_duck_position
        self._mask = pygame.mask.from_surface(self.__img)
        self._step_count += 1

    def Death(self):
        if self._health <= 0 :
            self._dino_run = False
            self._dino_jump = False
            self._dino_duck = False
            self._dino_dead = True
            self.__img = self._dead_img[0]
            return self._dino_dead
    
    def Spawn(self,screen):
        screen.blit(self.__img,(self._hitbox.x, self._hitbox.y))

class Obstacle:
    def __init__(self, img, obstacle_type, y_position):
        self._health = 50 + random.randint(0,100)
        self._protection = 0
        self._img = img
        self._obstacle_type = obstacle_type
        self._hitbox = self._img[self._obstacle_type].get_rect()
        self._mask = pygame.mask.from_surface(self._img[obstacle_type])
        self._hitbox.x = 1340
        self._hitbox.y = y_position

    def Update(self,game_speed,enemies):
        self._hitbox.x -= game_speed
        if self._hitbox.x <= -self._hitbox.width:
            enemies.pop()

    @abstractmethod
    def Spawn(self, screen):
        pass

    def Death(self,enemies):
        if self._health <= 0:
            enemies.pop()
            return True

class Cactus(Obstacle):
    def __init__(self,img):
        self._cactus_type = random.randint(0,1)
        self._damage = 5 + random.randint(0,30)
        super().__init__(img, self._cactus_type, 345)

    def Spawn(self, screen):
        screen.blit(self._img[self._cactus_type], self._hitbox)

class Thorn(Obstacle):
    def __init__(self,image):
        self._thorn_type = random.randint(0,1)
        self._damage = 10 + random.randint(0,25)
        super().__init__(image, self._thorn_type, 323)

    def Spawn(self, screen):
        screen.blit(self._img[self._thorn_type], self._hitbox)

class Spike(Obstacle):
    def __init__(self,img):
        self._spike_floor = img[0]
        self._damage = 8 + random.randint(0,20)
        self._floor_rect = self._spike_floor.get_rect()
        self._floor_rect.x = 1280
        self._floor_rect.y = 440
        super().__init__(img,1,439)

    def Update(self,game_speed,enemies):
        self._floor_rect.x -= game_speed
        self._hitbox.x -= game_speed
        if self._floor_rect.x <= -self._floor_rect.width and self._hitbox.x <= -self._hitbox.width:
            enemies.pop()

    def Spawn(self, screen):
        screen.blit(self._img[1], self._hitbox)
        screen.blit(self._spike_floor, self._floor_rect)

class T_Rex(Obstacle):
    def __init__(self,img):
        self._img = img
        self._damage = 20 + random.randint(0,40)
        super().__init__(img,0,340)
        self._index = 0

    def Spawn(self,screen):
        if self._index == 10:
            self._index = 0
        screen.blit(self._img[self._index//5],self._hitbox)
        self._index += 1

class Bird(Obstacle):
    def __init__(self,img,y_position):
        self._img = img
        self._damage = 5 + random.randint(0,75)
        super().__init__(img,0,y_position)
        self._index = 0

    def Spawn(self,screen):
        if self._index == 10:
            self._index = 0
        screen.blit(self._img[self._index//5],self._hitbox)
        self._index += 1
            

class Cloud:
    def __init__(self, img):
        self._x = 1280 + random.randint(500, 700)
        self._y = random.randint(105, 200)
        self._img = img
        self._width = self._img.get_width()

    def Update(self,game_speed):
        self._x -= game_speed
        if self._x < -self._width:
            self._x = 1280 + random.randint(0, 10)
            self._y = random.randint(105, 200)

    def Spawn(self, screen):
        screen.blit(self._img,(self._x,self._y))