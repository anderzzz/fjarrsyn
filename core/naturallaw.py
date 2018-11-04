'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random
from collections import Iterable
from collections import OrderedDict

from core.array import _Flash, Resource

class _ObjectMap(object):
    '''Parent class for mapping agent object. 

    Parameters
    ----------
    mapper : callable
        Function that given an agent instance maps the object
    func_map : _ForceFunctions 
        Instance to the class of library functions for mapping object

    '''
    def func_to_func(self, func):
        '''Map object to a callable function, where the object can be both a
        function or a string pointing to a library function

        Parameters
        ----------
        func 
            The object that is to be mapped to a callable function, where the
            mapping can be identity, in case func is callable.

        Raises
        ------
        ValueError
            In case a function can not be derived from the input

        '''
        if callable(func):
            return func 

        elif not self.func_map is None:
            try:
                return getattr(self.func_map, func)
            except AttributeError:
                raise ValueError('Standard object map method %s undefined' %(force_func))
            
        else:
            raise ValueError('Unknown mapping function encountered: %s' %(func))

    def set_func(self, func, func_kwargs={}):
        '''Bla bla

        '''
        self.kwargs = func_kwargs
        self.func = self.func_to_func(func)

    def empty_map(self):
        '''Bla bla

        '''
        self.func = None
        self.kwargs = None

    def __call__(self, agent):
        '''Bla bla

        '''
        self.mapper(agent)

    def __init__(self, mapper, func_map=None):

        if not callable(mapper):
            raise TypeError('Object mapper must be callable')
        self.mapper = mapper
        self.func_map = func_map

        self.func = None
        self.kwargs = None

class ObjectMapOneOne(_ObjectMap):
    '''Bla bla

    '''
    def map_identity(self, old_value):
        '''Trivial identity force function. Building-block of composite force
        functions.

        Parameters
        ----------
        old_value 
            The old_value of the scaffold to update

        Returns
        -------
        new_value
            The new value to update the scaffold to

        '''
        return old_value

    def _mapper_one_one(self, agent):
        '''Bla bla

        '''
        old_value = agent.scaffold[self.scaffold_to_map]
        new_value = self.func(old_value, **self.kwargs)
        agent.scaffold[self.scaffold_to_map] = new_value

    def __init__(self, scaffold_to_map, standard_funcs=False):

        self.scaffold_to_map = scaffold_to_map
        if standard_funcs:
            func_map = _ForceFunctions()

        else:
            func_map = None

        super().__init__(self._mapper_one_one, func_map)

class ObjectMapCollection(object):
    '''Bla bla

    '''
    def empty_map(self):
        '''Bla bla

        '''
        for scaffold_name, force_func in self.mappers.items():
            force_func.empty_map()

    def set_map_func(self, scaffold_name, force_func, force_func_kwargs={},
                     apply_p=None):
        '''Bla bla

        '''
        if not apply_p is None:
            args = (apply_p, force_func, force_func_kwargs)

        else:
            args = (force_func, force_func_kwargs)

        self.mappers[scaffold_name].set_func(*args)

    def __call__(self, agent):
        '''Bla bla

        '''
        for scaffold_name, force_func in self.mappers.items():
            try:
                force_func(agent)
            except KeyError:
                raise KeyError('Agent lacks scaffold named %s' %(scaffold_name))

    def __init__(self, scaffold_names, standard_funcs=False,
                 stochastic_decoration=False):

        self.mappers = {}
        for scaffold_name in scaffold_names:

            if not stochastic_decoration:
                self.mappers[scaffold_name] = ObjectMapOneOne(scaffold_name,
                                                              standard_funcs)

            else:
                self.mappers[scaffold_name] = ObjectMapOneOneRandom(scaffold_name, 
                                                                    standard_funcs)

class ObjectMapManyMany(_ObjectMap):
    '''Bla bla

    '''
    def _mapper_many_many(self, agent):
        '''Bla bla

        '''
        inp_values = tuple([agent.scaffold[x] for x in self.imprint_inputs])
        out_values = self.func(*inp_values, **self.kwargs)
        for scaffold_key, new_value in zip(self.imprint_outputs, out_values):
            agent.scaffold[scaffold_key] = new_value

    def __init__(self, imprint_inputs, imprint_outputs, standard_funcs=False):

        self.imprint_inputs = imprint_inputs
        self.imprint_outputs = imprint_outputs

        if standard_funcs:
            raise NotImplementedError('Standard functions for many to ' + \
                                      'many object mapping not implemented')

        else:
            func_map = None

        super().__init__(self._mapper_many_many, func_map)

