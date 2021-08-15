# Script to create vertical and horizontal scales for cave maps

# Copyright (C) 2020 Yuval Soboliev
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License

# run using:
# python "rulers.py" <y_top> <y_bottom> <depth>

import sys
import svgwrite # for creating SVG file. Install (on Windows) using "python -m pip install svgwrite"
from svgwrite import cm, mm   


print ("<y_top> <y_bottom> <depth>")

########################################################################
#################### User defined parameters ###########################
######################################################################## 

# Vertical scale parameters
intervals_arr = [1, 5, 10] # The jumps in meters between ticks
tick_len_arr = [5, 10, 20] # The length of the tick
font_size_arr = [0, 0, 10, 14] # The font size of the numbers (last index is for the total depth)
text_h_align_arr = [0, 5, 10] # The space between tick and number
text_v_align_arr = [3, 3, 3] # Aligns the label to the tick
direction = 1 # left or right ruler ** allowed values are '1' or '-1' **

# Horizontal scale parameters
base_unit = 2 # Value in meters of small rectangle
base_units_num = 5 # The number of small rectangles 
hight = 3 # The hight of one row in the horizontal scale
h_font_size = 6 # The label font size 

#################### Don't edit below here ###########################
######################################################################


scale = 841/297 # internal parameter 
ruler_top = float(sys.argv[1]) * scale
ruler_bottom = float(sys.argv[2]) * scale
depth = float(sys.argv[3])

# Updates horizontal alignment of the text to include tick length
for i in range(len(text_h_align_arr)):
	text_h_align_arr[i] += tick_len_arr[i]

# Updates vertical alignment of the text to be relative to font size
for i in range(len(text_v_align_arr)):
	text_v_align_arr[i] = font_size_arr[i]/text_v_align_arr[i]
	
# Create SVG file for output
file_name = 'vertical_ruler_' + str(depth) + '.svg'
dwg = svgwrite.Drawing(file_name, profile='tiny') 

# Draws vertical ruler
# --------------------

ruler_x = 20
interval = (ruler_bottom - ruler_top)/depth 

# Prints vertical line
dwg.add(dwg.line((ruler_x, ruler_top), (ruler_x, ruler_bottom), stroke='black'))


y = ruler_top
ruler_label = 0

# Function to print tick and its label
def print_tick(index):
	# Print tick
	dwg.add(dwg.line((ruler_x, y), (ruler_x - direction * tick_len_arr[index], y), stroke='black'))
	# Print label (if font size is not '0')
	if font_size_arr[index] > 0: 
		dwg.add(dwg.text(str(ruler_label), insert=(ruler_x - direction * text_h_align_arr[index], y + text_v_align_arr[index]), font_size=str(font_size_arr[index]) + 'px',  fill='black', text_anchor='middle'))

# Loop to print all ticks 
while (y + 1) < ruler_bottom:
	if   (ruler_label % intervals_arr[2]) == 0: print_tick(2)
	elif (ruler_label % intervals_arr[1]) == 0: print_tick(1)
	elif (ruler_label % intervals_arr[0]) == 0: print_tick(0)
	y += interval
	ruler_label += 1

# Prints total depth of the cave
dwg.add(dwg.line((ruler_x + tick_len_arr[2]/2, ruler_bottom), (ruler_x - tick_len_arr[2]/2, ruler_bottom), stroke='black'))
dwg.add(dwg.text(str(round(depth,2))+"m", insert=(ruler_x, ruler_bottom + font_size_arr[3]), font_size=str(font_size_arr[3]) + 'px',  fill='black', text_anchor='middle'))

dwg.save()
  
# Draw Horizontal ruler
# ----------------------
file_name = 'horizontal_ruler_' + str(depth) + '.svg'
dwg = svgwrite.Drawing(file_name, profile='tiny')

ruler_x = 50
ruler_y = 50
base_unit_size = base_unit * interval # The size of small rectangles 
width = base_unit_size
color = ['black', 'white']

# Loop to print rectangles and labels 
i = 0
while i < (base_units_num + 1):	
	# Print the label
	dwg.add(dwg.text(str(i*base_unit), insert=(ruler_x + i * width, ruler_y - 2), font_size=str(h_font_size) + 'px',  fill='black', text_anchor='middle'))
	if i == base_units_num: width = base_unit_size*base_units_num # last rectangle is wider
	
	# Prints 2 rows of rectangles
	dwg.add(dwg.rect(insert=(ruler_x + i * base_unit_size, ruler_y), size=(width, hight), fill=color[i%2], stroke_width=0))
	dwg.add(dwg.rect(insert=(ruler_x + i * base_unit_size, ruler_y + hight), size=(width, hight), fill=color[(i+1)%2], stroke_width=0))
	i += 1

# Prints outer rectangle
dwg.add(dwg.rect(insert=(ruler_x, ruler_y), size=(2*(base_unit_size * base_units_num), 2* hight), stroke='black', fill='none', stroke_width=0.5))
# Prints last label 
dwg.add(dwg.text(str(2*base_unit*base_units_num) + 'm', insert=(ruler_x + 2*(base_unit_size * base_units_num), ruler_y - 2), font_size=str(h_font_size) + 'px',  fill='black', text_anchor='middle'))

dwg.save()














