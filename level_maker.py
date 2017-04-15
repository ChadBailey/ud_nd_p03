# level_maker.py made by Chad Bailey 4-15-2017
#
# Level maker utility for making levels for game.py
#
# Purpose: Udacity intro to Programming Nanodegree, 3rd project
#
# Objective: Make a "fill in the blanks" game

import yaml

#Initializing variables
number_of_levels = 0

# Input validator variable, assume not valid until we prove that it is
valid = False

# Get number of levels to generate from the user
while valid == False:

	# Ask the user for number of levels, this must be an integer - if not, validation will not pass and they must re-try
	user_input = raw_input("Please enter the amount of levels you would like to make.\n")

	try:
		number_of_levels = int(user_input)
	except ValueError:
		print "That's not a valid number!\n"
		continue

	if number_of_levels > 20 or number_of_levels < 1:
		print "Error: You must enter a value between 1 and 20"
		continue

	print "You entered %s levels" % number_of_levels
	

	reply = raw_input("Is this correct? (Y/n)")

	if reply == "" or reply == "Yes" or reply == "Y" or reply == "y":
		valid = True
	else:
		# This could be assumed, but putting it here makes it more obvious
		valid = False

# Get input for each level - note, range extended by 1 because using 1 based range instead of 0 based range
for current_level in range(1,number_of_levels + 1):
	print "Please enter the sentence for level %s" % current_level



wait_for_input = raw_input("Press any key to continue")