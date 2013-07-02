from math import sqrt
from read_image import main

class Configuration(object):
	tit_size = 3

config = Configuration()

def wall_bottom_iteration(start_x, start_y, start_z, width, height, depth):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z,
             'width': width,
             'height': height,
             'depth': depth}

	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d

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
			
	#print "G1 x%(left_top_x)d y%(left_top_y)d " % data
	print "G1 x%(left_bottom_x)d y%(left_bottom_y)d " % data
	print "G1 x%(right_bottom_x)d y%(right_bottom_y)d " % data
	print "G1 x%(right_top_x)d y%(right_top_y)d " % data
	print "G1 x%(right_top_x_next)d y%(right_top_y)d " % data

def tits_x(start_x, start_y, start_z, tits_number, direction):
	def e(x, y):
		return {'x': x, 'y': y}

	offset = 0

	if direction == 'in':
		m = 1
	else:
		m = -1

	#print "G1 x%d y%d " % (start_x + 2*tit_size, start_y)
	for tit_index in range(0, tits_number):
		tit(start_x + config.tit_size * 2 * tit_index, 
		    start_y + m * config.tit_size, 
		    start_z, direction)	

	
def wall_iteration(start_x, start_y, start_z, width, height, depth, per = 1):
	d = {'start_x': start_x,
             'start_y': start_y,
             'start_z': start_z,
             'width': width,
             'height': height,
             'depth': depth}

	print "(\t wall start)"
	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d

	print "(\t tits on bottom of wall)"
	tits_x(start_x, start_y, start_z, width / (config.tit_size * 2), 'out')

	print "(\t right side)"
	print "G1 x" + str(start_x + width) +" y" + str(start_y + height - config.tit_size) +" z%(start_z)d" % d
	print "G0 x" + str(start_x + width) +" y" + str(start_y + height - config.tit_size) +" z10" % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height)  % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height) +" z%(start_z)d" % d 

	print "(\t tits on top of wall)"
	tits_x(start_x, start_y + height, start_z, width / (config.tit_size * 2), 'out')

	print "(\t left side)"
	print "G0 z10"  % d
	print "G0 x" + str(start_x) +" y" + str(start_y + height) + " z10"  % d
	print "G0 z%(start_z)d"  % d

	print "(\t move into new place?)"
	print "G1 x%(start_x)d y" %d + str(start_y + height) +" z%(start_z)d" % d
	print "G1 x%(start_x)d y%(start_y)d z%(start_z)d" % d


def wall(start_x, start_y, start_z, width, height, depth, z_feed_rate, per):
	iterations = (depth / z_feed_rate) + 1
	print "(%d iterations for wall)" % iterations

	print "G00 z10"
	print "G00 x" + str(start_x) + " y" + str(start_y) + " z10"
	print "G00 z0"
	
	for i in range(0, iterations):
		start_z_iteration = start_z - z_feed_rate * i
		wall_iteration(start_x, start_y, start_z_iteration, width, height, depth, per)

class Box(object):
	x_size = None
	y_size = None
	z_size = None
	config = None

	def _input_validation(self):
		def is_multiplication(field, field_name):
			if field % self.config.tit_size != 0:
				raise Exception('Invalid ' + field_name + '. Size of box must be a multiplication of tit size')

		is_multiplication(self.x_size, 'x_size')
		is_multiplication(self.y_size, 'y_size')
		is_multiplication(self.z_size, 'z_size')
	

	def __init__(self, x_size, y_size, z_size):
		self.x_size = x_size
		self.y_size = y_size
		self.z_size = z_size

		self.config = config
		self._input_validation()


	def box(self):
		z_feed_rate = 3
		material_height = 6 
		distance = 8

		#bottom 
		print "(bottom wall)"
		wall_bottom(0, 0, 0, self.x_size, self.y_size, material_height, z_feed_rate)

		#top
		print "(top wall)"
		wall(self.x_size + distance, 0, 0, self.x_size, self.y_size, material_height, z_feed_rate, 1)

		#side walls
		print "(side walls)"
		print "(side wall 1)"
		wall(0, self.y_size + distance, 0, self.x_size, self.z_size, material_height, z_feed_rate, 1)

		print "(side wall 2)"
		wall(self.x_size + distance, self.y_size + distance, 0, self.x_size, self.z_size, material_height, z_feed_rate, 1)

		print "(side wall 3)"
		wall(0, self.z_size + self.y_size + 2 * distance, 0, self.z_size, self.y_size, material_height, z_feed_rate, -1)

		print "(side wall 4)"
		wall(self.z_size + distance, self.z_size + self.y_size + 2 * distance, 0, self.z_size, self.y_size, material_height, z_feed_rate, -1)

print "S1M3"
print "G21"
print "g0 z1"
print "g0 x.25 y1.0"
print "g1 f10000 z0"

b = Box(x_size = 60, y_size = 36, z_size = 60)
b.box()


print "g0 z1"
print "M2"
