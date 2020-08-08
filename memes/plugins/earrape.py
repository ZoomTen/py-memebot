import moviepy.editor as mp
import numpy
from memes.editbase import EditBase

class Earrape(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
	def add_subparser(sp):
		parser = sp.add_parser('earrape')
	
	def process(self):
		orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
		orig_audio = orig_clip.audio
		
		factor = 0.02
		target_db = 0.4
		
		def clip(gf,t):
			x = gf(t)
			return numpy.clip(x,0,factor)*(target_db/factor)
		
		clipped = orig_audio.fl(clip, apply_to='audio')
		
		eclip = orig_clip.set_audio(clipped)
		final = eclip
		return final
