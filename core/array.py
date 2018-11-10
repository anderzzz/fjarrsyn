'''All array-like base objects. These should not be used directly in
applications but through child classes 

'''
from collections import Iterable, Hashable
from collections import OrderedDict

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

        self.array_name = array_name

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

    '''
    def values(self):
        '''Return the values in the defined order

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        '''
        return list(self._items.values())

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        return self._items[key]

    def __init__(self, imprint_name, imprint_element_names):

        super().__init__(imprint_name, imprint_element_names)

class _Flash(_Array):
    '''A child class for _Array which handles transient information that cannot
    be accessed non-destructively

    '''
    def values(self):
        '''Return the values in the defined order and exhausts the array after
        reading

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        '''
        if self.is_empty():
            raise RuntimeError('Empty flash array values cannot be accessed. ' + \
                               'Execute the relevant organ to populate the array')

        data = list(self._items.values())
        self._items = self.void_array()

        return data

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        data = self._items[key]
        self._items[key] = None

        return data

    def __init__(self, flash_name, flash_element_names):

        super().__init__(flash_name, flash_element_names)

