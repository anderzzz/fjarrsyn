'''Bla bla

'''
import numpy as np
import numpy.random

from collections import namedtuple

ScaffoldForce = namedtuple('ScaffoldForce', ['function', 'kwargs'])

class ObjectForce(object):
    '''Base class for all non-intentional object propagation part of the agent
    scaffold.

    '''
    def force_func_identity(self, old_value):
        '''Bla bla

        '''
        return old_value

    def _map_force_func(self, force_func):
        '''Bla bla

        '''
        if isinstance(force_func, str):
            try:
                func = getattr(self.predefinedforcefunctions, force_func)
            except AttributeError:
                raise ValueError('Object force method %s undefined' %(force_func))

        elif callable(force_func):
            func = force_func

        else:
            raise TypeError('Object force function either callable or string')

        return func

    def set_force_func(self, scaffold_name, force_func, force_func_kwargs={}):
        '''Bla bla

        '''
        func = self._map_force_func(force_func)
        self.scaffold_force_func[scaffold_name] = ScaffoldForce(func, force_func_kwargs)

    def empty_force_func(self):
        '''Bla bla

        '''
        self.scaffold_force_func = {}

    def __call__(self, agent):
        '''Bla bla

        '''
        for scaffold_name, force in self.scaffold_force_func.items():
            
            if scaffold_name in agent.scaffold:
                old_value = agent.scaffold[scaffold_name]
                new_value = force.function(old_value, **force.kwargs)
                agent.scaffold[scaffold_name] = new_value

    def __init__(self, name):

        self.name = name 
        self.scaffold_force_func = {}

        self.predefinedforcefunctions = _PreDefinedForceFunctions()

class _PreDefinedForceFunctions(object):
    '''Bla bla

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
        if loss > 1.0 or loss < 0.0:
            raise ValueError('The loss factor should be between 0.0 and 1.0, ' + \
                             'not %s' %(str(loss)))

        new_value = old_value * loss
        return new_value

    def force_func_noisy_exponential_decay(self, old_value, loss_mu, loss_std):
        '''Bla bla

        '''
        raise NotImplementedError('Noisy exponential decay not implemented yet') 

class RandomMutator(ObjectForce):
    '''Bla bla

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
                return self.force_func_identity(old_value)

        return new_func

    def set_force_func(self, scaffold_name, force_func, apply_thrs=1.0, force_func_kwargs={}):
        '''Method to set force function, with a random apply threshold.

        Notes
        -----
        Replaces the `set_force_func` method of the parent class `ObjectForce`

        Bla bla

        '''
        func = self._map_force_func(force_func)
        func_decorated = self._roll_dice(func, apply_thrs)
        self.scaffold_force_func[scaffold_name] = ScaffoldForce(func_decorated, force_func_kwargs)

    def __init__(self, name):

        super().__init__(name)

