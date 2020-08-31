#TODO: Brush it up 
#(see https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files)

from collections import namedtuple
import inspect

__all__ = ['prettytuple', 'namedtuple_from_signature']

def _validate_parameter(param):
	if param.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
		msg = "parameter '{name}' has unsupported kind: {kind!s}"
		yield msg.format(name=param.name, kind=param.kind)

def _get_parameters_attribute(attrname, signature):
	empty = inspect.Parameter.empty
	for name, param in signature.parameters.items():
		value = getattr(param, attrname)
		if value is not empty:
			yield name, value

def namedtuple_from_signature(typename, signature, *, docstring=None, **kwds):
	for param in signature.parameters.values():
		for err in _validate_parameter(param):
			raise ValueError(err)

	field_names = list(signature.parameters)
	defaults = dict(_get_parameters_attribute('default', signature))
	annotations = dict(_get_parameters_attribute('annotation', signature))

	if defaults:
		# Is it OK to modify incoming dictionary?
		kwds['defaults'] = [defaults[f] for f in field_names if f in defaults]

	nt = namedtuple(typename, field_names, **kwds)
	if docstring is not None:
		nt.__doc__ = docstring
	if annotations:
		if not hasattr(nt, '__annotations__'):
			nt.__annotations__ = dict()
		nt.__annotations__.update(annotations)
	return nt

def prettytuple(fun):
	if not inspect.isfunction(fun):
		msg = "prettytuple can accept a unsual function only, but got: {type}"
		raise TypeError(msg.format(type=type(fun).__name__))
	name = fun.__name__
	sig = inspect.signature(fun, follow_wrapped=False)
	return namedtuple_from_signature(name, sig, docstring=fun.__doc__, module=fun.__module__)


#TODO: Move tests to an invividual file
if __name__ == '__main__':
	@prettytuple
	def Location(lat: float, long: float): pass

