import networkx as nx
from tree_configuration import ModuleTreeConfiguration
from plotter_network_configuration import NetworkViewer
from plotter_base_configuration import BasePlotterConfiguration

class BaseNetworkConfiguration(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()
		self._tree = None
		self._graph = None
		self._hierarchy = None
		self._top_level_nodes = None
		self._is_include_common = None
		self._is_include_uncommon = None
		self._is_include_custom = None

	@property
	def tree(self):
		return self._tree
	
	@property
	def graph(self):
		return self._graph
	
	@property
	def hierarchy(self):
		return self._hierarchy

	@property
	def top_level_nodes(self):
		return self._top_level_nodes
	
	@property
	def is_include_common(self):
		return self._is_include_common

	@property
	def is_include_uncommon(self):
		return self._is_include_uncommon

	@property
	def is_include_custom(self):
		return self._is_include_custom

	def initialize_tree(self, tree):
		if not isinstance(tree, ModuleTreeConfiguration):
			raise ValueError("invalid type(tree): {}".format(type(tree)))
		if tree.canopy is None:
			raise ValueError("tree.canopy is not initialized")
		self._tree = tree

	def initialize_graph(self, is_include_common, is_include_uncommon, is_include_custom):
		
		def get_import_state(module_name, key, is_include):
			state = (
				(module_name in self.tree.import_names[key]) and is_include)
			return state

		if not isinstance(is_include_common, bool):
			raise ValueError("invalid type(is_include_common): {}".format(type(is_include_common)))		
		if not isinstance(is_include_uncommon, bool):
			raise ValueError("invalid type(is_include_uncommon): {}".format(type(is_include_uncommon)))
		if not isinstance(is_include_custom, bool):
			raise ValueError("invalid type(is_include_custom): {}".format(type(is_include_custom)))
		if not (is_include_common or is_include_uncommon or is_include_custom):
			raise ValueError("invalid inputs: is_include_common=False, is_include_uncommon=False, is_include_custom=False")
		graph = nx.DiGraph()
		for module_name, import_names in self.tree.canopy.items():
			common_state_at_root = get_import_state(
				module_name=module_name,
				key="common",
				is_include=is_include_common)
			uncommon_state_at_root = get_import_state(
				module_name=module_name,
				key="uncommon",
				is_include=is_include_uncommon)
			custom_state_at_root = get_import_state(
				module_name=module_name,
				key="custom",
				is_include=is_include_custom)
			if (common_state_at_root or uncommon_state_at_root or custom_state_at_root):
				if not graph.has_node(module_name):
					graph.add_node(
						module_name)
				if import_names is not None:
					for import_name in import_names:
						if not graph.has_edge(module_name, import_name):
							common_state_at_successor = get_import_state(
								module_name=import_name,
								key="common",
								is_include=is_include_common)
							uncommon_state_at_successor = get_import_state(
								module_name=import_name,
								key="uncommon",
								is_include=is_include_uncommon)
							custom_state_at_successor = get_import_state(
								module_name=import_name,
								key="custom",
								is_include=is_include_custom)
							if (common_state_at_successor or uncommon_state_at_successor or custom_state_at_successor):
								graph.add_edge(
									module_name,
									import_name)
		cycles = list(
			nx.simple_cycles(
				graph))
		number_cycles = len(
			cycles)
		if number_cycles != 0:
			raise ValueError("graph contains cycles: {}".format(cycles))
		self._graph = graph
		self._is_include_common = is_include_common
		self._is_include_uncommon = is_include_uncommon
		self._is_include_custom = is_include_custom

	def initialize_hierarchy(self):
		hierarchy = dict()
		for node in self.tree.import_names["custom"]:
			if node not in hierarchy.keys():
				hierarchy[node] = list()
				for successor in self.graph.successors(node):
					hierarchy[node].append(
						successor)
		self._hierarchy = hierarchy

	def initialize_top_level_nodes(self):
		top_level_nodes = list()
		for node in self.graph.nodes():
			if not self.graph.in_degree(node):  # No incoming edges
				top_level_nodes.append(
					node)
		self._top_level_nodes = top_level_nodes

	def get_string(self):

		def get_title_with_under_line(title, symbol):
			number_characters = len(
				title)
			under_line = symbol * (number_characters + 2) ## symmetric about one extra space per side
			label = "\n{}\n{}\n".format(
				title,
				under_line)
			return label

		def get_label_at_title():
			title = " ** IMPORT HIERARCHY INFORMATION **"
			label = get_title_with_under_line(
				title=title,
				symbol="=")
			return label

		def get_labels_at_top_level_nodes():
			labels = list()
			for node in self.top_level_nodes:
				partial_label = " .. {}\n".format(
					node)
				labels.append(
					partial_label)
			title = " ** List of Modules at Top-Level **"
			title_with_under_line = get_title_with_under_line(
				title=title,
				symbol="-")
			labels.insert(
				0,
				title_with_under_line)
			return labels

		def get_labels_at_imports():
			module_names = list()
			module_names.extend(
				list(
					self.tree.import_names["common"]))
			module_names.extend(
				list(
					self.tree.import_names["uncommon"]))
			module_names.extend(
				list(
					self.tree.import_names["custom"]))
			labels = list()
			for module_name in module_names:
				if (module_name in self.tree.import_names["common"]) or (module_name in self.tree.import_names["uncommon"]):
					label = "\n .. {} (Standard Library or Third-Party Module/Package)".format(
						module_name)
				elif module_name in self.tree.import_names["custom"]:
					label = "\n .. {} (Custom Module/Package)".format(
						module_name)
				else:
					raise ValueError("invalid module_name: {}".format(module_name))
				if module_name in self.top_level_nodes:
					label = label.replace(
						"(",
						"(Top-Level; ")
				labels.append(
					label)
			title = " ** List of Imported Modules **"
			title_with_under_line = get_title_with_under_line(
				title=title,
				symbol="-")
			labels.insert(
				0,
				title_with_under_line)
			return labels

		def get_labels_at_import_hierarchy():
			labels = list()
			for module_name, import_names in self.hierarchy.items():
				partial_label = "\n {}:\n".format(
					module_name)
				for import_name in import_names:
					partial_label += " .. {}\n".format(
						import_name)
				labels.append(
					partial_label)
			title = " ** Hierarchy of Imported Modules **"
			title_with_under_line = get_title_with_under_line(
				title=title,
				symbol="-")
			labels.insert(
				0,
				title_with_under_line)
			return labels

		label_at_title = get_label_at_title()
		labels_at_top_level_nodes = get_labels_at_top_level_nodes()
		labels_at_imports = get_labels_at_imports()
		labels_at_import_hierarchy = get_labels_at_import_hierarchy()
		labels = [
			label_at_title,
			*labels_at_top_level_nodes,
			*labels_at_imports,
			*labels_at_import_hierarchy]
		s = "\n".join(
			labels)
		return s

class NetworkConfiguration(BaseNetworkConfiguration):

	def __init__(self, tree, is_include_common=False, is_include_uncommon=False, is_include_custom=False):
		super().__init__()
		self.initialize_visual_settings()
		self.initialize_tree(
			tree=tree)
		self.initialize_graph(
			is_include_common=is_include_common,
			is_include_uncommon=is_include_uncommon,
			is_include_custom=is_include_custom)
		self.initialize_hierarchy()
		self.initialize_top_level_nodes()

	def __repr__(self):
		network = f"NetworkConfiguration()"
		return network

	def __str__(self):
		s = self.get_string()
		return s

	def write_module_hierarchy_to_file(self, extension=".txt"):
		self.verify_visual_settings()
		if self.visual_settings.path_to_save_directory is None:
			# raise ValueError("self.visual_settings.path_to_directory is not initialized")
			path_to_save_directory = self.tree.path_to_directory[:]
		else:
			path_to_save_directory = self.visual_settings.path_to_save_directory[:]
		allowed_extensions = (
			".txt",
			)
		if extension not in allowed_extensions:
			raise ValueError("invalid extension: {}".format(extension))
		file_name = "module_hierarchy"
		output_path = "{}{}{}".format(
			path_to_save_directory,
			file_name,
			extension)
		with open(output_path, "w") as data_file:
			data_file.write(
				str(
					self))

	def view_graph(self, layout="shell", top_level_color="orange", common_successor_color="skyblue", uncommon_successor_color="gold", custom_successor_color="limegreen", edge_color="silver", font_weight="bold", margins=0.4, is_with_legend=False, figsize=None, is_save=False):
		plotter = NetworkViewer()
		plotter.initialize_visual_settings()
		plotter.update_save_directory(
			path_to_save_directory=self.visual_settings.path_to_save_directory)
		plotter.view_graph(
			network=self,
			layout=layout,
			top_level_color=top_level_color,
			common_successor_color=common_successor_color,
			uncommon_successor_color=uncommon_successor_color,
			custom_successor_color=custom_successor_color,
			edge_color=edge_color,
			font_weight=font_weight,
			margins=margins,
			is_with_legend=is_with_legend,
			figsize=figsize,
			is_save=is_save)

##