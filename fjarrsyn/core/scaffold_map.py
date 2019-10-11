'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
from collections import Iterable

import numpy as np
import numpy.random

from fjarrsyn.core.array import _Flash, _SupraArray, EmptyFlashError
from fjarrsyn.core.message import Resource, Essence

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
    The map class encodes an operation onto a scaffold of an agent that in some
    manner alters a specific element of a specific scaffold in some specified
    manner. The content of the specification is done separatedly from the
    semantics of the specification, where the latter is typically done during
    initialization within the scope of the Agent class, and the former is done
    by some internal or external instructor, such as a Moulder, Actuator, or
    Compulsion. It is particularly for external causes of internal change to an
    agent that the map class are intended for since it keep a clear separation
    of concerns.

    Available library map force functions and their string

    * `reset` : Reset an old value to a new value
    * `delta` : Add an increment to an old value to produce a new value
    * `scale` : Multiply an old value with a factor to produce a new value
    * `delta_scale` : Add an increment to an old value, multiply the sum by a
                      factor to produce a new value
    * `wiener` : Add random number from zero-centred normal distribution to old
                 value to produce new value
    * `wiener_bounded` : Like `wiener` only new value forced to be bounded
    * `exponential_convergence` : Multiply the difference between an old value
                                  and a target value, add to target value to
                                  produce new value
    * `flip_one_char` : Flip a random character in a string of characters

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
    The map class encodes an operation onto a resource of an agent that in some
    manner alters a specific element of a specific scaffold in some specified
    manner. The content of the specification is done separatedly from the
    semantics of the specification, where the latter is typically done during
    initialization within the scope of the Agent class, and the former is done
    by some internal or external instructor, such as a Moulder, Actuator, or
    Compulsion. It is particularly for external causes of internal change to an
    agent that the map class are intended for since it keep a clear separation
    of concerns.

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
    The map class encodes an operation onto an essence of an agent that in some
    manner alters a specific element of a specific essence in some specified
    manner. The content of the specification is done separatedly from the
    semantics of the specification, where the latter is typically done during
    initialization within the scope of the Agent class, and the former is done
    by an external instructor, in particular Mutation. 

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

    def __getitem__(self, key):
        '''Retrieve an individual map from the collection

        Parameters
        ----------
        key 
            The scaffold key to retrieve the map for

        Returns
        -------
        map
            The map associated with the given key in the map collection

        Raises
        ------
        KeyError
            In case the given key is not associated with any map in the
            collection

        '''
        if not key in self.scaffold_keys:
            raise KeyError('%s not in keys' %(key))

        ind = self.scaffold_keys.index(key)

        return self._arrays[ind]

    def __init__(self, container, mix_indeces=None):

        super().__init__(container)
        self.scaffold_keys = [s.scaffold_key for s in self]

class _ForceFunctions(object):
    '''Bunch of pre-defined map force functions that other classes can use
    to associate a callable force function to a scaffold name

    '''
    def force_func_reset(self, old_value, new_value):
        '''Straight-up reset of a value, regardless of the old value

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        new_value
            The new value to overwrite the old value of the scaffold argument

        Returns
        -------
        new_value
            The new value after transformation

        '''
        return new_value

    def force_func_delta(self, old_value, increment):
        '''Add an increment to the old value to create the new value

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        increment
            The increment to add to the old value

        Returns
        -------
        new_value
            The new value after transformation

        '''
        return old_value + increment

    def force_func_scale(self, old_value, factor):
        '''Multiply a factor and the old value to create the new value

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        factor
            The factor to multiply with

        Returns
        -------
        new_value
            The new value after transformation

        '''
        return old_value * factor

    def force_func_delta_scale(self, old_value, increment, factor):
        '''Increment and multiply the old value to create the new value. The
        equation is new_value = factor * (old_value + increment)

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        increment
            The increment to add to the old value
        factor
            The factor to multiply with

        Returns
        -------
        new_value
            The new value after transformation

        '''
        return self.force_func_scale(self.force_func_delta(old_value, increment), factor)

    def force_func_wiener(self, old_value, std):
        '''Add a random number sampled from a zero-centred normal distribution
        of specified standard-deviation to the old value to create the new
        value. This generates a Wiener process

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        std
            Standard-deviation of the normal distribution from which to sample
            the increment

        Returns
        -------
        new_value
            The new value after transformation

        '''
        increment = np.random.normal(0.0, std)
        return old_value + float(increment)

    def force_func_wiener_bounded(self, old_value, std, lower_bound=-1.0*np.Infinity, 
                             upper_bound=1.0*np.Infinity):
        '''Add a random number sampled from a zero-centred normal distribution
        of specified standard-deviation to the old value and ensure the sum is
        bounded between at least one or two bounds

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        std
            Standard-deviation of the normal distribution from which to sample
            the increment
        lower_bound : optional
            The lower bound to force the new value to, minus infinity if not
            specified
        upper_bound : optional
            The upper bound to force the new value to, infinity if not
            specified

        Returns
        -------
        new_value
            The new value after transformation

        '''
        new_value = self.force_func_wiener(old_value, std)
        new_value = min(max(new_value, lower_bound), upper_bound)
        return new_value

    def force_func_exponential_convergence(self, old_value, loss, target):
        '''Create a new value through an exponential decay converging towards a
        target, or equilibrium, value. The equation is 
        new_value = target + loss * (old_value - target)

        Parameters
        ----------
        old_value 
            The old value of the scaffold argument to be altered
        loss
            The exponential decay coefficient
        target
            The target value towards the force moves 

        Returns
        -------
        new_value
            The new value after transformation

        '''
        if loss > 1.0 or loss < 0.0:
            raise ValueError('The loss factor should be between 0.0 and 1.0, ' + \
                             'not %s' %(str(loss)))

        return target + loss * (old_value - target) 

    def force_func_flip_one_char(self, old_value, alphabet, selector=None):
        '''Flip one character in a string of old value to another value from an
        alphabet, where the selection from the alphabet can be uniformly random
        or not

        Parameters
        ----------
        old_value 
            The old string of characters
        alphabet
            Iterable of characters that defines the alphabet from which to
            sample
        selector : callable, optional
            Function that takes a set of characters from the alphabet and
            selects one. If not defined, the selection is done uniformly random

        Returns
        -------
        new_value
            The new value after transformation

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

def universal_map_maker(scaffold, map_func, func_args, name_maker=None):
    '''Convenience function to generate a map collection for an entire scaffold
    using a single function and argument

    Parameters
    ----------
    scaffold : Resource or Essence
        The scaffold for which to generate a complete map collection
    map_func : callable or str
        Function that processes the input in order to evaluate the new scaffold
        values. The function can be specified as a string denoting one of the
        library functions, see further below. The function can be specified as
        a callable. The callable must accept at least as input the value of the
        scaffold and must return the new value
    func_args : Iterable
        A tuple or list of array semantics that the map_func accepts as input
    name_maker : callable, optional
        A function that given a scaffold key returns a string that is used as
        name for the associated map. If not given, the name defaults to `map
        collection`

    Returns
    -------
    mapcollection : MapCollection
        The map collection of maps for the complete scaffold

    '''
    if isinstance(scaffold, Resource):
        map_root = ResourceMap

    elif isinstance(scaffold, Essence):
        map_root = EssenceMap

    else:
        raise TypeError('Unknown scaffold type: %s' %(str(type(scaffold))))

    name_maker_f = name_maker
    if name_maker is None:
        name_maker_f = lambda x: 'map collection'

    mappers = [map_root(name_maker_f(key), map_func, key, func_args) \
                   for key in scaffold.keys()]

    return MapCollection(mappers)

