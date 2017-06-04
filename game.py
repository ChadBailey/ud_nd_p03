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

import yaml
import os
import base64
import re
from difflib import SequenceMatcher as SeqMat

#All default settings go here
def load_defaults(settings_dict):
	settings_dict['game_version'] 		= 1 		#Version of the game - used to validate the version of the levels file
	settings_dict['easy_lives'] 		= 7
	settings_dict['medium_lives'] 		= 5
	settings_dict['hard_lives'] 		= 3
	settings_dict['percent_correct'] 	= 0.9 		#Percent of match with blank to give the answer to the player ##NOTE: Value must be > percent_close
	settings_dict['percent_close'] 		= 0.7 		#Percent of match with blank to give player hint that they are close
	settings_dict['close_forgiveness'] 	= True 		#Should player lose a life when close to getting the answer right
	settings_dict['winner'] 			= False 	#Will be set to True to indicate the player won
	settings_dict['current_level'] 		= 1			#Always initialize current_level to begin at level 1
	settings_dict['level_complete'] 	= False
	return settings_dict

#Function for mapping user input to amount of lives available.
#settings['difficulty'] is set in function difficulty_select()
def set_lives(settings):
	if not settings['difficulty'] == 'c': #Custom difficulties already have lives set in difficulty_select function
		if settings['difficulty'] == 'e': settings['lives'] = settings['easy_lives']
		if settings['difficulty'] == 'm': settings['lives'] = settings['medium_lives']
		if settings['difficulty'] == 'h': settings['lives'] = settings['hard_lives']
	return True #Always return true, otherwise if there is an error it should cause an exception

#Returns levels dictionary if successful, otherwise returns false
def load_level(settings,levels_dict,filename):
	try:
		levels_file = open(filename, "r")
		levels_dict = yaml.load(levels_file)
		if levels_dict['settings']['version'] >= settings['game_version']: return levels_dict
		else:
			print 'Found levels file, but it is not the correct version. Please try another file.'
			x = raw_input('Press [enter] to continue')
			os.system('cls')
			return False
	except IOError:
		return False

# Allows user to select a level
# Takes settings dictionary from main function
# Since dictionary is mutable, nothing is returned back, the dictionary is simply updated
def level_select(settings,levels_dict):
	while True:
		user_input = raw_input('Please enter the name of the levels file you would like to use.\nHint: Just hit enter to load the default level\n')
		if user_input == '': user_input = 'udacity_example' 				#Sets default level if none is chosen
		levels_dict = load_level(settings,levels_dict,user_input + ".yml") 	# Attempts to load the requested level, returns True on success
		if not levels_dict:
			print "Error loading level, please try again." #Loop will continue around, causing instructions to be canceled
			continue
		else:
			os.system('cls')
			print "Successfully loaded level %s" % user_input
			settings['current_challenge'] = levels_dict['levels'][settings['current_level']]['challenge'] if not levels_dict['settings']['encoding'] else base64.b64decode(levels_dict['levels'][settings['current_level']]['challenge'])
		return levels_dict

# Allows user to select a difficulty)
def difficulty_select(settings):
	while True: #put into while loop so that the question is retried upon entering an incorrect difficulty
		user_input = raw_input("Please select your difficulty. ([e]asy, [m]edium, [h]ard, [c]ustom)\n")
		if user_input.lower() in ['easy','e','medium','m','hard','h','custom','c']:
			settings['difficulty'] = user_input.lower()[0] # only first letter stored, valid options are "e", "m", "h", and "c"
			if settings['difficulty'] == 'c':
				user_input = raw_input("Custom mode selected, how many lives do you want to have? (enter number, or type [c]ancel to re-select game difficulty)\n").lower()
				try:
					user_input = int(user_input)
					settings['lives'] = user_input
					print 'Difficulty set! You will have %s lives. Lets get started!' % str(settings['lives'])
				except ValueError: continue #Invalid input, retry
			else:
				settings['lives'] = settings['difficulty']
				set_lives(settings)
			break #Break the loop to prevent infinite loop

def validate_guess(settings,levels_dict,guess):
	result = 'incorrect' #By initializing this variable to incorrect, we are assuming an incorrect response if we don't get a "close" or "correct" result
	for answer in levels_dict['levels'][settings['current_level']]['answers']:
		answer_text = levels_dict['levels'][settings['current_level']]['answers'][answer] if not settings['encoded'] else base64.b64decode(levels_dict['levels'][settings['current_level']]['answers'][answer]) #decode if encoded
		percent_right = SeqMat(None, guess,answer_text).ratio()
		if settings['percent_close'] <= percent_right < settings['percent_correct']:
			result = 'close'
		elif percent_right >= settings['percent_correct']: #If percentage correct is greater than the required percent correct
			result = 'correct'
			settings['current_challenge'] = re.sub("_{3}(" + answer + "){1}_{3}",answer_text,settings['current_challenge'])
			del levels_dict['levels'][settings['current_level']]['answers'][answer] #Remove from dict
			if len(levels_dict['levels'][settings['current_level']]['answers']) == 0:#Level Complete!
				settings['level_complete'] = True
				settings['current_level'] += 1
			break # break loop to prevent a correct response from being overridden by a close response
	return result


def play_game(settings,levels_dict):
	os.system('cls')
	print settings['current_challenge'] + '\n'
	guess = raw_input('Lives remaining: %s\nAnswer: ' % str(settings['lives'])).lower()
	result = validate_guess(settings,levels_dict,guess)
	if result == 'correct':
		raw_input("That's Correct!\npress [enter] to continue")
		if settings['level_complete']:
			settings['level_complete'] = False
			try: settings['current_challenge'] = levels_dict['levels'][settings['current_level']]['challenge'] if not settings['encoded'] else base64.b64decode(levels_dict['levels'][settings['current_level']]['challenge'])
			except KeyError:
				settings['winner'] = True
				return
	elif result == 'close':
		raw_input("You're really close! Try again!\npress [enter] to continue")
		if not settings['close_forgiveness']: settings['lives'] -= 1 #Only reduce lives on a close guess if close_forgiveness is set
	else:
		raw_input('Not quite, Try again...\npress [enter] to continue')
		settings['lives'] -= 1

#Main function, requires no input, is ran upon execution of python file
def main():
	settings = {}
	levels_dict = {}
	os.system('cls') #clear the screen
	settings = load_defaults(settings)
	difficulty_select(settings)
	levels_dict = level_select(settings,levels_dict)
	settings['encoded'] = levels_dict['settings']['encoding']
	while settings['lives'] >= 0:
		play_game(settings,levels_dict)
		if settings['winner']:
			os.system('cls')
			play_again = raw_input('\n\n\nCongratulations!!! You are the Winrar! You win One FREE INTERNET!\n\n\nWould you like to play again? (y/[n])\n').lower()
			break
	if not settings['winner']:
		os.system('cls')
		play_again = raw_input('\n\n\nYou did your best... better luck next time :(\n\n\nWould you like to play again? (y/[n])\n').lower()
	if play_again == 'y': main()

if __name__ == '__main__': #Trigger main function if the game is not imported
	main()

