import moviepy.editor as mp
from memes.editbase import EditBase
import os

class Demotivational(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
		# default audio
		audio_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__,'..'))),'audio')
		self.audio = os.path.join(audio_dir,'sanctuary-guardian.ogg')
	
	def add_subparser(sp):
		parser = sp.add_parser('demotivational')
		parser.add_argument('-t', '--top', default="WHAT", help="Top text")
		parser.add_argument('-b', '--bottom', default="HOW", help="Bottom text")
		parser.add_argument('-n', '--no-prepend', help="Don't prepend the original clip", action='store_true')
		parser.add_argument('-i', '--image', help="Input is an image", action='store_true')
		parser.add_argument('-a', '--audio', help="Audio file to play")
	
	def process(self):
		sequence = []
		
		if(self.args.audio):
			audio = mp.AudioFileClip(self.args.audio)
		else:
			audio = mp.AudioFileClip(self.audio)
		
		blank_video = mp.ColorClip(color=(0,0,0), duration=audio.duration, size=self.TARGET_SIZE)
		
		if (self.args.image):
			freeze_frame = mp.ImageClip(self.args.input, duration=audio.duration)
		else:
			orig_clip = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
			
			if(self.args.no_prepend == False):
				sequence.append(orig_clip)
			
			freeze_frame = orig_clip.to_ImageClip(orig_clip.duration-0.1, duration=audio.duration)
		
		frame_size = (0.8, 0.6)
		gap_size = 0.005
		
		border_white = mp.ColorClip(color=(255,255,255),
									duration=audio.duration,
									size=self.relative_to(self.TARGET_SIZE, frame_size)
									)
		border_black = mp.ColorClip(color=(0,0,0),
									duration=audio.duration,
									size=self.relative_to(self.TARGET_SIZE, tuple(size-gap_size for size in frame_size))
									)
		freeze_frame = freeze_frame.resize(self.relative_to(self.TARGET_SIZE, tuple(size-(gap_size*2) for size in frame_size)))
		
		layers = [blank_video,border_white,border_black,freeze_frame]
		
		for i in range(len(layers)):
			layers[i] = layers[i].set_position(("center",0.1+(gap_size*i*0.5)),relative=True)
		
		top_text = mp.TextClip(self.args.top, color='white', font="Times-New-Roman", fontsize=36)
		top_text = top_text.set_position(("center",frame_size[1]+0.15),relative=True)
		top_text = top_text.set_duration(audio.duration)
		
		bottom_text = mp.TextClip(self.args.bottom, color='white', font="Times-New-Roman", fontsize=18)
		bottom_text = bottom_text.set_position(("center",frame_size[1]+0.3),relative=True)
		bottom_text = bottom_text.set_duration(audio.duration)
		
		layers.append(top_text)
		layers.append(bottom_text)
		
		part = mp.CompositeVideoClip(layers, size=self.TARGET_SIZE)
		part = part.set_audio(audio)
		sequence.append(part)
		
		final = mp.concatenate_videoclips(sequence)
		return final
