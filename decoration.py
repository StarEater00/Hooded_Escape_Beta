from settings import verticle_height,tile_size,screen_width
import pygame

class Sky:
    def __init__(self,horizon):
        self.top = pygame.image.load('../graphics/decoration/dark_background.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/middleground.png').convert()
        self.horizon = horizon
        x,y = self.top.get_size()
        #print(x,y)
        self.top = pygame.transform.scale(self.top,(x + 220 ,y ))
        
        #self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))

    def draw(self,surface):
        surface.blit(self.top,(0,0))
