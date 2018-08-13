'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random

class _ObjectMap(object):
    '''Bla bla

    '''
    def func_to_func(self, func):
        '''Bla bla

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

    def set_func(self, func, func_kwargs):
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

