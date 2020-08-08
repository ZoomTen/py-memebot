import moviepy.editor as mp
from memes.editbase import EditBase

class Impactfont(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
	def add_subparser(sp):
		parser = sp.add_parser('impactfont')
		parser.add_argument('-t', '--top', default="TOP TEXT", help="Top text")
		parser.add_argument('-b', '--bottom', default="BOTTOM TEXT", help="Bottom text")
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-d', '--duration', help="Duration (in seconds). Must be specified if input is image")
	
	def process(self):
		if (self.args.image):
			if (self.args.duration):
				duration = self.args.duration
				orig_clip = mp.ImageClip(self.args.input, duration=duration).resize(newsize=self.TARGET_SIZE)
			else:
				raise Exception("impactmeme: Input is image, but duration is unspecified")
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			duration = orig_clip.duration
		
		stroke_width = 2
		font_size = 42
		font = "Impact"
		
		top_text = mp.TextClip(self.args.top, font=font, fontsize=font_size, stroke_width=stroke_width, stroke_color="black", color='white')
		top_text = top_text.set_position(("center","top"))
		top_text = top_text.set_duration(duration)
		
		#top_text_top = mp.TextClip(self.args.top, font=font, fontsize=font_size, color='white')
		#top_text_top = top_text_top.set_position(("center","top"))
		#top_text_top = top_text_top.set_duration(duration)
		
		bottom_text = mp.TextClip(self.args.bottom, font=font, fontsize=font_size, stroke_width=stroke_width, stroke_color="black", color='white')
		bottom_text = bottom_text.set_position(("center","bottom"))
		bottom_text = bottom_text.set_duration(duration)
		
		#bottom_text_top = mp.TextClip(self.args.bottom, font=font, fontsize=font_size, color='white')
		#bottom_text_top = bottom_text_top.set_position(("center","bottom"))
		#bottom_text_top = bottom_text_top.set_duration(duration)
		
		layers = [orig_clip,top_text,bottom_text]#,top_text_top,bottom_text_top]
		
		final = mp.CompositeVideoClip(layers, size=self.TARGET_SIZE)
		return final
