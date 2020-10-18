from info import GRIDSIZE, SCREEN_HEIGHT, SCREEN_WIDTH, GRAY
import pygame

def drawRect(surface, point, colour):
	x, y = point
	r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
	pygame.draw.rect(surface, colour, r)

def drawWalls(surface):
	r = pygame.Rect((0,0), (SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.draw.rect(surface, GRAY, r, 5)