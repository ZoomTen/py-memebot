class EditBase():
	def __init__(self, args):
		self.YOUTUBE_SIZE = (854, 480)
		self.INSTAGRAM_SIZE = (480,480)
		
		# todo: change this
		target_size = {
						"youtube": self.YOUTUBE_SIZE,
						"instagram": self.INSTAGRAM_SIZE
						}
						
		self.args = args
		
		try:
			self.TARGET_SIZE = target_size[args.target_size]
		except:
			self.TARGET_SIZE = target_size["instagram"]
		
	def relative_to(self, target_res, position):
	# target_res and position are both tuples
		return tuple( round(target_res[i] * position[i])
					  for i in range(2)
					)
		
	def render_video(self, video):
		video.write_videofile(self.args.output, fps=30, codec='libx264', audio_codec='aac', ffmpeg_params=['-crf','36'])
