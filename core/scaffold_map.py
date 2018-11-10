'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random

from core.array import _Flash 
from core.message import Resource, Essence

class _Map(_Flash):
    '''Bla bla

    '''
    def _apply_to(self, agent, scaffold_type_label, single=True):
        '''Bla bla

        '''
        scaffold = getattr(agent, scaffold_type_label)
        if scaffold is None:
            raise RuntimeError('Agent has not been assigned ' + \
                'a %s, hence nothing to map' %(scaffold_type_label))

        if single:
            old_value = scaffold[self.scaffold_key]
            map_args_values = list(self.values())
            map_args_total = tuple([old_value] + map_args_values)

        else:
            raise NotImplementedError('Not implemented')

        new_value = self._mapper(*map_args_total)

        if single:
            scaffold[self.scaffold_key] = new_value

    def __init__(self, name, map_func, scaffold_key, map_args_keys):

        super().__init__(name, map_args_keys)

        self.scaffold_key = scaffold_key
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

class ResourceMap(_Map):
    '''Bla bla

    '''
    def apply_to(self, agent):
        '''Bla bla

        '''
        self._apply_to(agent, 'resource')

    def __name__(self):
        return 'ResourceMap'

    def __init__(self, map_name, map_func, resource_key, map_args_keys):

        super().__init__(map_name, map_func, resource_key, map_args_keys)

class EssenceMap(_Map):
    '''Bla bla

    '''
    def apply_to(self, agent):
        '''Bla bla

        '''
        self._apply_to(agent, 'essence')

    def __name__(self):
        return 'EssenceMap'

    def __init__(self, map_name, map_func, essence_key, map_args_keys):

        super().__init__(map_name, map_func, essence_key, map_args_keys)

class MapCollection(object):
    '''Bla bla

    '''
    def is_empty(self):
        '''Bla bla

        '''
        return all([_map.is_empty() for _map in self.map_container])

    def set_values(self, values):
        '''Bla bla

        '''
        for ind, _map in enumerate(self.map_container):
            left, right = self.args_indeces[ind]
            _map.set_values(values[left:right])

    def apply_to(self, agent):
        '''Bla bla

        '''
        for _map in self.map_container:
            _map.apply_to(agent)

    def __iter__(self):

        for _map in self.map_container:
            yield _map

    def __name__(self):
        return 'MapCollection'

    def __init__(self, container):

        self.map_container = container
        self.args_indeces = []

        left = 0
        for _map in self.map_container:
            right = left + _map.n_elements
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

