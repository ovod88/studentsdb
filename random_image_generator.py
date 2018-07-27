import os, numpy, time
from PIL import Image
from studentsdb.settings import MEDIA_ROOT
 
def create_and_save_image(path=MEDIA_ROOT, filename='default.png', width = 30, height = 30, num_of_images = 1):
    width = int(width)
    height = int(height)
    num_of_images = int(num_of_images)

    if path and filename:

    	for n in range(num_of_images):
	        rgb_array = numpy.random.rand(width, height, 3) * 255
	        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGBA')
	        image.save(os.path.join(path, filename))
    else:

	    current = time.strftime("%Y%m%d%H%M%S")
	    os.mkdir(current)
	 
	    for n in range(num_of_images):
	        filename = '{0}/{0}_{1:03d}.png'.format(current, n)
	        rgb_array = numpy.random.rand(width, height, 3) * 255
	        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGBA')
	        image.save(filename)
 
def main(args):
	if len(args) == 3:
		create_and_save_image(width = args[0], height = args[1], num_of_images = args[2])
	else:
		create_and_save_image()

	return 0
 
if __name__ == '__main__':
	import sys
	status = main(sys.argv[1:])
	sys.exit(status)
