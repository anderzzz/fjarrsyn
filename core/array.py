'''All flash classes of the basic Agent are contained in this file.

'''
from collections import Iterable
from collections import OrderedDict

class _Array(object):
    '''Bla bla

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
        if self.n_elements > 1:
            if not isinstance(value_container, Iterable):
                raise TypeError('Message with multiple elements given ' + \
                                'non-iterable value cotainer')

            if len(value_container) != self.n_elements:
                raise ValueError('Message container of incorrect length given')

            values = value_container

        else:
            if not isinstance(value_container, Iterable):
                values = [value_container]

            else:
                values = value_container

        for value_index, value in enumerate(values):
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

    def values(self):
        '''Return the values in the defined order

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        '''
        return list(self._items.values())

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

    def slicer(self, labels):
        '''Return a slice of the array based on a set of semantic labels

        Parameters
        ----------
        labels : iterable
            Iterable of semantic labels to include in the array to be
            generated. If a label is included that is not present in the array
            an exception is raised

        Returns
        -------
        array_slice : _Array
            Subarray of the present array

        Raises
        ------
        ValueError
            If the input labels include a value that is not present in the
            current array

        '''
        if not set(labels).issubset(set(self.keys())):
            raise ValueError('Labels to the slicer not found in the current array')

        class_slice = _Array(self.array_name + '_slice', labels)
        value_slice = [value for key, value in self._items.items() if key in labels]
        class_slice.set_values(value_slice)

        return class_slice

    def __str__(self):
        '''Return the OrderedDictionary view'''

        str_out = str(self._items)
        str_out = str_out.replace('OrderedDict','')

        return str_out

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        return self._items[key]

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
        self._item_names = array_semantics

        self.n_elements = len(self._item_names)
        self._items = self.void_array()

class _Flash(_Array):
    '''A child class for _Array which modifiers the parent class in the regard
    that after values are read they are exhausted and the array is emptied.

    '''
    def values(self):
        '''Return the values in the defined order and exhausts the array after
        reading

        Returns
        -------
        values : list
            The values of the array in the order defined upon initilization

        '''
        data = tuple(self._items.values())
        self._items = self.void_array()

        return data

    def __getitem__(self, key):
        '''Return the value of the array associated with a key.'''

        data = self._items[key]
        self._items[key] = None

        return data

    def __init__(self, flash_name, flash_element_names):

        super().__init__(flash_name, flash_element_names)

class Buzz(_Flash):
    '''The Buzz class that is used to define the output of sensors and input to
    interpreters. The class is a child class of a more general _Array class,
    however in applications the Buzz class should be used

    '''
    def __init__(self, buzz_name, buzz_element_names):

        super().__init__(buzz_name, buzz_element_names)

        self.message = self._items

class Direction(_Flash):
    '''The Direction class that is used to define the output of moulders
    and input to actuators. The class is a child class of a more general _Array
    class, however in applications the Direction class should be used

    '''
    def __init__(self, direction_name, direction_element_names):

        super().__init__(direction_name, direction_element_names)

        self.message = self._items

class Feature(_Flash):
    '''The Feature class that is used to define the output of cortex. The class
    is a child class of a more general _Array class, however in applications
    the Feature class should be used

    '''
    def __init__(self, feature_name, feature_element_names):

        super().__init__(feature_name, feature_element_names)

        self.message = self._items

class Belief(_Array):
    '''The Belief class that is used to define the persistent output of
    interpreter and input to moulder. The class is a child class of a more
    general _Array class, however in applications the Belief class should be
    used

    '''
    def __init__(self, belief_name, belief_element_names):

        super().__init__(belief_name, belief_element_names)

        self.message = self._items

class _Scaffold(_Array):
    '''Scaffold class

    '''
    def __init__(self, scaffold_title, item_names):

        super().__init__(scaffold_title, item_names)

class Resource(_Scaffold):
    '''The Resource class that is used to define the items organs can
    intentionally control as part of their execution. In applications 
    the Resource class should only be edited using the ResourceMap class 
    and related classes

    '''
    def __init__(self, resource_title, item_names):

        super().__init__(resource_title, item_names)

        self.element = self._items

class Essence(_Scaffold):
    '''The Essence class that is used to define the items of the agent that are
    beyond intentional control. In applications where external forces alters
    the essence the Essence class should only be edited using the EssenceMap
    class and related classes

    '''
    def __init__(self, essence_title, item_names):

        super().__init__(essence_title, item_names)

        self.element = self._items

