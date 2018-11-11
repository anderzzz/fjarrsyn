'''All array-like base objects. These should not be used directly in
applications but through child classes 

'''
from collections import Iterable, Hashable
from collections import OrderedDict

class EmptyFlashError(Exception):
    pass

class _Array(object):
    '''The parent class of all forms of data and information passing within and
    to and from the exterior of the agent. In applications the appropriate
    child classes should be used. The class is built on top an OrderedDict.

    Parameters
    ----------
    array_name : str
        A name to give to the array
    array_semantics : iterable
        An iterable of label to the elements of the array describing some
        relevant semantics

    '''
    def set_values(self, value_container):
        '''Set values of the array object.

        Parameters
        ----------
        value_container : ordered iterable
            Values of the array as an ordered iterable, like list or tuple, or
            as a single value in case the array contain only one element

        Raises
        ------
        TypeError
            If a non-iterable parameter is given for a multi-element array
        ValueError
            If the value container is not of the length expected based on the
            initialized semantic labels

        '''
        if self.n_elements == 1 and not isinstance(value_container, Iterable):
            value_container = (value_container,)

        else:
            if len(value_container) != self.n_elements:
                raise ValueError('Value container of length %s ' %(str(len(value_container))) + \
                                 'given, expected %s' %str(self.n_elements))

        for value_index, value in enumerate(value_container):
            self._items[self._item_names[value_index]] = value

    def void_array(self):
        '''Return a void array containing the semantics but `None` as values

        Returns
        -------
        void_array : OrderedDict
            The void array containing the array semantics as keys and `None` as
            values to be populated

        '''
        return OrderedDict([(key, None) for key in self._item_names])

    def keys(self):
        '''Return the semantic keys in the defined order

        Returns
        -------
        keys : list
            The semantic values of the array in the order defined upon
            initilization

        '''
        return list(self._items.keys())

    def items(self):
        '''Return iterator over key value pairs of the array, which preserves
        the order set during initilization

        Returns
        -------
        key
            The key of the element of the array
        value
            The corresponding value of the element of the array

        '''
        for key in self.keys():
            yield key, self[key]

    def is_empty(self):
        '''Determine if all values are None

        Returns
        -------
        empty : bool
            True if all values are None, False otherwise

        Notes
        -----
        The method accesses the values of the array indirectly and therefore
        does not consume or otherwise alter the values

        '''
        return all([x is None for x in self._items.values()])

    def __str__(self):
        '''Return the OrderedDictionary view'''

        str_out = str(self._items)
        str_out = str_out.replace('OrderedDict', str(self.__name__()))

        return str_out

    def __setitem__(self, key, value):
        '''Set the value of the array associated with the key. This can only be
        used to change existing values, not create new keys

        Parameters
        ----------
        key 
            The object used as key, presumably a string
        value
            The object assigned to the key

        Raises
        ------
        TypeError
            If a key is given that was not part of the initilization

        '''
        if not key in self.keys():
            raise TypeError('Array semantics is immutable, and new keys ' + \
                            'cannot be added: %s' %(key))

        self._items[key] = value

    def __init__(self, array_name, array_semantics):

        self.name = array_name

        if not isinstance(array_semantics, Iterable):
            raise TypeError('Array semantics should be provided as an iterable')
        if not all([isinstance(x, Hashable) for x in array_semantics]):
            raise TypeError('Elements of array semantics must be hashable')
        self._item_names = array_semantics

        self.n_elements = len(self._item_names)
        self._items = self.void_array()

class _Imprint(_Array):
    '''A child class for _Array which handles persistent information that can
    be accessed non-destructively

    Parameters
    ----------
    imprint_name : str
        A name to give to the imprint
    imprint_semantics : iterable
        An iterable of label to the elements of the imprint describing some
        relevant semantics

    '''
    def values(self):
        '''Return the values in the defined order. Accessing values this way
        does not alter the values

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        '''
        return list(self._items.values())

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        return self._items[key]

    def __init__(self, imprint_name, imprint_semantics):

        super().__init__(imprint_name, imprint_semantics)

class _Flash(_Array):
    '''A child class for _Array which handles transient information that cannot
    be accessed non-destructively

    Parameters
    ----------
    flash_name : str
        A name to give to the flash
    flash_semantics : iterable
        An iterable of label to the elements of the flash describing some
        relevant semantics

    '''
    def values(self):
        '''Return the values in the defined order and exhausts the array after
        reading

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        Raises
        ------
        EmptyFlashError
            In case an empty array is accessed. This suggests the flash has
            been exhausted and that an instructor must be run to re-populate
            the flash.

        '''
        if self.is_empty():
            raise EmptyFlashError('Empty flash array values cannot be accessed. ' + \
                                  'Execute the relevant instructor to populate the array')

        data = list(self._items.values())
        self._items = self.void_array()

        return data

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        data = self._items[key]
        self._items[key] = None

        return data

    def __init__(self, flash_name, flash_semantics):

        super().__init__(flash_name, flash_semantics)

