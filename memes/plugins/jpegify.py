# WARNING: SLOW AS SHIT

import moviepy.editor as mp
from PIL import Image
import numpy
from io import BytesIO

from memes.editbase import EditBase

class Jpegify(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
	def add_subparser(sp):
		parser = sp.add_parser('jpegify')
		parser.add_argument('-q', '--quality', default="Quality")
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-d', '--duration', help="Duration (in seconds). Must be specified if input is image")
	
	def process(self):
		if (self.args.image):
			if (self.args.duration):
				duration = self.args.duration
				orig_clip = mp.ImageClip(self.args.input, duration=duration).resize(newsize=self.TARGET_SIZE)
			else:
				raise Exception("jpegify: Input is image, but duration is unspecified")
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			duration = orig_clip.duration
		
		quality = 10
		
		def jpegify(i):
			array = Image.fromarray(numpy.uint8(i))
			buf = BytesIO()
			array.save(buf, "JPEG", quality=quality)
			jpeg = Image.open(buf)
			jpeg_array = numpy.array(jpeg)
			return jpeg_array
			
		jpgified = orig_clip.fl_image(jpegify)
		
		final = jpgified
		return final
