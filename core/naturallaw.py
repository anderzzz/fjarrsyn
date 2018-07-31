'''Methods to perturb or alter in random or deterministic fashion the scaffold
of an agent or other scaffolded object

'''
import numpy as np
import numpy.random

from collections import namedtuple

ScaffoldForce = namedtuple('ScaffoldForce', ['function', 'kwargs'])

class ObjectForce(object):
    '''Base class for all non-intentional object propagation part of the agent
    or auxiliary object scaffold.

    Parameters
    ----------
    name : str
        Name of the class instance
    force_scaffold_overlap : bool, optional
        Boolean flag to check that all force objects for a named scaffold are
        matched to a scaffold of the given agent. Default set to `False`.

    '''
    def force_func_identity(self, old_value):
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

    def _map_force_func(self, force_func):
        '''Map input force function argument to a callable. 

        Parameters
        ----------
        force_func
            The input argument for the force function

        Returns
        -------
        func : callable
            The callable function that upon execution creates new value

        Raises
        ------
        ValueError
            If a string given to pre-defined force function, but no such method
            is defined. Check the string.
        TypeError
            If the input is neither string nor a callable

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
        '''Associate scaffold with an object force function

        Parameters
        ----------
        scaffold_name : str
            Name of scaffold
        force_func 
            String that through mapping points to a pre-defined force function,
            or a callable that accepts an old value and returns a new value
            upon execution. The first argument of the callable is mandatory and
            the old value, additional arguments are provided by kwargs
            dictionary, see next parameter
        force_func_kwargs : dict, optional
            Kwargs dictionary for auxiliary force function arguments

        '''
        func = self._map_force_func(force_func)
        self.scaffold_force_func[scaffold_name] = ScaffoldForce(func, force_func_kwargs)

    def empty_force_func(self):
        '''Eradicates all associations between scaffold and force function.
        Convenience function for object forces that can only be used once.

        '''
        self.scaffold_force_func = {}

    def __call__(self, agent):
        '''Apply the object forces to the scaffolds of the agent (or other
        scaffolded object)

        Parameters
        ----------
        agent 
            Instance of the Agent class, or of any other scaffolded class

        Raises
        ------
        RuntimeError
            In case the object force instance is initialized to require that
            object force scaffolds overlap with agent scaffolds, and an
            instance of object force is unmatched with the agent scaffold.

        '''
        for scaffold_name, force in self.scaffold_force_func.items():
            
            if scaffold_name in agent.scaffold:
                old_value = agent.scaffold[scaffold_name]
                new_value = force.function(old_value, **force.kwargs)
                agent.scaffold[scaffold_name] = new_value

            elif force_scaffold_overlap:
                raise RuntimeError('The object force for scaffold %s ' %(scaffold_name) + \
                                   'not matched to any scaffold of agent')

    def __init__(self, name, force_scaffold_overlap=False):

        self.name = name 
        self.scaffold_force_func = {}

        self.predefinedforcefunctions = _PreDefinedForceFunctions()

class _PreDefinedForceFunctions(object):
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
    '''Class to create an object force that randomly mutates a scaffold by some
    function. This class inherets the `ObjectForce` class.

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
                return self.force_func_identity(old_value)

        return new_func

    def set_force_func(self, scaffold_name, force_func, apply_thrs=1.0, force_func_kwargs={}):
        '''Method to set force function, with a random apply threshold.

        Notes
        -----
        Overrides the `set_force_func` method of the parent class `ObjectForce`,
        such that random threshold can be applied.

        Parameters
        ----------
        scaffold_name : str
            Name of scaffold
        force_func 
            String that through mapping points to a pre-defined force function,
            or a callable that accepts an old value and returns a new value
            upon execution. The first argument of the callable is mandatory and
            the old value, additional arguments are provided by kwargs
            dictionary, see next parameter
        apply_thrs : float, optional
            A threshold between 0.0 and 1.0, such that over repeated execution
            the input force function is applied only with frequence equal to
            the threshold. In the other cases the force function returns
            identity and hence leaves the old value unchanged. Visualize this
            as a proverbial roll of the dice to decide if to apply the object
            force or not.
        force_func_kwargs : dict, optional
            Kwargs dictionary for auxiliary force function arguments

        '''
        func = self._map_force_func(force_func)
        func_decorated = self._roll_dice(func, apply_thrs)
        self.scaffold_force_func[scaffold_name] = ScaffoldForce(func_decorated, force_func_kwargs)

    def __init__(self, name, force_scaffold_overlap=False):

        super().__init__(name, force_scaffold_overlap)

