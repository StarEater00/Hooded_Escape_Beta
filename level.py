#!/usr/python3
from support import import_csv, import_cut_graphics
import pygame
from tiles import Tile, StaticTile, AnimatedTile, Flame #  Platform  #Tree
from player import Player
from enemy import Enemy,BossEnemy
from decoration import Sky
from particles import Particles
#,StaticTile,TreeTile
from settings import tile_size, screen_width
from random import randint
from pytmx.util_pygame import load_pygame 
import math

class Level():
    def __init__(self,level_data,surface):
        #print(dir(pygame.sprite))
        self.display = surface
        self.world_shift = 0 
        self.current_x = 0
        self.terrain_sprites = pygame.sprite.Group();self.tree_sprites = pygame.sprite.Group();self.firewood_sprites = pygame.sprite.Group();self.flame_sprites = pygame.sprite.Group();self.enemy_sprites = pygame.sprite.Group();self.constraint_sprites = pygame.sprite.Group();self.player = pygame.sprite.GroupSingle();self.goal = pygame.sprite.GroupSingle();self.particles = pygame.sprite.Group();self.cutscene = pygame.sprite.GroupSingle()
        
        tmx_data =  load_pygame(level_data['level_0'])
        self.sky = Sky(8) 

        self.manage_layers(tmx_data)
        self.manage_objects(tmx_data)

    def manage_layers(self,tmx_data):
        for layer in tmx_data.layers:
            if hasattr(layer,'data'):
                for x,y,surf in layer.tiles():
                    pos = (x *tile_size,y* tile_size )
                    if layer.name == 'ground':
                        StaticTile(tile_size,pos,surf,self.terrain_sprites)
                    if layer.name == 'firewood':
                        StaticTile(tile_size,pos,surf,self.firewood_sprites)
                    if layer.name == 'flame':
                        Flame(tile_size,(x*tile_size,y*tile_size) ,'../graphics/flame/',{'idle':[]},self.flame_sprites,)
    
    def manage_objects(self,tmx_data):
        object_layer = tmx_data.get_layer_by_name('objects')
        #print(object_layer)
        for obj in object_layer:
            pos = obj.x , obj.y
            if obj.type == 'vegetation':
                if obj.name == 'tree':
                    StaticTile(tile_size,pos,obj.image,self.tree_sprites)
            if obj.type == 'enemy':
                if obj.name == 'dark_hood':
                    BossEnemy(tile_size,pos,0,'../graphics/enemy/idle/',self.enemy_sprites)
            if obj.type == 'marker':
                if obj.name == 'player':
                    Player(tile_size,pos,self.player,self.display,self.create_particles,self.destroy_particles) 
                if obj.name == 'goal':
                    goal = pygame.Surface((32,32))
                    goal.fill('White')
                    StaticTile(tile_size,pos,goal,self.goal)
    
                if obj.name == 'cutscene':
                    cut_goal = pygame.Surface((32,32))
                    goal.fill('White')
                    StaticTile(tile_size,pos,cut_goal,self.cutscene)
    def scroll_x(self):
        player = self.player.sprite 
        player_x = player.rect.centerx 
        direction_x = player.direction.x

        if player_x < screen_width // 25 and not direction_x == 0 :
            if direction_x < 0: 
                self.world_shift = 3
                player.speed = 0 
            if direction_x < -1:
                self.world_shift = 6
                player.speed = 0 
            elif direction_x > 0:
                self.world_shift = 0  
                player.speed = 3
        elif player_x > screen_width - screen_width // 25 and not direction_x == 0:
            if direction_x > 0: 
                self.world_shift = -3 
                player.speed = 0
            if direction_x > 1:
                self.world_shift = -6
                player.speed = 0
            elif direction_x < 0:
                self.world_shift = 0  
                player.speed = 3
        else:
            self.world_shift = 0
            player.speed = 3
    

    def enemy_collision(self):
        for enemy in self.enemy_sprites.sprites():
            if not pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse_speed()       
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for terrain in self.terrain_sprites.sprites():
            if player.rect.colliderect(terrain.rect.x,terrain.rect.centery-6 ,terrain.rect.w,terrain.rect.h-10):
                if not player.on_ground: 
                    if player.direction.x < 0 and not player.on_ceiling:
                        player.rect.left = terrain.rect.right  
                        player.on_left = True 
                        self.current_x = player.rect.left
                    elif player.direction.x > 0 and not player.on_ceiling:
                        player.rect.right = terrain.rect.left 
                        player.on_right = True 
                        self.current_x = player.rect.right
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >=0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x<=0):
                player.on_right = False
            if player.rect.colliderect(terrain.rect.x,terrain.rect.centery,terrain.rect.w,terrain.rect.h-10):
                 if player.on_ground: 
                    if player.direction.x < 0:
                        player.rect.left = terrain.rect.right 
                        player.on_left = True
                    elif player.direction.x > 0:
                        player.rect.right = terrain.rect.left 
                        player.on_right = True
    def vertical_collision(self): 
        player = self.player.sprite
        #pygame.draw.rect(self.display,'white',player.rect,2)
        player.apply_gravity()
        for terrain in self.terrain_sprites.sprites():
            #pygame.draw.rect(self.display,'red',(terrain.rect.x,terrain.rect.centery-6,terrain.rect.w,1) )
            #pygame.draw.rect(self.display,'red',(terrain.rect.x,terrain.rect.bottom,terrain.rect.w,1) )
            if player.rect.colliderect(terrain.rect.x,terrain.rect.centery-6,terrain.rect.w,1):
                if player.direction.y > 0:
                    player.direction.y = 0
                    player.rect.bottom = terrain.rect.top 
                    player.rect = player.image.get_rect(midtop = (player.rect.center))
                    player.on_ground = True
            if player.rect.colliderect(terrain.rect.x,terrain.rect.bottom,terrain.rect.w,1):
                

                if player.direction.y < 0:
                    player.rect.top = (terrain.rect.bottom)                           #i think he goes through the bottom because their is nothing to stop him from the force of him jumping up: he is going past where he is allowed.  
                    player.direction.y = 0 
                    #player.rect = player.image.get_rect(topleft = (player.rect.topleft))
                    player.on_ceiling = True
                    #player.apply_gravity() 
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
            
        elif player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
   
    def create_particles(self):
        player = self.player.sprite
        particles = Particles((tile_size),(player.rect.bottomleft[0],player.rect.bottomleft[1]),self.particles)
        return particles
    def destroy_particles(self):
        for particle in self.particles:
            particle.kill()
                #sprite.kill() 
    def create_smoke(self):
        for fire in self.flame_sprites.sprites():
            particles = Particles((tile_size),(fire.rect.topleft[0],fire.rect.topleft[1]),self.particles) 
    def draw_enemy(self):
        player = self.player.sprite
         
        self.enemy_sprites.draw(self.display)
        self.enemy_sprites.update(self.world_shift)
        for enemy in self.enemy_sprites.sprites():
            enemy.image.set_alpha(0)
            print(int(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y)))
            
            if (int(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y)) < 100):
                enemy.image.set_alpha(205) 
             
            #enemy.image.set_alpha(0) 
        #print('player ' + str(player.rect.x)) 
        #for enemy in self.firewood_sprites.sprites():
            #print(int(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y))) 
            #if (int(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y)) < 100):
           # if player.rect.x > enemy.rect.x: 
           #     self.enemy_sprites.draw(self.display)
           #     self.enemy_sprites.update(0)
            #if int(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y)) < 400:
            #    print(math.hypot(player.rect.x-enemy.rect.x,player.rect.y-enemy.rect.y)< 300)
                #self.enemy_sprites.update(self.world_shift)
    def draw_update(self):
        sprites = [self.sky,self.tree_sprites,self.terrain_sprites,self.particles,self.player,self.firewood_sprites,self.flame_sprites,self.constraint_sprites,self.goal,self.cutscene]
        for i in sprites:
            i.draw(self.display)
            if i in [self.sky]:
                pass 
            else: i.update(self.world_shift)
            
    def run(self):
        #level 
        #self.draw_particles()
        self.draw_update() 
        self.draw_enemy() 
        self.scroll_x()
        #self.create_particles()
        #player 
        self.enemy_collision()
        self.vertical_collision()
        self.horizontal_movement_collision()
        #self.create_smoke()
