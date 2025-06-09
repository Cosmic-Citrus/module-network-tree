import numpy as np
import matplotlib.pyplot as plt


class BaseVisualSettingsConfiguration():

	def __init__(self):
		super().__init__()
		self._path_to_save_directory = None
		self._label_size = None

	@property
	def path_to_save_directory(self):
		return self._path_to_save_directory

	@property
	def label_size(self):
		return self._label_size
	
	@staticmethod
	def autocorrect_string_spaces(s, space_replacement=None):
		if not isinstance(s, str):
			raise ValueError("invalid type(s): {}".format(type(s)))
		modified_s = s[:]
		if space_replacement is not None:
			if not isinstance(space_replacement, str):
				raise ValueError("invalid type(space_replacement): {}".format(type(space_replacement)))
			modified_s = s.replace(
				" ",
				space_replacement)
		return modified_s

	def get_save_path(self, save_name, default_extension, extension=None, space_replacement=None):
		if self.path_to_save_directory is None:
			raise ValueError("cannot save plot; self.path_to_save_directory is None")
		if extension is None:
			modified_extension = default_extension[:]
		elif isinstance(extension, str):
			modified_extension = extension[:]
		else:
			raise ValueError("invalid type(extension): {}".format(type(extension)))
		save_path = self.autocorrect_string_spaces(
			s="{}{}{}".format(
				self.path_to_save_directory,
				save_name,
				modified_extension),
			space_replacement=space_replacement)
		return save_path

