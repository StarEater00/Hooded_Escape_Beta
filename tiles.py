#!/usr/bin/python3
import pygame
from support import import_folder
class Tile(pygame.sprite.Sprite):
    def __init__(self,size,pos,surf,groups):
        super().__init__(groups)
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=(pos))
    def update(self,shift):
        #here is where you can move the tiles left or right accordingly
        self.rect.x += shift
class StaticTile(Tile):
    def __init__(self,size,pos,surf,groups):
        super().__init__(size,pos,surf,groups)
        self.image = surf
    def update(self,shift):
        self.rect.x += shift
#class Tree(StaticTile):
#    def __init__(self,size,pos,surf,groups):
#        super().__init__(size,pos,surf,groups)
#        y = pos[1]; x = pos[0]
#        y_offset = y - size
#        self.rect = self.image.get_rect(topright=(x,y_offset))
#class Platform(StaticTile):
#    def __init__(self,size,pos,surf,groups,display):
#        super().__init__(size,pos,surf,groups)
#        x,y,width,height = self.image.get_rect(bottomleft=(pos[0],pos[1])) 
#        self.rect.x = x
#        self.rect.y = y - 12 
#        self.rect.width = width
#        self.rect.height = height - 12
#        print(self.image.get_size())


class AnimatedTile(Tile):
    def __init__(self,size,pos,path,animations,groups,status):
        super().__init__(size,pos,path,groups) 
        self.animations = animations 
        self.path = path
        self.part_path = '../graphics/particles/'
        self.part_animations = {'idle':[],'walk':[],'run':[],'jump':[]}
        self.part_status = status 
        self.import_graphics() 
        #self.import_graphics(self.part_animations,self.part_path) 
        self.status = status 
        #self.status = next(iter(animations))                       #This will give you the first item in a dicitionary
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index] 
        self.particles = self.part_animations[self.part_status][self.frame_index]
        self.window = pygame.display.get_surface()
        self.dust_frame_index = 0 
         
        self.run_dust_frame_index = 0
        self.dust_animation_speed = 0.25
        self.facing_right = True
        self.animation_timer = 0
    def import_graphics(self):
        for animation in self.animations.keys():
            #print(self.animations.keys())
            full_pth = self.path + animation
            self.animations[animation] = import_folder(full_pth)
        for parts in self.part_animations.keys():
            part_pth = self.part_path + parts 
            self.part_animations[parts]= import_folder(part_pth)
    
    def animate(self,ani_speed):
        animation = self.animations[self.status] 
        self.frame_index += ani_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
    def animate_particles(self,x,y,ani_speed):
        #print(self.status) 
        dust_particles = self.part_animations['walk']
        run_dust_particles = self.part_animations['run']
        idle_particles = self.part_animations['idle']
        self.idle_index = 0 
        #self.dust_image = dust_particles[int(self.dust_frame_index)]
        #this animation runs while the player is walking, then it stops when he stops walking.
        if self.animation_timer == 0 and self.direction.y == 0:
            if not self.direction.x >= 2 and not self.direction.x <= -2:
                if self.direction.x != 0: 
                    if self.direction.x < 0:
                        x = (x + 23)
                    self.dust_frame_index += ani_speed 
                    self.window.blit(pygame.transform.flip(self.dust_image,not self.facing_right,False),(x,y))
                    #if self.direction.x < 0:
                    #    x = (x + 62)
                    self.run_dust_frame_index = 0 
                    if self.dust_frame_index >= len(self.part_animations['walk']):
                        self.dust_frame_index = 0
                 
        #animation picks up where the previous animation ended, continues exactly where it ended, then it runs through one full cycle then it doesn't run anymore because an if statement turns off one that requires itself to run. 
        if self.animation_timer < 30: 
            if self.direction.y == 0 and self.dust_frame_index < len(self.part_animations['walk']) and self.dust_frame_index > 0:
                if self.direction.x == 0 :
                    if self.facing_right is False:
                        x = (x +23)
                    self.dust_frame_index += ani_speed 
                    self.window.blit(pygame.transform.flip(self.dust_image,not self.facing_right,False),(x,y))
                    if self.dust_frame_index >= len(self.part_animations['walk']):
                        self.animation_timer = 30 
                        self.dust_frame_index = 0
        self.idle_image = idle_particles[int(0)]
        if self.direction.y > 0:
            self.dust_frame_index = 0
        if self.direction.x !=0:
            self.animation_timer = 0
        #run animation
        if self.animation_timer >= 0 and self.animation_timer <= 30 and self.direction.x >= 2 and self.direction.y == 0:
            self.dust_frame_index = 6 
            self.window.blit(self.run_dust_image,(self.image_rect.x,self.image_rect.y-10))
            self.run_dust_frame_index += ani_speed 
            if self.run_dust_frame_index >= len(self.part_animations['run']):
                self.run_dust_frame_index = 0 
        if self.animation_timer >= 0 and self.animation_timer <= 30 and self.direction.x < -1:
            self.dust_frame_index = 6 
            self.window.blit(pygame.transform.flip(self.run_dust_image,True,False),(self.image_rect[0]+45,self.image_rect[1]-15))
            self.run_dust_frame_index += ani_speed 
            if self.run_dust_frame_index >= len(self.part_animations['run']):
                self.run_dust_frame_index = 0 
        #if self.animation_timer >= 60 and self.run_dust_frame_index >= 4:
        #    self.animation_timer = 0
        

        self.run_dust_image = run_dust_particles[int(self.run_dust_frame_index)]
        self.dust_image = dust_particles[int(self.dust_frame_index)]
       #self.idle_image = idle_particles[int(0)]
        self.image_rect = self.dust_image.get_rect(midleft = (x-25,y)) 
        if self.direction.y == 0:
            pass
