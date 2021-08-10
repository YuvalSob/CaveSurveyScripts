# Script to group different types of walls in Topodroid output SVG file 

# Copyright (C) 2020 Yuval Soboliev
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License

# run using:
# python sub_gropup_walls.py

import sys # for args
import os # for files in directory
directory = '.'

# Delete old output files 
for filename in os.listdir(directory):
    if filename.startswith("groupped"):
        os.remove(os.path.join(filename))

# Iterating svg files
for filename in os.listdir(directory):
	if filename.endswith(".svg"):
		print (filename, 'YES')
		# Open files
		in_file = open(filename, 'r') 
		out_file = open("groupped_" + filename, 'w')

		dict = {} # Dictionary of list (key will be wall type)
		flag = 0  # Indication for parsing wall line

		# Read input file line by line
		for line in in_file:
			# True after all walls
			if line.strip() == "</g>" and flag == 1 : 
				flag = 0
				# Print new sub groups
				for key in dict.keys(): # Loop over all wall types
					out_file.write("  <g id=\"" + key + "\">\n") # Print header for sub group
					for i in dict[key]:
						out_file.write("  " + i) # Print wall lines insid sub group 
					out_file.write("  </g>\n") # Print sub group footer 
		
			# Non wall lines print
			if flag == 0 :
				out_file.write(line)
				
			# Wall lines proccess 
			else :
				key = line.split("\"")[7]
				if key in dict : 
					dict[key].append(line) # Add wall line to existing group key 
				else :
					dict[key] = [line] # Create new group key and add line 	 
					
			# indicate next lines are walls
			if line.strip() == "<g id=\"lines\">" : 
				flag = 1
			
		# Close files
		in_file.close() 
		out_file.close() 
		dict.clear()
		flag = 0
	else:
		print (filename, 'NO')

















