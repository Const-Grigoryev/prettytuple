"""An alternative way to define a named tuple, clearer and less verbose then the standard one."""

__version__ = "0.1"
__status__ = "Development"
__all__ = ['prettytuple', 'namedtuple_from_signature']

__author__ = "Konstantin Grigoryev"
__copyright__ = "Copyright (c) 2020-2021, Const Grigoryev"

__license__ = "MIT"
__email__ = "aspid812@gmail.com"


from collections import namedtuple
import inspect

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
    """
    Construct a named tuple class from a function signature object, converting function formal
    parameters to field names of the tuple.

    :param typename: Desired name of the named tuple class.
    :param signature: Function signature object (of type :class:`inspect.Signature`).
    :param docstring: Docstring to be pasted into the class.
    :param annotation: Fields' type annotations dictionary (keyword only).
    :param default: Fields' default values (keyword only).
    """
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
    """
    You can prepend a regular function definition with `@prettytuple` decorator to transform it
    to named tuple definition.

    Function name will become the class name of that named tuple, formal arguments will become
    names of its fields, type annotations and docstring will be propagated to the class.

    Example:

        >>> @prettytuple
        >>> def Location(lat: float, long: float):
        ...     "Geographical coordinates of a point, i.e. its latitude and longitude."
    """
    if not inspect.isfunction(fun):
        msg = "prettytuple can accept a usual function only, but got: {type}"
        raise TypeError(msg.format(type=type(fun).__name__))
    name = fun.__name__
    sig = inspect.signature(fun, follow_wrapped=False)
    return namedtuple_from_signature(name, sig, docstring=fun.__doc__, module=fun.__module__)


#TODO: Move tests to an individual file
if __name__ == '__main__':
    @prettytuple
    def Location(lat: float, long: float): pass