class VisualLegendConfiguration(BaseVisualSettingsConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_empty_label():
		empty_label = " "
		return empty_label

	@staticmethod
	def get_empty_scatter_handle(ax):
		handle = ax.scatter(
			[np.nan], 
			[np.nan], 
			color="none", 
			alpha=0)
		return handle

	def get_base_legend(self, fig, handles, labels, ax=None, number_columns=None, **kwargs):
		if not isinstance(handles, (tuple, list)):
			raise ValueError("invalid type(handles): {}".format(type(handles)))
		if not isinstance(labels, (tuple, list)):
			raise ValueError("invalid type(labels): {}".format(type(labels)))
		number_handles = len(
			handles)
		number_labels = len(
			labels)
		if number_handles != number_labels:
			raise ValueError("{} handles and {} labels are not compatible".format(number_handles, number_labels))
		if number_labels == 0:
			raise ValueError("zero labels found")
		is_add_empty_columns = False
		if number_labels == 1:
			if ax is None:
				raise ValueError("ax is required to get empty_handle")
			is_add_empty_columns = True
			empty_handle = self.get_empty_scatter_handle(
				ax=ax)
			empty_label = self.get_empty_label()
			modified_handles = [
				empty_handle,
				handles[0],
				empty_handle]
			modified_labels = [
				empty_label,
				labels[0],
				empty_label]
			modified_number_columns = len(
				modified_labels)
		else:
			if number_columns is None:
				modified_number_columns = int(
					number_labels)
			else:
				if not isinstance(number_columns, int):
					raise ValueError("invalid type(number_columns): {}".format(type(number_columns)))
				if number_columns <= 0:
					raise ValueError("invalid number_columns: {}".format(number_columns))
				modified_number_columns = int(
					number_columns)
			modified_handles = handles
			modified_labels = labels
		fig.subplots_adjust(
			bottom=0.2)
		leg = fig.legend(
			handles=modified_handles,
			labels=modified_labels,
			ncol=modified_number_columns,
			**kwargs)
		return leg, modified_handles, modified_labels, is_add_empty_columns

	def autoformat_legend(self, leg, labels, title=None, title_color="black", text_colors="black", facecolor="lightgray", edgecolor="gray", is_add_empty_columns=False):
		if not isinstance(is_add_empty_columns, bool):
			raise ValueError("invalid type(is_add_empty_columns): {}".format(type(is_add_empty_columns)))
		number_total_labels = len(
			labels)
		is_labels_non_empty = np.full(
			fill_value=True,
			shape=number_total_labels,
			dtype=bool)
		if is_add_empty_columns:
			is_labels_non_empty[0] = False
			is_labels_non_empty[-1] = False
		number_true_labels = int(
			np.sum(
				is_labels_non_empty))
		if title is not None:
			if not isinstance(title, str):
				raise ValueError("invalid type(title): {}".format(type(title)))
			leg.set_title(
				title,
				prop={
					"size": self.label_size, 
					# "weight" : "semibold",
					})
			if title_color is not None:
				leg.get_title().set_color(
					title_color)
		leg._legend_box.align = "center"
		frame = leg.get_frame()
		if facecolor is not None:
			if not isinstance(facecolor, str):
				raise ValueError("invalid type(facecolor): {}".format(type(facecolor)))
			frame.set_facecolor(
				facecolor)
		if edgecolor is not None:
			if not isinstance(edgecolor, str):
				raise ValueError("invalid type(edgecolor): {}".format(type(edgecolor)))
			frame.set_edgecolor(
				edgecolor)
		if text_colors is not None:
			if isinstance(text_colors, str):
				modified_text_colors = [
					text_colors
						for _ in range(
							number_true_labels)]
			elif isinstance(text_colors, (tuple, list)):
				number_text_colors = len(
					text_colors)
				if number_text_colors != number_true_labels:
					raise ValueError("{} colors and {} labels are not compatible".format(number_text_colors, number_true_labels))
				modified_text_colors = list(
					text_colors)
			else:
				raise ValueError("invalid type(text_colors): {}".format(type(text_colors)))
			for index_at_label, (text, text_color) in enumerate(zip(leg.get_texts(), modified_text_colors)):
				if is_labels_non_empty[index_at_label]:
					text.set_color(
						text_color)
		return leg

	def get_legend(self, fig, handles, labels, ax=None, number_columns=None, title=None, title_color="black", text_colors="black", facecolor="lightgray", edgecolor="gray", **kwargs):
		leg, modified_handles, modified_labels, is_add_empty_columns = self.get_base_legend(
			fig=fig,
			handles=handles,
			labels=labels,
			ax=ax,
			number_columns=number_columns,
			loc="lower center",
			mode="expand",
			fontsize=self.label_size,
			borderaxespad=0.1,
			**kwargs)
		leg = self.autoformat_legend(
			leg=leg,
			labels=modified_labels,
			title=title,
			title_color=title_color,
			text_colors=text_colors,
			facecolor=facecolor,
			edgecolor=edgecolor,
			is_add_empty_columns=is_add_empty_columns)
		return leg

class VisualSettingsConfiguration(VisualLegendConfiguration):

	def __init__(self, label_size=10):
		super().__init__()
		self.initialize_font_sizes(
			label_size=label_size)

	def initialize_font_sizes(self, label_size):
		if not isinstance(label_size, (int, float)):
			raise ValueError("invalid type(label_size): {}".format(type(label_size)))
		if label_size <= 0:
			raise ValueError("invalid label_size: {}".format(label_size))
		self._label_size = label_size

	def update_save_directory(self, path_to_save_directory=None):
		if path_to_save_directory is not None:
			if not isinstance(path_to_save_directory, str):
				raise ValueError("invalid type(path_to_save_directory): {}".format(type(path_to_save_directory)))
		self._path_to_save_directory = path_to_save_directory

	def display_image(self, fig, save_name=None, dpi=800, bbox_inches="tight", pad_inches=0.1, extension=None, space_replacement=None, **kwargs):
		if save_name is None:
			plt.show()
		elif isinstance(save_name, str):
			save_path = self.get_save_path(
				save_name=save_name,
				default_extension=".png",
				extension=extension,
				space_replacement=space_replacement)
			fig.savefig(
				save_path,
				dpi=dpi,
				bbox_inches=bbox_inches,
				pad_inches=pad_inches,
				**kwargs)
		else:
			raise ValueError("invalid type(save_name): {}".format(type(save_name)))
		plt.close(
			fig)

##