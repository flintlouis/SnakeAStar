import random
import pygame
from info import START_POS, RIGHT, GRID_WIDTH, GRID_HEIGHT, HEAD, GREEN, GRIDSIZE
from node import Node
from draw import drawRect
import sys

class Snake(object):
	def __init__(self, len):
		self.reset(len)

	def add_body(self):
		self.body.append(self.body[-1])

	def getOpDir(self, dir):
		return (dir[0]*-1, dir[1]*-1)

	def turn(self, dir):
		if self.getOpDir(dir) == self.direction or not self.moved:
			return
		self.direction = dir
		self.moved = False

	def getDir(self, pos):
		return pos[0]-self.head[0], pos[1]-self.head[1]

	def move(self, walls):
		newhead = self.getNewHead(walls)
		self.body.insert(0, newhead)
		self.body.pop()
		self.head = newhead
		self.moved = True

	def reset(self, len):
		self.moved = True
		self.body = [START_POS]
		self.direction = RIGHT
		for i in range(len-1):
			self.add_body()
		self.head = self.body[0]

	def draw(self, surface):
		drawRect(surface, self.head, HEAD)
		for pos in self.body[1:]:
			drawRect(surface, pos, GREEN)
	
	def getNewHead(self, walls):
		x, y = self.direction
		headx, heady = self.head
		if walls:
			return (headx+x, heady+y)
		return (int((x+headx)%GRID_WIDTH), int((y+heady)%GRID_HEIGHT))

	def wallHit(self, pos):
		x, y = pos
		return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

	def hit(self, walls):
		pos = self.getNewHead(walls)
		if pos in self.body[:-1] or self.wallHit(pos):
			return True
		return False

	# def zigzag(self, walls):
	# 	if not self.hit(walls):
	# 		return
		


class Food(object):
	def __init__(self):
		self.colour = (150, 20, 20)
		self.randomize_position()

	def randomize_position(self):
		self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

	def draw(self, surface):
		pos = (self.position[0]*GRIDSIZE, self.position[1]*GRIDSIZE)
		r = pygame.Rect(pos, (GRIDSIZE, GRIDSIZE))
		pygame.draw.rect(surface, self.colour, r)

class Settings:
	mute = False
	fps = 25
	highscore = 0
	walls = True

	def initMaze(self):
		self.maze = [[Node((x,y)) for y in range(int(GRID_HEIGHT))] for x in range(int(GRID_WIDTH))]

	def getHighscore(self):
		try:
			with open('.highscore', 'r') as f:
				self.highscore =  int(f.read())
		except:
				self.highscore =  0

	def saveHighscore(self):
		with open('.highscore', 'w') as f:
			f.write(str(self.highscore))

def handle_keys(settings):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == ord('m'):
				if settings.mute:
					settings.mute = False
					pygame.mixer.music.unpause()
				else:
					settings.mute = True
					pygame.mixer.music.pause()
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.key == pygame.K_UP and settings.fps < 100:
				settings.fps += 5
			elif event.key == pygame.K_DOWN and settings.fps > 10:
				settings.fps -= 5
			elif event.key == pygame.K_SPACE:
				settings.walls = False if settings.walls else True