#        
            ##if self.direction.x == 1: 
            #    self.animation_timer += 1 
            #    self.dust_frame_index += ani_speed
            #    self.window.blit(self.dust_image,(x,y))
       #    #     self.animation_timer +=1 
       #    #     #pygame.draw.rect(self.window,(125,125,125),,1) 
            #if self.direction.x == -1:
            #    self.animation_timer += 1 
            #    self.dust_frame_index += ani_speed
       #    #     self.window.blit(pygame.transform.flip(self.dust_image,True,False),(x+25,y))
            #if self.direction.x > 2:
            #    self.run_dust_frame_index += ani_speed
            #    self.animation_timer += 1
            #    self.window.blit((self.run_dust_image),(self.image_rect[0]-0,self.image_rect[1]))
            #if self.direction.x < -2:
            #    self.run_dust_frame_index += ani_speed
            #    self.animation_timer += 1
            #    self.window.blit(pygame.transform.flip(self.run_dust_image,True,False),(self.image_rect[0]+65,self.image_rect[1]))
            #if self.direction.x == 0 and self.frame_index < 30 :
                #self.window.blit((self.idle_image),(x,y))
                #self.animation_timer += 1
                #self.dust_frame_index +=ani_speed 
                #self.animation_timer +=1 
                #self.dust_frame_index = 0
                #self.animation_timer += 1 
            ##if self.animation_timer == 30:
            #    self.window.blit((self.idle_image),(x,y))
            #if self.animation_timer < 30:
            #    self.animation_timer += 1 
            #    self.dust_frame_index += ani_speed
                
            #if self.dust_frame_index <= len(self.part_animations['walk']) :
                #self.dust_frame_index = 0 
                #self.window.blit((self.idle_image),(x,y))
            #if self.direction.x == 0 and self.dust_frame_index <= len(self.part_animations['walk']):
            #    self.window.blit(pygame.transform.flip(self.dust_image,True,False),(x+25,y))
            #    self.dust_frame_index += ani_speed
            #    if self.dust_frame_index >= len(self.part_animations['walk']):
            #        run_dust_particles = self.part_animations['idle']
            #    
            #        self.window.blit(pygame.transform.flip(self.dust_image,True,False),(x+25,y))
                
                
                #self.run_dust_frame_index = 0
                #if self.dust_frame_index != 0:
                #self.window.blit((self.dust_image),(x,y))
            #if self.dust_frame_index >= len(self.part_animations['walk']):
            #    self.window.blit((self.idle_image),(self.image_rect.x,self.image_rect.y)) 
                #self.animation_timer +=1~~ 
                #if self.animation_timer >= 10:
                #if self.dust_frame_index >= len(self.part_animations[self.part_status]):
                #self.dust_frame_index = 4 
           #     pygame.draw.rect(self.window,(125,125,125),self.image_rect,1)
           #     #if self.dust_frame_index >= len(self.part_animations[self.part_status]):
           #     #    self.dust_image.fill((0,0,0))
           # if self.direction.x < -1:
           #     self.image_rect = self.dust_image.get_rect(midleft = (x+25,y)) 
           ##     
           #     self.window.blit(pygame.transform.flip(self.dust_image,True,False),self.image_rect)
           #     pygame.draw.rect(self.window,(125,125,125),self.image_rect,1) 
        #if self.direction.x < 0 and self.direction.y == 0:
        #    self.window.blit(pygame.transform.flip(self.dust_image,True,False),(x+20,y))
        #    pygame.draw.rect(self.window,(125,125,125),image_rect,1) 
    def resize(self,new_w,new_h):
        self.image = pygame.transform.scale(self.image,(new_w,new_h))
    def reverse_image(self):
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image,True,False)
    def set_rect(self):
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
    def update(self,shift,ani_speed):
        self.animate(ani_speed)
        self.rect.x += shift

class Flame(AnimatedTile):
    def __init__(self,size,pos,path,animations,groups):
        super().__init__(size,pos,path,animations,groups,'idle')
        pos = pos[0], pos[1] - 20 
        self.rect = self.image.get_rect(topleft=(pos))
    def update(self,shift):
        self.animate(0.085)
        self.rect.x += shift
        self.image.set_alpha(125)
