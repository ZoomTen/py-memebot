import moviepy.editor as mp
from memes.editbase import EditBase
import os

class Ifunny(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
		# ifunny watermark
		asset_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__,'..'))),'assets')
		self.ifunny_asset = os.path.join(asset_dir,'ifunny.png')
		
	def add_subparser(sp):
		parser = sp.add_parser('ifunny')
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-d', '--duration', help="Duration (in seconds). Must be specified if input is image")
	
	def process(self):
		if (self.args.image):
			if (self.args.duration):
				duration = self.args.duration
				orig_clip = mp.ImageClip(self.args.input, duration=duration).resize(newsize=self.TARGET_SIZE)
			else:
				raise Exception("ifunny: Input is image, but duration is unspecified")
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			duration = orig_clip.duration
		
		width, height = orig_clip.size
		
		height = height - 20
		
		orig_clip = orig_clip.resize(newsize=(width,height))
		
		watermark = mp.ImageClip(self.ifunny_asset, duration=duration).set_position(("right","bottom"))
		
			
		bg_clip = mp.ColorClip(color=(23,23,23), duration=duration, size=self.TARGET_SIZE)
		
		layers = [bg_clip, orig_clip, watermark]
		
		inormie = mp.CompositeVideoClip(layers, size=self.TARGET_SIZE)
		final = inormie
		return final
