import moviepy.editor as mp
import os
from memes.editbase import EditBase

class Hypercam(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
		# Hypercam watermark
		asset_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__,'..'))),'assets')
		self.hypercam_asset = os.path.join(asset_dir,'hypercam.png')
		
	def add_subparser(sp):
		parser = sp.add_parser('hypercam')
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-d', '--duration', help="Duration (in seconds). Must be specified if input is image")
	
	def process(self):
		if (self.args.image):
			if (self.args.duration):
				duration = self.args.duration
				orig_clip = mp.ImageClip(self.args.input, duration=duration).resize(newsize=self.TARGET_SIZE)
			else:
				raise Exception("hypercam: Input is image, but duration is unspecified")
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			duration = orig_clip.duration
		
		watermark = mp.ImageClip(self.hypercam_asset, duration=duration).set_position(("left","top"))
		
		layers = [orig_clip, watermark]
		
		hypermeme = mp.CompositeVideoClip(layers, size=self.TARGET_SIZE)
		final = hypermeme
		return final
