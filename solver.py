# Shaayan Syed

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


#---------- HELPERS ----------
# Converts boolean line to a rule represented as an array of integers,
# which can then be compared to the existing rules/constraints
def convertToRule(line):
	rules = []
	count = 0
	for digit in line:
		if digit:
			count += 1
		elif count > 0:
			rules.append(count)
			count = 0
	if count > 0:
		rules.append(count)

	if len(rules) == 0:
		rules.append(0)

	return rules

# Checks whether the converted line is valid wrt the applicable rules.
def checkValid(line, rule, isLast):
	# First check the case where this line is completed
	if isLast:
		return line == rule

	# Return False if the number of marked elements is already greater than the max
	if sum(line) > sum(rule):
		return False

	# Check if any of the current adjoined, marked elements break the rules
	limit = min(len(line), len(rule))
	for i in range(0, limit):
		if line[i] > rule[i]:
			return False

	return True


#---------- INPUT ----------
input = open("test1.txt", "r")
maxIters = 1000

# Get the size of the board
size = input.readline().rstrip("\n").split(" ")
height = int(size[0])
width = int(size[1])
sums = {}

# Get the rules for the rows
rowRules = []
for count in range(height):
	rules = [int(i) for i in input.readline().rstrip("\n").split(" ")]
	rowRules.append(rules)
	sums["r" + str(count)] = sum(rules)

# Get the rules for the columns
colRules = []
for count in range(width):
	rules = [int(i) for i in input.readline().rstrip("\n").split(" ")]
	colRules.append(rules)
	sums["c" + str(count)] = sum(rules)

# Initialize the board
board = np.zeros((height, width), dtype = bool)


#---------- SOLVE ----------
# Recursive backtracking function that solves the board using brute force
def solveBoard(row, col):
	# Base case
	if row == height:
		return True

	# Find the next element to check,
	nextRow = row
	nextCol = col + 1
	if nextCol == width:
		nextRow = row + 1
		nextCol = 0

	# Check if this is the last element in the row or column
	isLastRow = False
	isLastCol = False
	if row + 1 == height:
		isLastRow = True
	if col + 1 == width:
		isLastCol = True

	# Mark the current element
	board[row][col] = True
	currRow = convertToRule(board[row, :])
	currCol = convertToRule(board[:, col])

	# Check if the move turns out to be valid
	if checkValid(currRow, rowRules[row], isLastCol) \
		and checkValid(currCol, colRules[col], isLastRow) \
		and solveBoard(nextRow, nextCol):
		return True

	# If the previous action is against the rules, remove the mark and try again
	board[row][col] = False
	currRow = convertToRule(board[row, :])
	currCol = convertToRule(board[:, col])
	if checkValid(currRow, rowRules[row], isLastCol) \
		and checkValid(currCol, colRules[col], isLastRow) \
		and solveBoard(nextRow, nextCol):
		return True

	return False

# Solve and display the board
solveBoard(0, 0)
board = 1 - (board * 1)

grid = colors.ListedColormap(['black', 'white'])
norm = colors.BoundaryNorm([0, 1], grid.N)
fig, ax = plt.subplots()
ax.imshow(board, cmap=grid, norm=norm)
ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
plt.show()
