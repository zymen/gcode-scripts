from math import sqrt
from read_image import main

def wall_bottom_iteration(start_x, start_y, start_z, width, height, depth):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z,
             'width': width,
             'height': height,
             'depth': depth}

	tit_inside_size = 3

	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d

	steps = 10

	print "G1 x" + str(start_x + width) +" y%(start_y)d z%(start_z)d" % d
	print "G1 x" + str(start_x + width) +" y" + str(start_y + height) +" z%(start_z)d" % d
	print "G1 x%(start_x)d y" %d + str(start_y + height) +" z%(start_z)d" % d
	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d


def wall_bottom(start_x, start_y, start_z, width, height, depth, z_feed_rate):
	iterations = (depth / z_feed_rate) + 1
	print "(Preparing data for bottom wall)"

	print "G00 z10"
	print "G00 x" + str(start_x) + " y" + str(start_y) + " z10"
	print "G00 z0"
	
	for i in range(0, iterations):
		wall_bottom_iteration(start_x, start_y, start_z - z_feed_rate * i, width, height, depth)

def tit_y(start_x, start_y, start_z):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z}

	tit_inside_size = 3

	#print "G10 L2 P1 x10"
	print "(tit_y start)"
	print "G1 x" + str(start_x) +" y" + str(start_y + tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(start_x - tit_inside_size) +" y" + str(start_y + tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(start_x - tit_inside_size) +" y" + str(start_y + 2* tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(start_x) +" y" + str(start_y + 2* tit_inside_size) +" z%(start_z)d" % d

	#print "G10 L2 P1 X0 Y0 Z0"

def tit_x(start_x, start_y, start_z, per):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z}

	tit_inside_size = 3
	offset = 0

	if per == 1:
		offset = 4 + tit_inside_size

	print "G1 x" + str(offset + start_x + tit_inside_size) +" y%(start_y)d z%(start_z)d" % d
	print "G1 x" + str(offset + start_x + tit_inside_size) +" y" + str(start_y + tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(offset + start_x + 2 * tit_inside_size) +" y" + str(start_y + tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(offset + start_x + 2 * tit_inside_size) +" y" + str(start_y) +" z%(start_z)d" % d

def tit_x2(start_x, start_y, start_z, per):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z}

	tit_inside_size = 3
	offset = 0

	if per == 1:
		offset = tit_inside_size

	print "G1 x" + str(offset + start_x - tit_inside_size) +" y%(start_y)d z%(start_z)d" % d
	print "G1 x" + str(offset + start_x - tit_inside_size) +" y" + str(start_y - tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(offset + start_x - 2 * tit_inside_size) +" y" + str(start_y - tit_inside_size) +" z%(start_z)d" % d
	print "G1 x" + str(offset + start_x - 2 * tit_inside_size) +" y" + str(start_y) +" z%(start_z)d" % d
	

def tit(x, y, z, direction):
	tit_size = 3

	if direction == 'in':
		m = 1
	else:
		m = -1

	data = {'left_top_x': x, 
		'left_top_y': y,
		'left_bottom_x': x, 
		'left_bottom_y': y + tit_size,
		'right_top_x': x + tit_size, 
		'right_top_y': y,
		'right_bottom_x': x + tit_size, 
		'right_bottom_y': y + tit_size,
		'right_top_x_next': x + 2 * tit_size}
			
	print "G1 x%(left_top_x)d y%(left_top_y)d " % data
	print "G1 x%(left_bottom_x)d y%(left_bottom_y)d " % data
	print "G1 x%(right_bottom_x)d y%(right_bottom_y)d " % data
	print "G1 x%(right_top_x)d y%(right_top_y)d " % data
	print "G1 x%(right_top_x_next)d y%(right_top_y)d " % data

def tits_x(start_x, start_y, start_z, tits_number, direction):
	def e(x, y):
		return {'x': x, 'y': y}

	tit_size = 3
	offset = 0

	if direction == 'in':
		m = 1
	else:
		m = -1

	#print "G1 x%d y%d " % (start_x + 2*tit_size, start_y)
	for tit_index in range(0, tits_number):
		tit(start_x + tit_size * 2 * tit_index, 
		    start_y + m * tit_size, 
		    start_z, direction)	

	print "G10 L2 P2  R0"
	
def wall_iteration(start_x, start_y, start_z, width, height, depth, per = 1):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z,
             'width': width,
             'height': height,
             'depth': depth}

	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d

	steps = 10

	tits_x(start_x, start_y, start_z, 4, 'out')

	#for position in range(start_x + 6, start_x + width - 24 , 6):
		#tit_x(position, start_y, start_z, per)

	print "G1 x" + str(start_x + width) +" y%(start_y)d z%(start_z)d" % d

	#for position in range(start_y + 6, start_y + height - 6, 6):
		#tit_y(start_x + width, position, start_z)

	print "G1 x" + str(start_x + width) +" y" + str(start_y + height) +" z%(start_z)d" % d
	print "G0 x" + str(start_x + width) +" y" + str(start_y + height) +" z10" % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height)  % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height) +" z%(start_z)d" % d 

	tits_x(start_x, start_y + height, start_z, 4, 'out')
	print "G0 z10"  % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height) + " z10"  % d
	print "G0 z%(start_z)d"  % d

	#print "G0 x" + str(start_x + width) +" y" + str(start_y + height) +" z30" % d
	#for position in range(start_x + width - 12, start_x + 18, -6):
		#tit_x2(position, start_y + height, start_z, per)

	print "G1 x%(start_x)d y" %d + str(start_y + height) +" z%(start_z)d" % d
	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d


def wall(start_x, start_y, start_z, width, height, depth, z_feed_rate, per):
	iterations = (depth / z_feed_rate) + 1
	print "(%d iterations for wall)" % iterations

	print "G00 z10"
	print "G00 x" + str(start_x) + " y" + str(start_y) + " z10"
	print "G00 z0"
	
	for i in range(0, iterations):
		wall_iteration(start_x, start_y, start_z - z_feed_rate * i, width, height, depth, per)

def box(x_size, z_size, y_size):
	z_feed_rate = 6
	material_height = 5 
	distance = 8

	#bottom 
	print "(bottom wall)"
	wall_bottom(0, 0, 0, x_size, y_size, material_height, z_feed_rate)

	#top
	print "(top wall)"
	wall(x_size + distance, 0, 0, x_size, y_size, material_height, z_feed_rate, 1)

	#side walls
	print "(side walls)"
	print "(side wall 1)"
	wall(0, y_size + distance, 0, x_size, z_size, material_height, z_feed_rate, 1)

	print "(side wall 2)"
	wall(x_size + distance, y_size + distance, 0, x_size, z_size, material_height, z_feed_rate, 1)

	print "(side wall 3)"
	wall(0, z_size + y_size + 2 * distance, 0, z_size, y_size, material_height, z_feed_rate, -1)

	print "(side wall 4)"
	wall(z_size + distance, z_size + y_size + 2 * distance, 0, z_size, y_size, material_height, z_feed_rate, -1)

print "S1M3"
print "G21"
print "g0 z1"
print "g0 x.25 y1.0"
print "g1 f10000 z0"

box(x_size = 120, y_size = 60, z_size = 30)

#main()

print "g0 z1"
print "M2"
