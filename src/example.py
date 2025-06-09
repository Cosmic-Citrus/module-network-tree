from tree_configuration import ModuleTreeConfiguration
from network_configuration import NetworkConfiguration


path_to_directory = "/Users/owner/Desktop/programming/module_network_tree/src/"
path_to_save_directory = "/Users/owner/Desktop/programming/module_network_tree/output/"


if __name__ == "__main__":

	module_tree = ModuleTreeConfiguration()
	module_tree.initialize(
		path_to_directory=path_to_directory)
	network = NetworkConfiguration(
		tree=module_tree,
		is_include_common=True,
		is_include_uncommon=True,
		is_include_custom=True)
	network.update_save_directory(
		path_to_save_directory=path_to_save_directory)

	# print(network)
	network.write_module_hierarchy_to_file()
	network.view_graph(
		# layout="arf",
		layout="shell",
		# layout="circular",
		# layout="planar",
		# layout="spring",
		# layout="spiral",
		top_level_color="lightsteelblue",
		common_successor_color="bisque",
		uncommon_successor_color="bisque",
		custom_successor_color="bisque",
		is_with_legend=True,
		figsize=(12, 7),
		is_save=True)

##