'''All flash classes of the basic Agent are contained in this file.

'''
from collections import Iterable
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

class Buzz(_Flash):
    '''The Buzz class that is used to define the output of sensors and input to
    interpreters. The class is a child class of a more general _Array class,
    however in applications the Buzz class should be used

    Parameters
    ----------
    buzz_name : str
        The name of the Buzz
    buss_element_names : iterable
        An iterable of names for each element of the Buzz, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Buzz'

class Direction(_Flash):
    '''The Direction class that is used to define the output of moulders
    and input to actuators. The class is a child class of a more general _Array
    class, however in applications the Direction class should be used

    Parameters
    ----------
    direction_name : str
        The name of the Direction
    direction_element_names : iterable
        An iterable of names for each element of the Direction, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Direction'

class Feature(_Flash):
    '''The Feature class that is used to define the output of cortex. The class
    is a child class of a more general _Array class, however in applications
    the Feature class should be used

    Parameters
    ----------
    feature_name : str
        The name of the Feature
    feature_element_names : iterable
        An iterable of names for each element of the Feature, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Feature'

class Belief(_Imprint):
    '''The Belief class that is used to define the persistent output of
    interpreter and input to moulder. The class is a child class of a more
    general _Array class, however in applications the Belief class should be
    used

    Parameters
    ----------
    belief_name : str
        The name of the Belief
    belief_element_names : iterable
        An iterable of names for each element of the Belief, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Belief'

class Resource(_Imprint):
    '''The Resource class that is used to define the items organs can
    intentionally control as part of their execution. In applications 
    the Resource class should only be edited using the ResourceMap class 
    and related classes

    Parameters
    ----------
    resource_name : str
        The name of the Resource
    resource_element_names : iterable
        An iterable of names for each element of the Resource, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Resource'

class Essence(_Imprint):
    '''The Essence class that is used to define the items of the agent that are
    beyond intentional control. In applications where external forces alters
    the essence the Essence class should only be edited using the EssenceMap
    class and related classes

    Parameters
    ----------
    essence_name : str
        The name of the Essence
    essence_element_names : iterable
        An iterable of names for each element of the Essence, each name describing
        some relevant semantics

    '''
    def __name__(self):
        return 'Essence'

class ImprintOperator(object):
    '''Provides different ways to dynamically access subsets or supersets of an
    Imprint. Enables multiple organs to operate on different but overlapping 
    sets of imprints

    Parameters
    ----------
    base_imprints 
        One or an iterable of imprints on which to operate
    slice_labels : iterable, optional
        In case the base imprint should be sliced to a subset of elements, this
        iterable should contain the element labels to keep in the final imprint
    merger : bool, optional
        In case the base imprints should be merged to a larger set of element,
        this flag should be set to True
    new_name : str, optional
        The name to give the final imprint after operation

    '''
    def identity(self):
        '''To handle case where an organ has been initialized with one specific
        imprint, hence no operations are needed.

        Returns
        -------
        imprint : _Imprint
            The single imprint of the operator

        '''
        return self.base_imprints

    def slicer(self):
        '''To handle case where an organ operates on a subset of elements of
        some imprint

        Returns
        -------
        imprint : _Imprint
            The sliced imprint as defined by the operator initialization

        '''
        class_slice = self.base_imprints.__class__(self.new_name, self.slice_labels)
        value_slice = [value for key, value in self.base_imprints._items.items() \
                             if key in self.slice_labels]
        class_slice.set_values(value_slice)

        return class_slice

    def merge(self):
        '''To handle case where an organ operates on a merged set of multiple
        non-overlapping imprints

        Returns
        -------
        imprint : _Imprint
            The merged imprint as defined by the operator initialization

        '''
        union_semantics = []
        union_values = []
        for base_imprint in self.base_imprints:
            union_semantics.extend(base_imprint.keys())
            union_values.extend(base_imprint.values())

        ret_array = self.base_imprints[0].__class__(self.new_name, union_semantics)
        ret_array.set_values(union_values)

        return ret_array

    def __init__(self, base_imprints, slice_labels=None, merger=False,
                 new_name='new_imprint'):

        self.base_imprints = base_imprints
        self.slice_labels = slice_labels
        self.merger = merger
        self.new_name = new_name

        if (not slice_labels is None) and merger:
            raise TypeError('ImprintOperator cannot handle slicing and merging simultaneously')
        
        if not slice_labels is None:
            if not set(slice_labels).issubset(set(self.base_imprints.keys())):
                raise ValueError('Labels to the slicer not found in the current array')

            if not isinstance(base_imprints, _Imprint):
                raise TypeError('Slicing can only be done for Imprints and child classes')

        if merger:
            if len(base_imprints) < 2:
                raise TypeError('Imprint merger requires at least two base imprints')

            for base_imprint in base_imprints:
                if not isinstance(base_imprint, _Imprint):
                    raise TypeError('Only instances of Imprint can be merged')
    
