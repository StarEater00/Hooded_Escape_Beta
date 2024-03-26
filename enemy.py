import pygame
from tiles import AnimatedTile
class BossEnemy(AnimatedTile):
    def __init__(self,size,pos,speed,path,groups):
        super().__init__(size,pos,'../graphics/enemy/',{'idle':[]},groups,'idle')
        self.speed = speed
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
    def reverse_speed(self):
        self.speed *= -1
    def move(self):
        self.rect.x += self.speed
    def update(self,shift):
        self.animate(0.05)
        self.resize(28,32)
        self.rect.x += shift

class Enemy(BossEnemy):
    def __init__(self,size,x,y,speed):
        super().__init__(size,x,y,'../graphics/enemy/idle')         #maybe change to variable so that i can change the different folders and have other enemies.
        self.rect.y += self.size - self.image.get_size()[1] * 2
     
