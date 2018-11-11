'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random
from collections import Iterable

from core.array import _Flash, _SupraArray, EmptyFlashError 
from core.message import Resource, Essence

class _Map(_Flash):
    '''Base class for all scaffold maps. 

    Parameters
    ----------
    name : str
        Name of the scaffold map
    map_func : callable or str
        Function that processes the input in order to evaluate the new scaffold
        values. The function can be specified as a string denoting one of the
        library functions, see further below. The function can be specified as
        a callable. The callable must accept at least as input the value of the
        scaffold and must return the new value, see examples for details
    scaffold_key : str
        Key to the element of the corresponding scaffold that is to be altered
        by the map
    map_args_keys : Iterable
        A tuple or list of array semantics that an instructor will populate
        with values upon its execution, which are values that are provided as
        input to the map function

    Raises
    ------
    ValueError
        If the standard library map function string did not match any library
        function
    TypeError
        If the map function was not specified as either a string or a callable

    Notes
    -----
    TO BE WRITTEN

    '''
    def _apply_to(self, scaffold, empty_to_identity=True):
        '''General method to apply a scaffold map to a scaffold

        Parameters
        ----------
        scaffold
            The particular scaffold to apply the map to, typically either an
            instance of class Resource or Essence
        empty_to_identity : bool, optional
            If True, the interpretation of an empty element in the map values
            is that the identity operator should be applied to the current
            value. If False, an exception is raised if an empty element is
            encountered

        Raises
        ------
        EmptyFlashError
            If empty element encountered and the empty_to_identity is False

        Notes
        -----
        The value of the map are transient, which means after the map has been
        applied once, it cannot be applied again, rather the relevant
        instructor must be executed to populate the map again

        '''
        old_value = scaffold[self.scaffold_key]

        #
        # Extract map values. If unassigned (None), decide if that implies
        # identity operator or exception
        #
        compute_new = True
        try:
            map_args_value = self.values()

        except EmptyFlashError:
            if not empty_to_identity:
                raise EmptyFlashError('Non-assigned element in map values encountered')
            compute_new = False

        #
        # Apply the engine of the map
        #
        if compute_new:
            if not isinstance(map_args_value, (list, tuple)):
                map_args_value = (map_args_value,)

            args = tuple(map_args_value)
            new_value = self._mapper(old_value, *args)

        else:
            new_value = old_value

        scaffold[self.scaffold_key] = new_value

    def __init__(self, name, map_func, scaffold_key, map_args_keys):

        super().__init__(name, map_args_keys)

        self.scaffold_key = scaffold_key
        self._func_library = _ForceFunctions()

        if callable(map_func):
            self._mapper = map_func

        elif isinstance(map_func, str):   
            try:
                transform_func = getattr(self._func_library, 'force_func_' + map_func)

            except AttributeError:
                raise ValueError('No library transformation function exist for ' + \
                                 'label %s' %(map_func))

            self._mapper = transform_func

        else:
            raise TypeError('The map function should be a callable or a ' + \
                            'standard function string')

class ResourceMap(_Map):
    '''Definition of how to map existing resources of an agent to an updated
    set of resource

    Parameters
    ----------
    map_name : str
        Name of the resource map
    map_func : callable or str
        Function that processes the input in order to evaluate the new resource
        values. The function can be specified as a string denoting one of the
        library functions, see further below. The function can be specified as
        a callable. The callable must accept at least as input the value of the
        resource and must return the new value, see examples for details
    resource_key : str
        Key to the element of the corresponding resource that is to be altered
        by the map
    map_args_keys : Iterable
        A tuple or list of array semantics that an instructor will populate
        with values upon its execution, which are values that are provided as
        input to the map function

    Notes
    -----
    TO BE WRITTEN

    '''
    def apply_to(self, agent, empty_to_identity=True):
        '''Apply map to agent resource

        Parameters
        ----------
        agent : Agent
            The agent whose resources are to be altered by the resource map
        empty_to_identity : bool, optional
            If True, the interpretation of an empty element in the map values
            is that the identity operator should be applied to the current
            value. If False, an exception is raised if an empty element is
            encountered

        Raises
        ------
        RuntimeError
            If no resources have been assigned to the agent

        Notes
        -----
        The value of the map are transient, which means after the map has been
        applied once, it cannot be applied again, rather the relevant
        instructor must be executed to populate the values again.

        '''
        if agent.resource is None:
            raise RuntimeError('Agent has not been assigned resource')

        self._apply_to(agent.resource, empty_to_identity)

    def __name__(self):
        return 'ResourceMap'

    def __init__(self, map_name, map_func, resource_key, map_args_keys):

        super().__init__(map_name, map_func, resource_key, map_args_keys)

