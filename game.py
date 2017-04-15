# game.py made by Chad Bailey 4-15-2017
#
# Purpose: Udacity intro to Programming Nanodegree, 3rd project
#
# Objective: Make a "fill in the blanks" game
#

### Udacity Criteria ###
#
# Mandatory Criteria:
#
# 	Game Basics
# 		Game has 3 or more levels and each level contains 4 or more blanks to fill in
#
# 	Beginning the Game
# 		Immediately after running the program, user is prompted to select a difficulty level from easy / medium / hard
# 		Once a level is selected, game displays a fill-in-the-blank and a prompt to fill in the first blank.
#
# 	Game Play
# 		When player guesses correctly, new prompt shows with correct answer in the previous blank and a new prompt for the next blank
# 		When player guesses incorrectly, they are prompted to try again
#
# Code Review Criteria:
#
# 	Use of Variables
# 		Code uses variables to avoid magic numbers
# 		Each variable name reflects the purpose of the value stored in it
# 		Once initiated, the purpose of each variable is maintained throughout the program
# 		No variables override Python built-in values (for example, def)
#
# 	Use of Functions
# 		Functions are used as tools to automate tasks which are likely to be repeated
# 		Functions produce the appropriate output (typically with a return statement) from the appropriate input (function parameters)
# 		No functions are longer than 18 lines of code (does not include blank lines, comments, or function definitions)
#
# 	Appropriate Use of Data
# 		The appropriate data types are used consistently (strings for text, lists for ordered data, nested lists as appropriate)
#
# 	Appropriate Use of Coding Techniques
# 		Student demonstrates coding techniques like branching and loops appropriately (i.e. to loop through a list, for element in list:; or to test whether something is in a list, if name in list_names:)
# 
# 	Comments / Documentation
# 		Each function includes a comment which explains the intended behavior, inputs, and outputs (if applicable)
#
# 	Suggestions to Make Your Project Stand Out!
# 		Let the user decide how many wrong guesses they can make before they lose
#

### My Bonus Criteria ###
# Abstract levels into a configuration file
# Make configuration file not obvious to read/modify to discourage cheating
# Make ascii graphic to represent tries/lives like hangman
# Make cool ascii ending congratulations

