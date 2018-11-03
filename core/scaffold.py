'''Mapper class

'''
import numpy as np
from collections import Iterable
from collections import OrderedDict

class _ScaffoldMap(object):
    '''Bla bla

    '''
    def set_values(self, value_container):
        '''Bla bla

        '''
        if self.n_elements > 1:
            if not isinstance(value_container, Iterable):
                raise TypeError('Scaffold with multiple elements given ' + \
                                'non-iterable value')

            if len(value_container) != self.n_elements:
                raise ValueError('Scaffold container of incorrect length given')

            values = value_container

        else:
            if not isinstance(value_container, Iterable):
                values = [value_container]
            
            else:
                values = value_container

        for value_index, value in enumerate(values):
            self.scaffold_map_return[self.scaffold_element_names[value_index]] = value

    def void_map(self):
        '''Bla bla

        '''
        return OrderedDict([(key, None) for key in self.scaffold_element_names])

    def __init__(self, name, scaffold_names, map_funcs):

        self.scaffold_name = name
        self.func_library = _ForceFunctions()

        if len(scaffold_names) != len(map_funcs): 
            raise TypeError('Number of scaffold names must equal number ' + \
                            'of mapping functions')

        self.mapper = {}
        for item, map_func in zip(scaffold_names, map_funcs): 
            if callable(map_func):
                self.mapper[item] = map_func

            elif isinstance(map_func, str):   
                try:
                    transform_func = getattr(self.func_library, 'force_func_' + map_func)
                except AttributeError:
                    raise ValueError('No library transformation function exist for ' + \
                                     'label %s' %(map_func))

                self.mapper[item] = transform_func

        self.scaffold_element_names = tuple(scaffold_names)
        self.n_elements = len(self.scaffold_element_names)

        self.scaffold_map_return = self.void_map()

class ResourceMap(_ScaffoldMap):
    '''Bla bla

    '''
    def is_empty(self):
        '''Bla bla

        '''
        return all([x is None for x in self.scaffold_map_return.values()])   

    def __call__(self, agent):
        '''Bla bla

        '''
        resource = agent.resource
        if resource is None:
            raise RuntimeError('Agent has not been assigned a resource so ' + \
                               'nothing to transform via a map')                     
        elif not isinstance(resource, Resource):
            raise TypeError('Agent can only be assigned one resource of ' + \
                            'class Resource')

        for item, resource_map in self.mapper.items():
            derived_adjustment = self.scaffold_map_return[item]
            if derived_adjustment is None:
                continue

            old_value = resource[item]
            if old_value is None:
                raise RuntimeError('Initial values of resource %s not assigned' %(item))
            new_value = resource_map(old_value, derived_adjustment)
            resource[item] = new_value

            self.scaffold_map_return[item] = None

        agent.resource = resource 

    def __init__(self, name, resource_to_map_names, map_funcs):

        super().__init__(name, resource_to_map_names, map_funcs)

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

