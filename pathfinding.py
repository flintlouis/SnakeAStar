def getPath(path):
	newPath = []
	while path.parent:
		newPath.append(path.pos)
		path = path.parent
	newPath.reverse()
	return newPath

def bodyHit(neighbour, snake, g):
	if neighbour.pos in snake.body[:-g]:
		return True
	return False

def findPath(openSet, closedSet, maze, end, snake, walls):
	current = openSet[0]
	# Find node with lowest f
	for node in openSet:
		if node.f < current.f:
			current = node
	# Remove from openSet and add to closedSet
	openSet.remove(current)
	closedSet.append(current)
	# Stop if end node has been found
	if current.pos == end:
		return current
	# check all neigbouring nodes to see which to add to openSet
	for neighbour in current.getNeighbours(maze, walls):
		# Make sure node wasn't already visited
		g = current.g + 1
		if neighbour in closedSet or bodyHit(neighbour, snake, g):
			continue
		if neighbour not in openSet:
			neighbour.update(g, end, current, walls)
			openSet.append(neighbour)
		else:
			# Update node in openSet because better g was found
			if g < node.g:
				neighbour.update(g, end, current, walls)
	return None
