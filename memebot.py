from argparse import ArgumentParser
from memes.plugin import PluginManager
import inspect

if __name__ == '__main__':
	pm = PluginManager()
	pm.load_all()
	
	ap = ArgumentParser(
						description="Shitpost maker script. Built for local use, but bot functionality is planned"
						)
	sp = ap.add_subparsers(dest='type', help='Type of shitpost')
	ap.add_argument(
						'input',
						help='input file'
					)
	ap.add_argument(
						'output',
						help='output file'
					)
	ap.add_argument(
						'-y', '--crf',
						help='CRF (the higher it is the crunchier)', type=int, default=36
					)
	ap.add_argument(
						'-z', '--target-size',
						help='Target resolution {instagram|youtube}', default="instagram"
					)
	
	for plugin_name in pm.plugins:
		pm.plugins[plugin_name].add_subparser(sp)
	
	args = ap.parse_args()
	
	video = pm.plugins[args.type](args)
	
	video.render_video(video.process())
