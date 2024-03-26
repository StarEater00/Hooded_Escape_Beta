#!/usr/bin/python3

import pygame
from support import import_folder
from tiles import AnimatedTile
class Player(AnimatedTile):
    def __init__(self,size,pos,groups):
        super().__init__(size,pos,'../graphics/player/',{'idle':[],'run':[],'attack':[]},groups)
        self.direction = pygame.math.Vector2(0,0)
        self.rect.w,self.rect.h = self.image.get_size() 
        self.jump_speed = -16
        self.gravity = .8
        self.speed = 3
        self.facing_right =True 
    def jump(self):
        self.direction.y = self.jump_speed 

    def apply_movement(self):
        keys = pygame.key.get_pressed()
        self.status = 'run'
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False 
            
        else:
            self.direction.x = 0
            self.status = 'idle'
        
        if keys[pygame.K_SPACE]:
            self.jump() 
        if keys[pygame.K_f]:
            self.status = 'attack'
    def apply_gravity(self):
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y
    def update(self,ani_speed):
        self.animate(0.2)
        self.apply_movement()
        self.reverse_image()