class ObjectMapOneOneRandom(ObjectMapOneOne):
    '''Class to create an object force that randomly mutates a scaffold by some
    function. This class inherets the `ObjectMapOneOne` class.

    Parameters
    ----------
    name : str
        Name of the class instance
    force_scaffold_overlap : bool, optional
        Boolean flag to check that all force objects for a named scaffold are
        matched to a scaffold of the given agent. Default set to `False`.

    '''
    def _roll_dice(self, func, thrs):
        '''Decorator that preprend a given force function with a proverbial
        roll of the dice, wherein the force function is applied as usual if the
        roll of the dice is less than threshold, otherwise the force function is
        substituted for the identity function.

        Parameters
        ----------
        func : callable
            The force function to be applied to a scaffold component
        thrs : float
            The threshold, to be between 0.0 and 1.0, that regulates how
            frequently the force function is applied and how often it does not
            take place

        Returns
        -------
        decorated_func : callable
            The decorated force function

        '''
        def new_func(old_value, *args, **kwargs):
            test_value = np.random.random()
            if test_value < thrs:
                return func(old_value, *args, **kwargs) 
            else:
                return self.map_identity(old_value)

        return new_func

    def set_func(self, apply_p, func, func_kwargs):
        '''Method to set force function, with a random apply threshold.

        '''
        if not isinstance(apply_p, float):
            raise TypeError('Random mapping requires float-valued apply_p parameter')

        self.kwargs = func_kwargs
        self.func = self._roll_dice(self.func_to_func(func), apply_p)

    def __init__(self, scaffold_name, standard_funcs=False):

        super().__init__(scaffold_name, standard_funcs)

class _Map(object):
    '''Bla bla

    '''


class ResourceMap(_Flash):
    '''Defines a map to the agent resources. This is the preferred way to alter
    resources of an agent after initilization

    Parameters
    ----------
    name : str
        Name of the resource map
    resource_to_map_names : iterable
        The labels of the resources to apply a mapping to. These names must
        correspond to a subset of the element labels of an agent scaffold.
        Iterable should be ordered
    map_funcs : iterable
        The functions to apply to the corresponding resource as defined by the
        semantics in the `resource_to_map_names`. The function can either be a
        callable or a string that maps to a standard function, see Notes

    Notes
    -----
    The mapping functions can be standard ones available as strings. The
    standard functions are:

    `delta` : Bla bla

    '''
    def apply_to(self, agent):
        '''Apply the resoure map to the resources of an agent

        Parameters
        ----------
        agent : Agent
            The agent to which to apply the resource mapping

        Notes
        -----
        The resource map is consumed after it is applied. That is it can only
        be applied once to any given agent.

        '''
        if agent.resource is None:
            raise RuntimeError('Agent has not been assigned a resource so ' + \
                               'nothing to transform via a map')                     

        old_value = agent.resource[self.resource_to_alter]
        if old_value is None:
            raise RuntimeError('For agent %s, initial values of ' %(agent) + \
                               'resource %s not assigned' %(self.resource_to_alter))

        func_args_vals = tuple(self.values())
        new_value = self._mapper(old_value, *func_args_vals)
        agent.resource[self.resource_to_alter] = new_value

    def __init__(self, map_name, resource_to_alter, map_func, map_input):

        if not isinstance(map_input, Iterable):
            raise TypeError('The map input should be an iterable')

        super().__init__(map_name, map_input)

        self.resource_to_alter = resource_to_alter
        self.func_library = _ForceFunctions()

        if callable(map_func):
            self._mapper = map_func

        elif isinstance(map_func, str):   
            try:
                transform_func = getattr(self.func_library, 'force_func_' + map_func)

            except AttributeError:
                raise ValueError('No library transformation function exist for ' + \
                                 'label %s' %(map_func))

            self._mapper = transform_func

        else:
            raise TypeError('The map function should be a callable or a ' + \
                            'standard function string')

class ResourceMapCollection(object):
    '''Bla bla

    '''
    def is_empty(self):
        '''Bla bla

        '''
        return all([mapper.is_empty() for mapper in self.map_container])

    def set_values(self, values):
        '''Bla bla

        '''
        for ind, mapper in enumerate(self.map_container):
            left, right = self.args_indeces[ind]
            mapper.set_values(values[left:right])

    def apply_to(self, agent):
        '''Bla bla

        '''
        for mapper in self.map_container:
            mapper.apply_to(agent)

    def __init__(self, container):

        self.map_container = container
        self.args_indeces = []

        left = 0
        for mapper in self.map_container:
            right = left + mapper.n_elements
            self.args_indeces.append((left, right))
            left = right

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
        return old_value + increment

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

