#!/usr/bin/python3
import csv
from settings import *
import pygame
from os import walk

def import_csv(path):
    map_layout = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for line in reader:
            map_layout.append(list(line))
        return map_layout

def import_cut_graphics(path):
    cut_graphics_list = []
    tile_set_image = pygame.image.load(path).convert_alpha()
    x_num_tiles = (tile_set_image.get_size()[0] / tile_size)
    y_num_tiles = (tile_set_image.get_size()[1] / tile_size)
    for y in range(int(y_num_tiles)):
        for x in range(int(x_num_tiles)):
            y_coor = y * tile_size
            x_coor = x * tile_size
            new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
            new_surf.blit(tile_set_image,(0,0),(pygame.Rect((x_coor,y_coor,tile_size,tile_size))))
            cut_graphics_list.append(new_surf)
    return cut_graphics_list

def import_folder(path):
    surface_list = []
    for _,__,image_files in walk(path):
        #print(image_files)
        for image in sorted(image_files):
            #print(image)
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append((image_surf))
    return surface_list
