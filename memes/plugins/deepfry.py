# WARNING: REALLY FUCKING SLOW

import moviepy.editor as mp
from skimage.filters import unsharp_mask, gaussian
import moviepy.video.fx.all as vfx
from PIL import Image
import numpy
from io import BytesIO

from memes.editbase import EditBase

class Deepfry(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
	def add_subparser(sp):
		parser = sp.add_parser('deepfry')
		parser.add_argument('-f', '--factor', default="Factor")
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-d', '--duration', help="Duration (in seconds). Must be specified if input is image")
	
	def process(self):
		if (self.args.image):
			if (self.args.duration):
				duration = self.args.duration
				orig_clip = mp.ImageClip(self.args.input, duration=duration).resize(newsize=self.TARGET_SIZE)
			else:
				raise Exception("deepfry: Input is image, but duration is unspecified")
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			duration = orig_clip.duration
		def sharpen(i):
			im = Image.fromarray(numpy.uint8(i))
			bu = BytesIO()
			im.save(bu, "JPEG", quality=35)
			ip = Image.open(bu)
			ik = numpy.array(ip)
			ii = unsharp_mask(ik, radius=4, amount=6.0)*255
			return unsharp_mask(ii, radius=0.5, amount=2.0)*255
			
		sharp = orig_clip.fl_image(sharpen)
		contrast = sharp.fx(vfx.lum_contrast, lum=-127, contrast=127)
		
		final = contrast
		return final
