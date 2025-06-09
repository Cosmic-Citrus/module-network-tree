import networkx as nx
import matplotlib.pyplot as plt
from plotter_base_configuration import BasePlotterConfiguration


class BaseNetworkViewer(BasePlotterConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_node_colors(network, top_level_color, common_successor_color, uncommon_successor_color, custom_successor_color):
		node_color = list()
		for node in network.graph.nodes():
			if node in network.top_level_nodes:
				node_color.append(
					top_level_color)
			else:
				if node in network.tree.import_names["common"]:
					node_color.append(
						common_successor_color)
				elif node in network.tree.import_names["uncommon"]:
					node_color.append(
						uncommon_successor_color)
				elif node in network.tree.import_names["custom"]:
					node_color.append(
						custom_successor_color)
				else:
					raise ValueError("invalid node: {}".format(node))
		return node_color

	@staticmethod
	def get_pos(network, layout):
		if layout is None:
			pos = None
		else:
			layout_mapping = {
				"arf" : nx.arf_layout,
				"shell" : nx.shell_layout,
				"circular" : nx.circular_layout,
				"planar" : nx.planar_layout,
				"spring" : nx.spring_layout,
				"spiral" : nx.spiral_layout}
			if layout not in layout_mapping.keys():
				raise ValueError("invalid layout: {}".format(layout))
			selected_layout = layout_mapping[layout]
			pos = selected_layout(
				network.graph)
		return pos

	@staticmethod
	def autocorrect_scaling(ax, margins):
		ax.margins(
			x=margins)
		return ax

	@staticmethod
	def get_save_name(is_save):
		if is_save:
			save_name = "module_network_graph"
		else:
			save_name = None
		return save_name

	def plot_legend(self, fig, ax, network, top_level_color, common_successor_color, uncommon_successor_color, custom_successor_color, edge_color):

		def get_unique_node_colors(network, top_level_color, common_successor_color, uncommon_successor_color, custom_successor_color):
			unique_node_colors = set()
			unique_node_colors.add(
				top_level_color)
			if network.is_include_common:
				unique_node_colors.add(
					common_successor_color)
			if network.is_include_uncommon:
				unique_node_colors.add(
					uncommon_successor_color)
			if network.is_include_custom:
				unique_node_colors.add(
					custom_successor_color)
			unique_node_colors = list(
				unique_node_colors)
			return unique_node_colors

		def get_unique_node_labels(network, unique_node_colors, top_level_color, common_successor_color, uncommon_successor_color, custom_successor_color):
			top_level_label = "Modules and Packages\nat Top-Level"
			common_label = "Common Modules\nand Packages"
			uncommon_label = "Uncommon Modules\nand Packages"
			custom_label = "Custom Modules\nand Packages"
			non_custom_label = "Standard Library\nModules and Packages"
			label_mapping = {
				## one element is True
				(True, False, False, False) : "Modules and Packages\nat Top-Level", ## top-level
				(False, True, False, False) : "Common Modules\nand Packages", ## common
				(False, False, True, False) : "Uncommon Modules\nand Packages", ## uncommon
				(False, False, False, True) : "Custom Modules\nand Packages", ## custom
				## two elements [0, ...] are True
				(True, True, False, False) : "Common Modules\nand Packages\nat Top-Level",
				(True, False, True, False) : "Uncommon Modules\nand Packages\nat Top-Level",
				(True, False, False, True) : "Custom Modules\nand Packages\nat Top-Level",
				## two elements [not 0, ... > 0] are True
				(False, True, True, False) : "Standard Library\nand Third Party\nModules and Packages",
				(False, True, False, True) : "Common and Custom\nModules and Packages",
				(False, False, True, True) : "Uncommon and Custom\nModules and Packages",
				## three elements are True
				(True, True, True, False) : "Standard Library\nand Third Party\nModules and Packages\nAt Top-Level",
				(True, True, False, True) : "Common and Custom\nModules and Packages\nAt Top-Level",
				(True, False, True, True) : "Uncommon and Custom\nModules and Packages\nAt Top-Level",
				(False, True, True, True) : "All Other Imported\nModules and Packages",
				## four elements are True
				(True, True, True, True) : "All Modules and Packages\n(including Top-Level)"}
			unique_node_labels = list()
			for facecolor in unique_node_colors:
				partial_labels = list()
				is_top_level = (
					facecolor == top_level_color)
				is_common = (
					network.is_include_common and (facecolor == common_successor_color))
				is_uncommon = (
					network.is_include_uncommon and (facecolor == uncommon_successor_color))
				is_custom = (
					network.is_include_custom and (facecolor == custom_successor_color))
				state = (
					is_top_level,
					is_common,
					is_uncommon,
					is_custom)
				label = label_mapping[state]
				unique_node_labels.append(
					label)
			return unique_node_labels

		unique_node_colors = get_unique_node_colors(
			network=network,
			top_level_color=top_level_color,
			common_successor_color=common_successor_color,
			uncommon_successor_color=uncommon_successor_color,
			custom_successor_color=custom_successor_color)
		facecolors = unique_node_colors + [edge_color]
		unique_node_labels = get_unique_node_labels(
			network=network,
			unique_node_colors=unique_node_colors,
			top_level_color=top_level_color,
			common_successor_color=common_successor_color,
			uncommon_successor_color=uncommon_successor_color,
			custom_successor_color=custom_successor_color)
		edge_label = "'o' imports\nfrom '>'"
		labels = unique_node_labels + [edge_label]
		number_leg_columns = len(
			labels)
		handles = list()
		for facecolor, label in zip(facecolors, labels):
			handle = ax.scatter(
				list(),
				list(),
				color=facecolor,
				marker="o")
			handles.append(
				handle)
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			number_columns=number_leg_columns)
		return fig, ax, leg

class NetworkViewer(BaseNetworkViewer):

	def __init__(self):
		super().__init__()

	def view_graph(self, network, layout, top_level_color, common_successor_color, uncommon_successor_color, custom_successor_color, edge_color, font_weight, margins, is_with_legend, figsize, is_save):
		pos = self.get_pos(
			network=network,
			layout=layout)
		node_color = self.get_node_colors(
			network=network,
			top_level_color=top_level_color,
			common_successor_color=common_successor_color,
			uncommon_successor_color=uncommon_successor_color,
			custom_successor_color=custom_successor_color)
		fig, ax = plt.subplots(
			figsize=figsize)
		nx.draw(
			network.graph,
			pos=pos,
			ax=ax,
			node_color=node_color,
			edge_color=edge_color,
			font_weight=font_weight,
			font_size=self.visual_settings.label_size,
			with_labels=True,
			arrows=True)
		ax = self.autocorrect_scaling(
			ax=ax,
			margins=margins)
		if is_with_legend:
			fig, ax, leg = self.plot_legend(
				fig=fig,
				ax=ax,
				network=network,
				top_level_color=top_level_color,
				common_successor_color=common_successor_color,
				uncommon_successor_color=uncommon_successor_color,
				custom_successor_color=custom_successor_color,
				edge_color=edge_color)
		save_name = self.get_save_name(
			is_save=is_save)
		self.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##