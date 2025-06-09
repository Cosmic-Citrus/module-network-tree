from visual_settings_configuration import VisualSettingsConfiguration


class BasePlotterConfiguration():

	def __init__(self):
		super().__init__()
		self._visual_settings = None

	@property
	def visual_settings(self):
		return self._visual_settings
		
	def initialize_visual_settings(self, *args, **kwargs):
		self._visual_settings = VisualSettingsConfiguration(
			*args,
			**kwargs)

	def update_save_directory(self, path_to_save_directory=None):
		self.verify_visual_settings()
		self._visual_settings.update_save_directory(
			path_to_save_directory=path_to_save_directory)

	def verify_visual_settings(self):
		if self.visual_settings is None:
			raise ValueError("visual_settings is not initialized")
		if not isinstance(self.visual_settings, VisualSettingsConfiguration):
			raise ValueError("invalid type(self.visual_settings): {}".format(type(self.visual_settings)))

##