class EssenceMap(_Map):
    '''Definition of how to map existing essence of an agent to an updated
    essence

    Parameters
    ----------
    map_name : str
        Name of the essence map
    map_func : callable or str
        Function that processes the input in order to evaluate the new essence
        values. The function can be specified as a string denoting one of the
        library functions, see further below. The function can be specified as
        a callable. The callable must accept at least as input the value of the
        essence and must return the new value, see examples for details
    essence_key : str
        Key to the element of the corresponding essence that is to be altered
        by the map
    map_args_keys : Iterable
        A tuple or list of array semantics that an instructor will populate
        with values upon its execution, which are values that are provided as
        input to the map function

    Notes
    -----
    TO BE WRITTEN

    '''
    def apply_to(self, agent, empty_to_identity=True):
        '''Apply map to agent essence

        Parameters
        ----------
        agent : Agent
            The agent whose essence are to be altered by the essence map
        empty_to_identity : bool, optional
            If True, the interpretation of an empty element in the map values
            is that the identity operator should be applied to the current
            value. If False, an exception is raised if an empty element is
            encountered

        Raises
        ------
        RuntimeError
            If no essence has been assigned to the agent

        Notes
        -----
        The value of the map are transient, which means after the map has been
        applied once, it cannot be applied again, rather the relevant
        instructor must be executed to populate the values again.

        '''
        if agent.essence is None:
            raise RuntimeError('Agent has not been assigned essence')

        self._apply_to(agent.essence, empty_to_identity)

    def __name__(self):
        return 'EssenceMap'

    def __init__(self, map_name, map_func, essence_key, map_args_keys):

        super().__init__(map_name, map_func, essence_key, map_args_keys)

class MapCollection(_SupraArray):
    '''Creates an object that contains several scaffold maps wherein the public
    methods of the object are similar to other maps. 

    Parameters
    ----------
    container : Iterable
        Collection of scaffold map objects

    Notes
    -----
    The map collection is a collection of maps, where the map collection has
    public methods and attributes very similar to ordinary maps. The exception
    is anything related to map argument keys. Unlike in ordinary maps, where
    these keys are unique, the map collection does not enforce this. Hence, any
    method that involves getting or setting values using keys will raise an
    AttributeError.

    '''
    def apply_to(self, agent, empty_to_identity=True):
        '''Apply map collection to agent 

        Parameters
        ----------
        agent : Agent
            The agent whose scaffold are to be altered by the map collection
        empty_to_identity : bool, optional
            If True, the interpretation of an empty element in the map values
            is that the identity operator should be applied to the current
            value. If False, an exception is raised if an empty element is
            encountered

        Notes
        -----
        The value of the map are transient, which means after the map has been
        applied once, it cannot be applied again, rather the relevant
        instructor must be executed to populate the values again.

        '''
        for _map in self:
            _map.apply_to(agent, empty_to_identity)

    def __name__(self):
        return 'MapCollection'

    def __init__(self, container):

        super().__init__(container)
        self.scaffold_keys = [s.scaffold_key for s in self]

class _ForceFunctions(object):
    '''Bunch of pre-defined object force functions that other classes can use
    to associate a callable force function to a scaffold name

    '''
    def force_func_delta(self, old_value, increment):
        '''Bla bla

        '''
        return old_value + increment

    def force_func_scale(self, old_value, factor):
        '''Bla bla

        '''
        return old_value * factor

    def force_func_delta_scale(self, old_value, increment, factor):
        '''Bla bla

        '''
        return self.force_func_scale(self.force_func_delta(old_value, increment), factor)

    def force_func_wiener(self, old_value, std):
        '''Bla bla

        '''
        increment = np.random.normal(0.0, std)
        return old_value + float(increment)

    def force_func_wiener_bounded(self, old_value, std, lower_bound=-1.0*np.Infinity, 
                             upper_bound=1.0*np.Infinity):
        '''Bla bla

        '''
        new_value = self.force_func_wiener(old_value, std)
        new_value = min(max(new_value, lower_bound), upper_bound)
        return new_value

    def force_func_exponential_decay(self, old_value, loss):
        '''Bla bla

        '''
        return self.force_func_exponential_convergence(old_value, loss, 0.0) 

    def force_func_exponential_convergence(self, old_value, loss, target):
        '''Bla bla

        '''
        if loss > 1.0 or loss < 0.0:
            raise ValueError('The loss factor should be between 0.0 and 1.0, ' + \
                             'not %s' %(str(loss)))

        return target + loss * (old_value - target) 

    def force_func_flip_one_char(self, old_value, alphabet, selector=None):
        '''Bla bla

        '''
        index_flip = np.random.randint(len(old_value))
        other_chars = [x for x in alphabet if not x == old_value[index_flip]]

        if selector is None:
            _selector = lambda options : np.random.choice(options)

        elif callable(selector):
            _selector = selector

        else:
            raise TypeError('Selector must be a callable function, not %s' %(str(type(selector))))

        new_value = old_value[:index_flip] + \
                    _selector(other_chars) + \
                    old_value[index_flip + 1:]

        return new_value

