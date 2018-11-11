'''Message classes

'''
from core.array import _Imprint, _Flash

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
    