class _SupraArray(object):
    '''Supra arrays contain a collection of other array, with public methods
    mostly like the atomic arrays

    Parameters
    ----------
    container : list, tuple
        An ordered collection of atomic arrays, which all can be flashes or all
        can be imprints, but not a mixture of the two.

    Raises
    ------
    TypeError
        In case the container does not meet specifications

    Notes
    -----
    The supra array is a collection of arrays with public methods and
    attributes very similar to ordinary arrays. The exception is anything
    related to keys. Unlike atomic arrays, where these keys are unique, the
    supra array does not enforce this. Hence, any method that involves getting
    or setting values using keys will raise an informative AttributeError

    '''
    def is_empty(self):
        '''Determine if all values are None

        Returns
        -------
        empty : bool
            True if all values are None, False otherwise

        Notes
        -----
        The method accesses the values of the array indirectly and therefore
        does not consume or otherwise alter the values

        '''
        return all([c.is_empty() for c in self._arrays])

    def set_values(self, values):
        '''Set values of the array object.

        Parameters
        ----------
        values : ordered iterable
            Values of the array as an ordered iterable, like list or tuple.

        '''
        for ind, _array in enumerate(self._arrays):
            left, right = self._array_indeces[ind]
            _array.set_values(values[left:right])

    def values(self):
        '''Return the values in the defined order. If accessing values this way
        is destructive or not depends on the property of the constituent atomic
        arrays

        Returns
        -------
        values : list
            The values of the supra array in the order defined upon
            initialization.

        '''
        ret = []
        for _array in self._arrays:
            ret.append(_array.values())

        return ret

    def keys(self):
        '''Placeholder attribute for key access, which is disallowed for supra
        arrays. Included to catch understandable error and raise informative
        exception.

        Raises
        ------
        AttributeError

        '''
        raise AttributeError('Supra arrays are not guaranteed to have ' + \
                             'unique keys, hence `keys` is invalid attribute')

    def items(self):
        '''Placeholder attribute for key access, which is disallowed for supra
        arrays. Included to catch understandable error and raise informative
        exception.

        Raises
        ------
        AttributeError

        '''
        raise AttributeError('Supra arrays are not guaranteed to have ' + \
                             'unique keys, hence `items` is invalid attribute')

    def __iter__(self):
        '''Iterate over the constituent arrays of the supra array

        Returns
        -------
        arrays
            The arrays in the defined order that constitutes the supra array

        '''
        for _array in self._arrays:
            yield _array

    def __str__(self):
        '''Return the concatenation of the OrderedDictionary view

        '''
        total_str = []
        for _array in self._arrays:
            total_str.append(str(array))

        return ' + '.join(total_str)

    def __setitem__(self, key, value):
        '''Placeholder attribute for key access, which is disallowed for supra
        arrays. Included to catch understandable error and raise informative
        exception.

        Raises
        ------
        AttributeError

        '''
        raise AttributeError('Supra arrays are not guaranteed to have ' + \
                             'unique keys, hence setting with keys ' + \
                             'is invalid')

    def __getitem__(self, key):
        '''Placeholder attribute for key access, which is disallowed for supra
        arrays. Included to catch understandable error and raise informative
        exception.

        Raises
        ------
        AttributeError

        '''
        raise AttributeError('Supra arrays are not guaranteed to have ' + \
                             'unique keys, hence getting with keys ' + \
                             'is invalid')

    def __init__(self, container):

        if not isinstance(container, (list, tuple)):
            raise TypeError('Container must be an ordered iterable')

        if isinstance(container[0], _Flash):
            if not all([isinstance(c, _Flash) for c in container]):
                raise TypeError('Array collection must be of one type of array')

        elif isinstance(container[0], _Imprint):
            if not all([isinstance(c, _Imprint) for c in container]):
                raise TypeError('Array collection must be of one type of array')

        else:
            raise TypeError('Array collection must be comprised of either ' + \
                            '_Flash or _Imprint type')
        self._arrays = container

        self._array_indeces = []
        left = 0
        for _array in self._arrays:
            right = left + _array.n_elements
            self._array_indeces.append((left, right))
            left = right

        self.name = '+'.join([a.name for a in self._arrays])
        self.n_elements = sum([a.n_elements for a in self._arrays])

