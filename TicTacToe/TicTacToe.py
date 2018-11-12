import time
import random

empty = 0
circle = 1
cross = 2

def buildGrid(val):
	gridList = []
	for rowNum in xrange(0, 3):
		rowList = []
		row = (val >> (rowNum * 6)) & 0x3F
		for cellNum in xrange(0, 3):
			cell = (row >> (cellNum * 2)) & 3
			rowList.append(cell)
		gridList.append(rowList)
	return gridList

def gridDraw(gridList):
	symbols = ['.', 'O', 'X']
	textDrawing = ''
	for row in gridList:
		for cell in row:
			textDrawing += symbols[cell]
		textDrawing += '\n'
	print(textDrawing)

def victoryCode(circles, crosses):
	if circles == 3 and crosses == 3:
		return 3		# invalid disposition
	elif crosses == 3:
		return cross	# crosses win
	elif circles == 3:
		return circle	# circles win
	else:
		return 0		# no win

def isVictory(val):
	grid = buildGrid(val)

	# test rows
	for column in xrange(0, 3):
		circles = 0
		crosses = 0
		for row in xrange(0, 3):
			cell = grid[column][row]
			if cell == cross:
				crosses += 1
			elif cell == circle:
				circles += 1
		if circles == 3 or crosses == 3:
			return victoryCode(circles, crosses)

	# test columns
	for row in xrange(0, 3):
		circles = 0
		crosses = 0
		for column in xrange(0, 3):
			cell = grid[column][row]
			if cell == cross:
				crosses += 1
			elif cell == circle:
				circles += 1
		if circles == 3 or crosses == 3:
			return victoryCode(circles, crosses)

	# test diagonals: left to right
	circles = 0
	crosses = 0
	for cellNum in xrange(0, 3):
		cell = grid[cellNum][cellNum]
		if cell == cross:
				crosses += 1
		elif cell == circle:
				circles += 1
	if circles == 3 or crosses == 3:
		return victoryCode(circles, crosses)

	# test diagonals: right to left
	# same logic as the check before but reflecting the grid top to bottom
	circles = 0
	crosses = 0
	for cellNum in xrange(0, 3):
		cell = grid[::-1][cellNum][cellNum]
		if cell == cross:
				crosses += 1
		elif cell == circle:
				circles += 1
	if circles == 3 or crosses == 3:
		return victoryCode(circles, crosses)
	return victoryCode(circles, crosses)

def isValidMove(disp, move):
	if ((disp >> (move * 2)) & 3) == 0:
		return True
	return False

def elaborateMove(disp, move, symbol):
	return (disp + (symbol << (move * 2)))

def buildMoves(disp, symbol):
	possibleMoves = []
	moveFitness = []
	print 'debug'
	for move in xrange(0, 9):
		if isValidMove(disp, move):
			possibleMoves.append(move)
	for move in possibleMoves:
		newDisp = elaborateMove(disp, move, symbol)
		if isVictory(newDisp) == symbol:
			moveFitness.append((move, 1))
		elif isVictory(newDisp) == 0:
			print 'No diff'
			moveFitness.append((move, 0))
		else:
			print 'Gonna lose'
			moveFitness.append((move, -1))

	bestFitness = -1
	bestMoves = []
	for move in moveFitness:
		if move[1] > bestFitness:
			bestFitness = move[1]
			bestMoves = []
		if move[1] == bestFitness:
			bestMoves.append(move[0])
	return random.choice(bestMoves)

seed = int(time.time())
seed = 1532599575
print('Match seed: %d' % seed)
random.seed(seed)
turns = 0
currDisp = 0
while turns < 9:
	symbol = cross if turns % 2 == 0 else circle

	# crosses run with lesser intelligence
	if symbol == cross:
		move = buildMoves(currDisp, symbol)
	# circles go random. Just for testing purposes
	else:
		move = random.randint(0, 8)
		while isValidMove(currDisp, move) != True:
			move = random.randint(0, 8)
	currDisp = elaborateMove(currDisp, move, symbol)
	gridDraw(buildGrid(currDisp))
	if isVictory(currDisp) == circle:
		print('Circle wins in %d turns' % (turns + 1))
		break
	elif isVictory(currDisp) == cross:
		print('Cross wins in %d turns' % (turns + 1))
		break
	turns += 1
if turns == 9:
	print('No win')
