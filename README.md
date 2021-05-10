Prettytuple
===========

The standard [named tuple][namedtuple_docs] is a popular and handful tool in many cases, which
suffers from its own clunky and messy syntax. Consider an example:

```python
Location = namedtuple('Location', 'lat long')
```

It is a declaration of new record type, named `Location`, with two fields, `lat` and `long`.
But why the type's name is doubled? Why fields are enumerated as a plain string? How do we specify
type hints for fields of this record? And what happens if someone makes a field with invalid name,
such as `if` or `123`?

The present library provides an alternative way to declare named tuples, which doesn't raise these
questions. Just have a look:

```python
@prettytuple
def Location(lat, long): pass
```

Neat and pleasant, isn't it?


Installation
------------

The library consists of a [single file](./prettytuple.py). You can simply copy it into your project,
and then import like any other module. The only thing you need from _prettytuple_ module is
the same-named function:

```python
from prettytuple import prettytuple
```

Usage
-----

After importing, you can use `prettytuple` decorator to convert any function to a named tuple
declaration. The converion rules are following:

  * Function name becomes the record type name;
  * Function arguments become fields of the record (names and order are preserved);
  * Function docstring become docstring of the new type;
  * Function body is discarded. 

Let's come back to our example:

```python
@prettytuple
def Location(lat: float, long: float):
	"Geographical coordinates of a point, i.e. its latitude and longitude."
```

Here we define a subclass of built-in `tuple`, with name `Location` and two fields, `lat`
and `long`. Wa also annotate these fields as floating point numbers and assign a docstring for
this new class.

And the most remarkable thing is that this new `Location` is 100% compatible with your other code
and patterns, because it *is* a good old named tuple under the hood!


License
-------

This software is distributed under [MIT Licence](./LICENSE). You are free to use this software for
any purpose, but do it at your own risk!


[namedtuple_docs]: https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields
