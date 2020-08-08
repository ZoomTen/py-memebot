import moviepy.editor as mp
import re
from memes.editbase import EditBase

class Combine(EditBase):
	def __init__(self, args):
		super().__init__(args)
		
	def add_subparser(sp):
		parser = sp.add_parser('combine')
		parser.add_argument('expression', help="Combinator string")
	
	def process(self):
		# example syntax: impactfont:top=top text:bottom=bottom text;hypercam;ifunny;demotivational:top=WHAT:bottom=HOW
		# will be split into:
		# impactfont -> top="top text" bottom="bottom text"
		# hypercam
		# ifunny
		# demotivational -> top="WHAT":bottom="HOW"
		
		commands = re.findall(r'\w+:?[A-Za-z0-9="\'\s:]+;?', self.args.expression)
		tokens = [re.findall(r'\w+="?[A-Za-z0-9_ ]+"?|\w+', i) for i in commands]
		
		process = []
		
		for i in tokens:
			name = i[0]
			values = {}
			for x in i[1:]:
				vals = re.search(r'(\w+)=("?[A-Za-z0-9_\s]+"?)', x)
				if vals is not None:
					values[vals.group(1)] = vals.group(2)
			single_process = {}
			single_process['name'] = name
			single_process['params'] = values
			process.append(single_process)
		
		for i in range(len(process)):
			print("{}:".format(i))
			for key, value in process[i].items():
				print('    {}: {}'.format(key, value))
		
		# TODO: implement the actual processing and stuff
		
		final = mp.VideoFileClip(self.args.input).resize(newsize=self.TARGET_SIZE)
		return final
