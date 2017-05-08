# level_maker.py made by Chad Bailey 4-15-2017
#
# Level maker utility for making levels for game.py
#
# Purpose: Udacity intro to Programming Nanodegree, 3rd project
#
# Objective: This is a simple level maker utility to create levels to be used by the application.
#
# Notice: This level maker is a complete bonus and not a requirement of the project. Therefore 
# certain criteria have not been met. For example, I have not abstracted
# out anything into functions. While I normally do this for everything I design, this particular
# application I did not feel it made sense to do so due to the way it flowed.


import os
import yaml
import re
import base64

#Initializing variables
number_of_levels = 0

# Input validator variable, assume not valid until we prove that it is
valid = False
levels_file = False
levels_dict = {}
levels_dict['settings'] = {}

# Get number of levels to generate from the user
while not valid:

	# caution to those who strongly type: falsy operator
	if not levels_file:

		levels_filename = raw_input("Please enter the name of this levels file\n")

		if os.path.isfile(levels_filename + ".yml"):
			user_response = raw_input("Warning: A levels file with that name already exists, would you like to continue, overwriting the contents? (Y/n)")
			if user_response != "" and user_response.lower() != "yes" and user_response.lower() != "y":
				# If user does not respond with "[blank]/Yes/yes/Y/y", then go to next iteration of while loop and ask for the filename again
				continue

		# otherwise, try and open the file for writing
		try:
			levels_file = open("%s.yml" % levels_filename, "w")
		except IOError:
			print "Error, invalid filename or permissions."
			continue



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

	# test lower-cased version of response to enforce case insensitivity
	if reply == "" or reply.lower() == "yes" or reply.lower() == "y":
		valid = True
	else:
		# This could be assumed, but putting it here makes it more obvious
		continue


# Note: I fully understand that encoding into and out of base64 is not a proper security measure
reply = raw_input("Do you want to encode this file to prevent casual cheating? (Y/n)")
if reply == "" or reply.lower() == "yes" or reply.lower() == "y":
	enable_encoding = True
	levels_dict['settings']['encoding'] = True
else:
	enable_encoding = False
	levels_dict['settings']['encoding'] = False

#clear screen

# Get input for each level - note, range extended by 1 because using 1 based range instead of 0 based range

for current_level in range(1,number_of_levels + 1):

	# Re-setting and re-using valid variable
	valid = False

	while not valid:

		#len(re.search("__{1}(\d+)__{1}",s).groups())
		level_sentence = raw_input("Please enter the challenge sentence for level %s:\n" % current_level)
		#this will be the solution once the user 
		solution = level_sentence
		replacements_list = list(set(re.findall("__{1}(\d+){1}__{1}",level_sentence)))
		number_of_blanks = len(replacements_list)

		if number_of_blanks > 0:
			#print "Level %s Saved successfully." % current_level

			# Create sub-dict for this level
			levels_dict["level_" + str(current_level)] = {}

			# Create sub-dict for the answers
			levels_dict["level_" + str(current_level)]['2_answers'] = {}

			# Add sentence to levels dictionary as key '1_challenge'
			levels_dict["level_" + str(current_level)]['1_challenge'] = level_sentence if not enable_encoding else base64.b64encode(level_sentence)

			for current_blank in range(0,number_of_blanks):


				blank_answer = raw_input("Please enter the answer for: __%s__\n" % replacements_list[current_blank])

				# The solution isn't actually needed for anything, but is tracked so that it can be played back to the end user
				# to ensure that the solution says what they ended it to.
				solution = re.sub("__{1}(" + replacements_list[current_blank] + "){1}__{1}",blank_answer,solution)

				# Add answer to levels dictionary
				levels_dict["level_" + str(current_level)]['2_answers'][replacements_list[current_blank]] = blank_answer if not enable_encoding else base64.b64encode(blank_answer)

			print "Solution stored as:\n%s\n\n" % solution

			valid = True
		else:
			print "Error, please enter a string containing replacements in the format __(number)__."
			continue


# Now that we've built the dictionary, output to a yaml formatted file.
# disable default_flow_style because we like our configs to be pretty,
# lacking things like curly braces (eww)
yaml.dump(levels_dict,levels_file,default_flow_style=False)

wait_for_input = raw_input("%s.yml generated successfully, press any key to continue" % levels_filename)