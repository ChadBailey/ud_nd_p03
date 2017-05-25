#

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

import yaml
import os
import base64

# Returns true if valid, false if invalid
# Also prints out helpful text if a level was loaded, but not of the correct version - then returns false
def level_validator(filename):
	if os.path.isfile(filename):
		try:
			try:
				levels_file = open(filename, "r")
			except IOError:
				return False
			levels_dict = yaml.load(levels_file)
			try:
				if levels_dict['settings']['version'] == 1: return True
			except KeyError: pass
			print 'Found levels file, but it is not the correct version. Please try another file.'
			x = raw_input('Press [enter] to continue')
			os.system('cls')
			return False

		except IOError:
			return False
	return False

# load_level returns true on success, false on failure
def load_level(levels_dict,filename):
	if level_validator(filename):
		# otherwise, try and open the file for writing
		try:
			levels_file = open(filename, "r")
		except IOError:
			return False

		levels_dict = yaml.load(levels_file)
#		if levels_dict['settings']['encoding']:

#		print levels_dict

		return levels_dict

	else:
		return False

# Allows user to select a level
# Takes settings dictionary from main function
# Since dictionary is mutable, nothing is returned back, the dictionary is simply updated
def level_select(levels_dict):
	#Level select
	while True:
		user_input = raw_input('Please enter the name of the levels file you would like to use.\nHint: Just hit enter to load the default level\n')

		#Sets default level if none is chosen
		if user_input == '': user_input = 'udacity_example'

		# Attempts to load the requested level, returns True on success
		levels_dict = load_level(levels_dict,user_input + ".yml")
		if not levels_dict:
			print "Error loading level, please try again."
		else:
			os.system('cls')
			print "Successfully loaded level %s" % user_input
			return levels_dict

# Allows user to select a difficulty)
def difficulty_select(settings):
	while True:
		user_input = raw_input("Please select your difficulty. ([e]asy, [m]edium, [h]ard, [c]ustom)\n")

		if user_input.lower() in ['easy','e','medium','m','hard','h','custom','c']:
			# only first letter stored, valid options are "e", "m", "h", and "c"
			settings['difficulty'] = user_input.lower()[0]
			if settings['difficulty'] == 'c':
				user_input = raw_input("Custom mode selected, how many lives do you want to have? (enter number, or type [c]ancel to re-select game difficulty)\n")
				try:
					user_input = int(user_input)
					settings['lives'] = user_input
				except ValueError:
					continue

			elif settings['difficulty'] == 'e': settings['lives'] = 10
			elif settings['difficulty'] == 'm': settings['lives'] = 5
			elif settings['difficulty'] == 'h': settings['lives'] = 3

			os.system('cls')
			print 'Difficulty set! You will have %s lives. Lets get started!' % str(settings['lives'])
			break

def play_level(settings,level):
	print settings
	print 'Challenge: %s' % level['1_challenge']
	print 'Answers: %s' % level['2_answers']
	print 'Lives Left: %s' % str(settings['lives'])
	user_input = raw_input("'[S]ave a life, [L]ose a life, [W]in?'\n")
	user_input = user_input.lower()
	if user_input != 's' and user_input != 'w':
		os.system('cls')
		print 'Life depleting.....'
		settings['lives'] -= 1
		return
	elif user_input == 'w':
		settings['winner'] = True
		return
	else:
		print 'Save successful!'
		return
	

def main():

	os.system('cls') #clear the screen

	#Initialize and populate settings dictionary
	settings = {}
	settings['winner'] = False # Will be set to True to indicate they have won!
	settings['win_level'] = False
	levels_dict = {}

	difficulty_select(settings)

	levels_dict = level_select(levels_dict)

	settings['encoded'] = levels_dict['settings']['encoding']

	while settings['lives'] >= 0:

		for key in levels_dict:
			if "level_" in key:
				play_level(settings,levels_dict[key])

		if settings['winner']:
			os.system('cls')
			print '\n\n\nCongratulations!!! You are the Winrar! You win One FREE INTERNET!\n\n\n'
			break

	if not settings['winner']:
		os.system('cls')
		print '\n\n\nSomething very unfortunate has happened... better luck next time :(\n\n\n'

if __name__ == '__main__':
	main()

