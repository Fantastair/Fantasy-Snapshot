import pygame
import pygame.freetype

from pygame.locals import *

default_rect = pygame.Rect(0, 0, 0, 0)
default_font = pygame.freetype.Font(None)
default_font.origin = True

del pygame