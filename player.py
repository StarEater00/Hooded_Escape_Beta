#!/usr/bin/python3

import pygame
from tiles import AnimatedTile
from support import import_folder
from particles import Particles
import random
class Player(AnimatedTile):
    def __init__(self,size,pos,groups,window,create_particles,destroy_particles):
        super().__init__(size,pos,'../graphics/player/',{'idle':[],'walk':[],'run':[],'attack':[],'jump':[]},groups,'idle')
         
        self.direction = pygame.math.Vector2(0,0) 
        self.speed = 3 
        self.jump_speed = -16
        self.gravity = 0.8
        #self.rect.w,self.rect.h = self.image.get_size()                           #15
        #self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.is_walking = True
        self.rect = pygame.Rect(self.rect.x,self.rect.y,18,26)
        self.rect =  self.image.get_rect(topleft = self.rect.topleft)
        self.create_particles = create_particles
        self.destroy_particles = destroy_particles
        #self.import_particles()
        #self.rect.h = 25
        self.window = window
        self.lifetime = 0
        self.part_count = 0 
    def apply_gravity(self):
        self.direction.y += self.gravity 
        #print(self.direction.y, self.gravity )#your adding .8 to 0
        self.rect.y += self.direction.y
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'
            self.part_status = 'idle'
        if self.direction.x == 1 or self.direction.x == -1:
            self.status = 'walk'
            self.part_status = 'walk'
        if self.direction.x >= 2 or self.direction.x <= -2:
            self.status = 'run' 
            self.part_status = 'run'
        if self.direction.y < 0:        #if self.direction.y > 0 
            self.status = 'jump' 
            self.part_status = 'jump'
            #self.status = 'attack'
    def jump(self):
        #for i in range(self.jump_speed,0):
        self.direction.y = self.jump_speed
    def apply_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1 
            self.facing_right = True
            #self.create_particles()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_particles()
        if keys[pygame.K_a]:
            self.direction.x = -1 
            self.facing_right = False
        if keys[pygame.K_LSHIFT]:
            self.direction.x *= 3 
            #self.create_particles()
            #if keys[pygame.K_LSHIFT]:
            #    self.direction.x = -2 
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = 0    
    def particle_effect(self):
        pass 
        #if self.direction.x == 1 and self.animation_timer == 0:  
        #    particles = self.create_particles()
        #    self.animation_timer += 1
        #
        #particles = self.create_particles() 
        #if self.direction.x == 0 and self.animation_timer == 0: 
        #    self.destroy_particles()
            
        if self.animation_timer == 0:
            if self.direction.x == 1:
                particles = self.create_particles() 
                self.animation_timer += 1
        if self.direction.x == 0:
            self.destroy_particles()
            self.animation_timer = 0 
        #if particles == None:
        #    particles = self.create_particles()
       # if self.animation_timer == 1:
            
       #     if self.direction.x == 0:
                #particles = self.create_particles()
                #particles.status = 'idle'
                
       #         pass 
                #if self.frame_index > 3: 
                    #self.destroy_particles()
                #self.animation_timer = 0
        #if self.animation_timer == 1:
        #    self.create_particles()

        #if particles.frame_index < 4:

        #    if self.animation_timer == 1:
        #        particles = self.create_particles()
        #        self.animation_timer = 0
        #    if self.frame_index > 3:
        #        self.destroy_particles()
        #    particles = self.create_particles()
         
        #if self.status == 'idle' and self.animation_timer == 0:
        #    particles = self.create_particles()
        #    self.animation_timer = 1 
            #self.animation_timer = 0
        #if self.animation_timer = 0:
        #    self.destroy_particles()

            #self.create_particles() 
            #if self.frame_index > 3:
            #    self.destroy_particles()
            #self.destroy_particles() 
        
        #    particles = self.create_particles()

    def update(self,shift):
        self.animate_particles(self.rect.bottomleft[0] - 10,self.rect.bottomleft[1]-5,.15)
        self.animate(0.1)
        #self.particle_effect()
        self.get_status()
        #self.rect.x += self.direction.x * self.speed 
        #self.rect.x += shift
        self.apply_movement()
        #self.apply_particles()
        self.reverse_image()
        #self.resize(18,30)
        
