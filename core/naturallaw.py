'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random
from collections import Iterable
from collections import OrderedDict

from core.array import _Flash, Resource, Essence

class _Map(_Flash):
    '''Bla bla

    '''
    def __init__(self, name, map_func, scaffold_to_alter, map_keys):

        super().__init__(name, map_keys)

        self.scaffold_to_alter = scaffold_to_alter
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
    def _apply_to_multi_inp(self, agent):
        '''Bla bla

        '''
        if agent.resource is None:
            raise RuntimeError('Agent has not been assigned a resource so ' + \
                               'nothing to transform via a map')                     

        old_values = [agent.resource[key] for key in self.resource_to_alter]
        func_args_vals = old_values + list(self.values())
        new_values = self._mapper(*func_args_vals)
        for new_val, key in zip(new_values, self.resource_to_alter):
            agent.resource[key] = new_val

    def _apply_to_single_inp(self, agent):
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

    def __iter__(self):
        return self.resource_to_alter

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

        if isinstance(self.resource_to_alter, str) or \
            (not isinstance(self.resource_to_alter, Iterable)):
            self.apply_to = self._apply_to_single_inp

        else:
            self.apply_to = self._apply_to_multi_inp

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

    def __iter__(self):

        for mapper in self.map_container:
            yield mapper.__iter__()

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

