import pygame
import sys
import os
from game import Snake, Food, Settings, handle_keys
from draw import drawWalls
from info import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from pathfinding import findPath, getPath

def initPygame():
	pygame.init()
	pygame.display.set_caption('Snake')
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
	surface = pygame.Surface(screen.get_size())
	surface = surface.convert()
	return screen, surface

def loadMisc():
	bitesound = pygame.mixer.Sound('sounds/bite.wav')
	hit = pygame.mixer.Sound('sounds/hit.wav')
	music = pygame.mixer.music.load('sounds/music.mp3')
	myfont = pygame.font.SysFont("arialblack", 16)
	return bitesound, hit, myfont

def display(screen, surface, myfont, score, highscore):
	screen.blit(surface, (0,0))
	text = myfont.render(f"Score {score}", 1, WHITE)
	screen.blit(text, (10, 10))
	text = myfont.render(f"Highscore {highscore}", 1, WHITE)
	screen.blit(text, (350, 10))
	pygame.display.update()

def main():
	os.system("clear")
	print("Loading...")
	clock = pygame.time.Clock()
	screen, surface = initPygame()
	bitesound, hit, myfont = loadMisc()
	settings = Settings()
	settings.getHighscore()
	snake = Snake(3)
	apple = Food()
	os.system("clear")

	pygame.mixer.music.play(-1)
	path = None
	score = 0
	# Mainloop
	while(True):
		clock.tick(settings.fps)
		surface.fill(BLACK)
		handle_keys(settings)

		# A* Pathfinding to find apple
		if not path:
			i = 0
			openSet = []
			closedSet = []
			settings.initMaze()
			x, y = snake.head
			openSet.append(settings.maze[int(x)][int(y)])
			while len(openSet):
				path = findPath(openSet, closedSet, settings.maze, apple.position, snake, settings.walls)
				if path:
					path = getPath(path)
					break

		# If path was found move snake through path
		if path:
			snake.turn(snake.getDir(path[i]))
			i += 1
			if i == len(path):
				path = None

		# Check if snake hits obstacle
		if snake.hit(settings.walls):
			if not settings.mute:
				hit.play()
			snake.reset(3)
			apple.randomize_position()
			if score > settings.highscore:
				settings.highscore = score
				settings.saveHighscore()
			score = 0
			pygame.time.delay(1000)

		snake.move(settings.walls)

		# Check if apple gets eaten
		if snake.head == apple.position:
			if not settings.mute:
				bitesound.play()
			snake.add_body()
			while apple.position in snake.body:
				apple.randomize_position()
			score += 1

		snake.draw(surface)
		apple.draw(surface)
		if settings.walls:
			drawWalls(surface)
		display(screen, surface, myfont, score, settings.highscore)

main()
