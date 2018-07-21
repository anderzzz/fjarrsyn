'''Bla bla

'''
import numpy as np
import numpy.random

class ObjectForce(object):
    '''Base class for all non-intentional object propagation part of the agent
    scaffold.

    '''
    def wiener(self, old_value, std):
        '''Bla bla

        '''
        increment = np.random.normal(0.0, std)
        return old_value + increment

    def wiener_bounded(self, old_value, std, lower_bound=-1.0*np.Infinity, 
                             upper_bound=1.0*np.Infinity):
        '''Bla bla

        '''
        new_value = self.wiener(old_value, std)
        new_value = min(max(new_value, lower_bound), upper_bound)
        return new_value

    def exponential_decay(self, old_value, loss):
        '''Bla bla

        '''
        if loss > 1.0 or loss < 0.0:
            raise ValueError('The loss factor should be between 0.0 and 1.0, ' + \
                             'not %s' %(str(loss)))

        new_value = old_value * loss
        return new_value

    def noisy_exponential_decay(self, old_value, loss_mu, loss_std):
        '''Bla bla

        '''
        raise NotImplementedError('Noisy exponential decay not implemented yet') 

    def stochastic_addition(self, old_value, increment, thrs_prob):
        '''Bla bla

        '''
        test_value = np.random.random()
        if test_value <= thrs_prob:
            new_value = old_value + increment

        else:
            new_value = old_value

        return new_value

    def stochastic_attempt(self, apply_thrs):
        '''Bla bla

        '''
        test_value = np.random.random()
        return test_value <= apply_thrs

    def set_force_func(self, scaffold_name, force_func, force_func_kwargs={},
                       stochastic_apply=1.0):
        '''Bla bla

        '''
        if isinstance(force_func, str):
            try:
                func = getattr(self, force_func)
            except AttributeError:
                raise ValueError('Object force method %s undefined' %(force_func))

        elif callable(force_func):
            func = force_func

        else:
            raise TypeError('Object force function either callable or string')

        self.scaffold_force_func[scaffold_name] = (func, 
                                                   force_func_kwargs,
                                                   stochastic_apply)

    def __call__(self, agent):
        '''Bla bla

        '''
        for scaffold_name, func_data in self.scaffold_force_func.items():
            
            if scaffold_name in agent.scaffold:
                old_value = agent.scaffold[scaffold_name]
                if self.stochastic_attempt(func_data[2]): 

                    new_value = func_data[0](old_value, **func_data[1])
                else:

                    new_value = old_value

                agent.scaffold[scaffold_name] = new_value

    def __init__(self, name):

        self.name = name 

        self.scaffold_force_func = {}
