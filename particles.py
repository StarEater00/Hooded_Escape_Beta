#!/usr/bin/python3

import pygame
import random
from tiles import AnimatedTile

class Particles(AnimatedTile):
    def __init__(self,size,pos,groups):
        super().__init__(size,pos,'../graphics/particles/',{'idle':[],'walk':[],'run':[],'jump':[],},groups,'jump')
        self.pos = pos 
        self.rect = self.image.get_rect(bottomleft = (pos[0]-30,pos[1]))     
        if self.status == 'walk':
            self.rect = self.image.get_rect(bottomleft = (self.pos[0]-10  ,self.pos[1]))     
    def walk_rect(self):
        if self.status == 'jump' and self.frame_index >= 5:
            self.kill() 
        if self.status == 'walk':
            self.rect.x += 2.5
        #if self.frame_index >= 5:
        #    self.status = 'idle'
            #if self.frame_index >= 5:
            #    self.kill()
        #if self.status == 'idle':
        #    self.image = pygame.image.load(self.animations[self.status]) 
        pass
        
        #if self.frame_index >= 2 and self.status == 'idle' :
        #if self.frame_index >= 4:   
           #self.kill()
        #if self.status == 'idle':
        #    self.kill()
        #if self.frame_index >= 6:
        #    self.kill()
    def destroy(self):
        if self.frame_index >=4 and self.status == 'run':
            self.kill()

    def update(self,shift): 
        #self.draw_walk()    
        self.animate(.29)
        self.destroy() 
        self.walk_rect() 
        #self.run_()
        #self.walk_()
        #print(self.frame_index)
    #    self.rect.x += shift
        #self.delete()



#class Particles(pygame.sprite.Sprite):
#    def __init__(self,x_coor,y_coor,groups):    
#        super().__init__(groups)
#        self.x_coor = x_coor
#        self.y_coor = y_coor
#        self.x_velocity = random.randrange(-2,0)*2
#        self.y_velocity = random.randrange(-1,5)
#        self.lifetime = 0
#        self.image = pygame.Surface((16,16),pygame.SRCALPHA)
#        self.image.fill((0,0,0,0))
#        self.rect = self.image.get_rect(center = (self.x_coor,self.y_coor))
#        pygame.draw.circle(self.image,(155,0,0),(8,8),2)
#        
#    
#
#    def update(self,world_shift):
#        self.rect[0] += self.x_velocity
#        self.rect[1] += self.y_velocity
