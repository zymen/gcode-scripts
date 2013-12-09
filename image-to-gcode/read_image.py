import os
import Image

def level(im, x, y):
	'''
	result = 0
	for a in range(-1, 1):
		for b in range(-1, 1):
			if a == y and b == x:
				continue

			v = im.getpixel((y + a, x + b))
			if v == 255:
				result = result + 1


	return result 
	'''
	v = im.getpixel((y, x))

	if v == 255:
		return 10 
	else:
		return -10

def main():
	distance = 10
	im = Image.open("/home/bfaja/gcode/image.jpg")
	size = im.size
	y_size = size[0]
	x_size = size[1]

	print "G0 x0 y0 z10 f10000"
	was_last = False

	for y in range(0, y_size):	
		print "G0 x0 y" + str(y/3)
		for x in range(0, x_size):

			v = im.getpixel((y, x))
			
			if y % distance == 0 and x % distance == 0:

				if v == 255:
					print "G1 x" + str(x/3) + " y" + str(y/3)
					r =level(im, x, y) 
					print " z" + str(-r)
					was_last = False

				else:
					if not was_last:
						print "G1 z0"
						was_last = True

		print "G0 z10"

	#print "g0 z1"
	print "M2"

if __name__ == '__main__':
	main()
