import time
import random

empty = 0
circle = 1
cross = 2

def isValidVal(val):
	for times in xrange(0, 18, 2):
		cellContent = (val >> times) & 3
		if cellContent not in (empty, circle, cross):
			return False
	return True

def isRealDisp(val):
	circleNum = 0
	crossNum = 0
	for times in xrange(0, 18, 2):
		cellContent = (val >> times) & 3
		if cellContent in (circle, cross):
			if cellContent == circle:
				circleNum += 1
			else:
				crossNum += 1
	if (crossNum - circleNum) in (0, 1):
		return True
	else:
		return False

def countMoves(val):
	moves = 0
	for times in xrange(0, 18, 2):
		cellContent = (val >> times) & 3
		if cellContent in (circle, cross):
			moves += 1
	return moves

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

# yup, essentially dead code
# let's not remove it for the time being
def victorySelfTest():
	gridDraw(buildGrid(movesDict[5][0]))
	print isVictory(movesDict[5][0])
	gridDraw(buildGrid(movesDict[5][57]))
	print isVictory(movesDict[5][57])

	gridDraw(buildGrid(movesDict[5][369]))
	print isVictory(movesDict[5][369])
	gridDraw(buildGrid(movesDict[5][902]))
	print isVictory(movesDict[5][902])

	gridDraw(buildGrid(movesDict[5][728]))
	print isVictory(movesDict[5][728])
	gridDraw(buildGrid(movesDict[5][858]))
	print isVictory(movesDict[5][858])

	gridDraw(buildGrid(movesDict[5][453]))
	print isVictory(movesDict[5][453])
	gridDraw(buildGrid(movesDict[5][654]))
	print isVictory(movesDict[5][654])

def isValidMove(disp, move):
	if ((disp >> (move * 2)) & 3) == 0:
		return True
	return False

def elaborateMove(disp, move, symbol):
	return (disp + (symbol << (move * 2)))

def buildMoves(disp, symbol):
	possibleMoves = []
	moveFitness = []
	for move in xrange(0, 9):
		if isValidMove(disp, move):
			possibleMoves.append(move)
	for move in possibleMoves:
		newDisp = elaborateMove(disp, move, symbol)
		if isVictory(newDisp) == symbol:
			moveFitness.append((move, 1))
		elif isVictory(newDisp) == 0:
			moveFitness.append((move, 0))
		else:
			moveFitness.append((move, -1))

	bestFitness = -1
	bestMoves = []
	for move in moveFitness:
		if move[1] > bestFitness:
			bestFitness = move[1]
			bestMoves = []
		if move[1] == bestFitness:
			bestMoves.append(move[0])
	print bestMoves
	return random.choice(bestMoves)

database = []
for disp in xrange(0, 0x3FFFF):
	if isValidVal(disp) == True:
		if isRealDisp(disp) == True:
			database.append(disp)
print('Database initialized')
print('# of elements: %d' % len(database))

movesDict = {}
for disp in database:
	moves = countMoves(disp)
	if moves not in movesDict:
		movesDict[moves] = []
	movesDict[moves].append(disp)
for numMoves in movesDict:
	print('# dispositions at move %d: %d' % (numMoves, len(movesDict[numMoves])))

random.seed(int(time.time()))
print int(time.time())
turns = 0
currDisp = movesDict[turns][0]
while turns < 9:
	symbol = cross if turns % 2 == 0 else circle

	# crosses run with minor intelligence
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
