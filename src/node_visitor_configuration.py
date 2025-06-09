import ast


class BaseNodeVisitorConfiguration():

	def __init__(self):
		super().__init__()
		self._module_names = None
		self._node_visitor = None

	@property
	def module_names(self):
		return self._module_names

	@property
	def node_visitor(self):
		return self._node_visitor

	def pre_initialize(self):

		def visit_Import(node):
			for name in node.names:
				self._module_names.add(
					name.name.split(
						".")[0])

		def visit_ImportFrom(node):
			## missing node.module ==> "from foo import bar"
			## level > 0 ==> "from .foo import bar"
			if node.module is not None and node.level == 0:
				self._module_names.add(
					node.module.split(
						".")[0])

		module_names = set()
		node_visitor = ast.NodeVisitor()
		node_visitor.visit_Import = visit_Import
		node_visitor.visit_ImportFrom = visit_ImportFrom
		self._module_names = module_names
		self._node_visitor = node_visitor

class NodeVisitorConfiguration(BaseNodeVisitorConfiguration):

	def __init__(self):
		super().__init__()
		self.pre_initialize()

	def get_imported_module_names(self, path_to_file):
		with open(path_to_file) as f:
			self._node_visitor.visit(
				ast.parse(
					f.read()))
		module_names = list(
			self.module_names)
		self._module_names = set()
		return module_names

##