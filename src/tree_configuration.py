import os
from node_visitor_configuration import NodeVisitorConfiguration


class BaseModuleTreeConfiguration():

	def __init__(self):
		super().__init__()
		self._path_to_directory = None
		self._pre_selected_import_names = None
		self._import_names = None
		self._branches = None
		self._canopy = None

	@property
	def path_to_directory(self):
		return self._path_to_directory
	
	@property
	def pre_selected_import_names(self):
		return self._pre_selected_import_names
	
	@property
	def import_names(self):
		return self._import_names

	@property
	def branches(self):
		return self._branches

	@property
	def canopy(self):
		return self._canopy

	def pre_initialize(self, path_to_directory):
		if path_to_directory is not None:
			if not isinstance(path_to_directory, str):
				raise ValueError("invalid type(path_to_directory): {}".format(type(path_to_directory)))
		pre_selected_import_names = {
			"common" : tuple([
				"os",
				"pathlib",
				"numpy",
				"scipy",
				"matplotlib",
				"mpl_toolkits",
				"pandas",
				"sympy",
				"networkx",
				"itertools",
				"datetime",
				"pygame"]),
			"uncommon" : tuple([
				"numpy_indexed",
				"moviepy",
				"skimage",
				"cv2",
				"ast",
				"re"])}
		import_names = {
			"common" : set(),
			"uncommon" : set(),
			"custom" : set()}
		branches = dict()
		self._path_to_directory = path_to_directory
		self._pre_selected_import_names = pre_selected_import_names
		self._import_names = import_names
		self._branches = branches

	def grow_branches(self, path_to_file, file_name):
		node_visitor = NodeVisitorConfiguration()
		module_names = node_visitor.get_imported_module_names(
			path_to_file=path_to_file)
		branch = {
			"common" : list(),
			"uncommon" : list(),
			"custom" : list()}
		for module_name in module_names:
			if module_name in self.pre_selected_import_names["common"]:
				key = "common"
			elif module_name in self.pre_selected_import_names["uncommon"]:
				key = "uncommon"
			else:
				key = "custom"
			self._import_names[key].add(
				module_name)
			branch[key].append(
				module_name)
		self._branches[file_name] = branch

	def initialize_canopy(self):
		
		def replace_sets_with_lists(data):
			for key, value in data.items():
				if isinstance(value, set):
					modified_value = list(
						value)
					data[key] = modified_value
				elif isinstance(value, data):
					replace_sets_with_lists(
						data=value)
				elif not isinstance(value, list):
					raise ValueError("invalid type(value): {}".format(type(value)))
			return data

		extension = ".py"
		module_names = tuple(
			list(
				self.import_names["custom"]))
		canopy = dict()
		for module_name in module_names:
			for file_name_with_extension, imported_module_names in self.branches.items():
				file_name = file_name_with_extension.replace(
					".py",
					"")
				if file_name not in canopy.keys():
					canopy[file_name] = set()
				common_names = imported_module_names["common"]
				uncommon_names = imported_module_names["uncommon"]
				custom_names = imported_module_names["custom"]
				if custom_names is not None:
					for custom_name in custom_names:
						if module_name == custom_name:
							canopy[file_name].add(
								custom_name)
				if common_names is not None:
					canopy[file_name].update(
						common_names)
				if uncommon_names is not None:
					canopy[file_name].update(
						uncommon_names)

		canopy = replace_sets_with_lists(
			data=canopy)
		canopy = self.replace_empty_list_with_none(
			data=canopy)
		self._canopy = canopy

	def trim_branches(self):
		branches = self.replace_empty_list_with_none(
			data=self._branches)
		self._branches = branches

	def replace_empty_list_with_none(self, data):
		for key, value in data.items():
			if value is not None:
				if isinstance(value, list):
					number_values = len(
						value)
					if number_values == 0:
						data[key] = None
				elif isinstance(value, dict):
					self.replace_empty_list_with_none(
						data=value)
				else:
					raise ValueError("invalid type(value): {}".format(type(value)))
		return data

class ModuleTreeConfiguration(BaseModuleTreeConfiguration):

	def __init__(self):
		super().__init__()

	def initialize(self, path_to_directory):
		self.pre_initialize(
			path_to_directory=path_to_directory)
		for path_to_selected_directory, sub_directory_names, file_names in os.walk(path_to_directory):
			for file_name in file_names:
				if file_name.endswith(".py"):
					path_to_file = "{}{}".format(
						path_to_selected_directory,
						file_name)
					self.grow_branches(
						path_to_file=path_to_file,
						file_name=file_name)
		self.trim_branches()
		self.initialize_canopy()

##