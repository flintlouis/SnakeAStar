from math import sqrt
from info import GRID_WIDTH, GRID_HEIGHT, DIRECTIONS

class Node(object):
	f = 0
	g = 0
	h = 0
	parent = None
	obstacle = False

	def __init__(self, pos):
		self.pos = pos

	def heuristic(self, point, walls):
		x = abs(point[0] - self.pos[0])
		y = abs(point[1] - self.pos[1])
		if not walls:
			xoffside = abs(GRID_WIDTH - x)
			yoffside = abs(GRID_HEIGHT - y)
			if x > xoffside:
				x = xoffside
			if y > yoffside:
				y = yoffside
		self.h = x + y

	def update(self, g, end, parent, walls):
		self.parent = parent
		self.g = g
		self.heuristic(end, walls)
		self.f = self.g + self.h

	def _sumPoints(self, a, b):
		xa, ya = a
		xb, yb = b
		return (xa+xb, ya+yb)

	def _outofbounds(self, point):
		x, y = point
		if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
			return True
		return False

	def getNeighbours(self, maze, walls):
		neighbours = []
		for dir in DIRECTIONS:
			x, y = self._sumPoints(self.pos, dir)
			if not walls:
				x, y = int(x%GRID_WIDTH), int(y%GRID_HEIGHT)
				neighbours.append(maze[x][y])
			elif not self._outofbounds((x, y)):
				neighbours.append(maze[x][y])
		return neighbours

	def printInfo(self):
		print(self.pos)
		if self.parent:
			print(f"parent: {self.parent.pos}")
		else:
			print(f"parent: {self.parent}")
		print(f"f:{self.f} = g:{self.g} + h:{self.h}\n")


