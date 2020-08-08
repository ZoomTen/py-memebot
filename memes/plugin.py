#inspired by morevna project's renderchan module handling

from memes.editbase import EditBase
from importlib import import_module
import os, sys
import inspect

class PluginManager():
	def __init__(self):
		self.PLUGIN_DIR_NAME = 'plugins'
		self.plugins = {}
	
	def load(self, name):
		try:
			module = import_module('.'.join(['memes',self.PLUGIN_DIR_NAME,name]))
		except ImportError as e:
			raise ImportError("{}: module doesn't exist - ({})".format(name, e)) from None
		
		class_name = name.capitalize()
		
		try:
			module_class = getattr(module, class_name)
		except AttributeError:
			raise ImportError("{}: class loaded must be named '{}'; however it doesn't exist".format(name, class_name)) from None
		
		parent_class = EditBase
		if not issubclass(module_class, parent_class):
			raise ImportError("{}: class {} must be a subclass of {}".format(name, class_name, parent_class.__name__)) from None
		
		self.plugins[name] = module_class
	
	def load_all(self):
		root_dir = os.path.dirname(os.path.abspath(__file__))
		plugins_dir = os.path.join(root_dir, self.PLUGIN_DIR_NAME)
		plugin_files = [f for f in os.listdir(plugins_dir) if os.path.isfile(os.path.join(plugins_dir, f))]
		for f in plugin_files:
			fn, xt = os.path.splitext(f)
			if xt == ".py":
				if fn != "__init__":
					self.load(fn)
